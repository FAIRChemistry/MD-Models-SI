"""REST round trip for the Experiment model.

Creates N random Experiment records through the generated REST API
(POST /experiment/), retrieves each one (GET /experiment/{id}?full=true),
and compares the returned record field by field with what was sent.

Usage: python -I roundtrip_rest.py MODEL.md DB_PATH [N]
"""

import json
import random
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from mdmodels import sql
from mdmodels.datamodel import DataModel
from mdmodels.rest.config import RestApiConfig
from mdmodels.rest.create import create_rest_app

model_path, db_path = sys.argv[1], Path(sys.argv[2])
n = int(sys.argv[3]) if len(sys.argv) > 3 else 100
db_path.unlink(missing_ok=True)

lib = DataModel.from_markdown(model_path)
db = sql.DatabaseConnector(library=lib, db_type="sqlite", database=str(db_path))
db.create_tables()
app = FastAPI()
create_rest_app(
    app=app,
    db=db,
    config=RestApiConfig.model_validate(
        {"endpoints": {"Experiment": ["create", "list", "retrieve"]}}
    ),
)
client = TestClient(app)

roles = ["substrate", "product", "cofactor", "inhibitor", "enzyme"]
rng = random.Random(42)


def rand_record(i: int) -> dict:
    return {
        "name": f"experiment-{i}",
        "description": f"Random record {i} for the round-trip test",
        "molecules": [
            {
                "name": f"mol-{i}-{j}-{rng.randint(0, 10**6)}",
                "initial_concentration": rng.uniform(0, 500),
                "role": rng.choice(roles),
            }
            for j in range(rng.randint(1, 6))
        ],
        "enzymes": [
            {
                "name": f"enz-{i}-{j}",
                "initial_concentration": rng.uniform(0, 1),
                "role": "enzyme",
            }
            for j in range(rng.randint(1, 3))
        ],
        "conditions": {"temperature": rng.uniform(4, 80), "pH": rng.uniform(2, 11)},
    }


def strip(obj):
    """Drop storage-only keys (ORM ids, JSON-LD keys) before comparison."""
    if isinstance(obj, dict):
        return {
            k: strip(v)
            for k, v in obj.items()
            if k not in {"id"} and not k.startswith("@") and v is not None
        }
    if isinstance(obj, list):
        return [strip(v) for v in obj]
    return obj


sent, mismatches, order_lost, set_mismatch = [], [], 0, 0
n_molecules = n_enzymes = 0
for i in range(n):
    rec = rand_record(i)
    r = client.post("/experiment/", json=rec)
    assert r.status_code == 200, (r.status_code, r.text[:300])
    rid = r.json()["id"]
    got = client.get(f"/experiment/{rid}", params={"full": True})
    assert got.status_code == 200, got.text[:300]
    back = strip(got.json())
    want = strip(rec)
    n_molecules += len(rec["molecules"])
    n_enzymes += len(rec["enzymes"])
    if back != want:
        # distinguish "same content, different order" from real differences
        same_as_sets = all(
            sorted(json.dumps(x, sort_keys=True) for x in back.get(k, []))
            == sorted(json.dumps(x, sort_keys=True) for x in want.get(k, []))
            for k in ("molecules", "enzymes")
        ) and {k: v for k, v in back.items() if k not in ("molecules", "enzymes")} == {
            k: v for k, v in want.items() if k not in ("molecules", "enzymes")
        }
        if same_as_sets:
            order_lost += 1
        else:
            set_mismatch += 1
            mismatches.append((rec["name"], want, back))

# Second check: link existing Molecule rows into a new Experiment in a
# different order. The link table has no position column, so this shows
# whether array order is stored or only follows row order.
from typing import cast  # noqa: E402

from mdmodels.sql.childref import ChildRef, reconstruct_model  # noqa: E402

with db as session:
    models = db._db_models
    first = session.get(models.Experiment, 1)
    mol_ids = [m["id"] for m in first.to_dict()["molecules"]]
    while len(mol_ids) < 2:  # need at least two rows to reorder
        mol_ids.append(mol_ids[0])
    wanted = list(reversed(mol_ids))
    Exp = reconstruct_model(lib.Experiment)
    relinked = Exp(name="relinked", molecules=[ChildRef(row_pk=i) for i in wanted])
    session.add_all(sql.insert_nested(cast(DataModel, relinked), lib, session, models))
    session.commit()
    row = session.exec(
        sql.select(models.Experiment).where(models.Experiment.name == "relinked")
    ).one()
    returned = [m["id"] for m in row.to_dict()["molecules"]]

report = {
            "records": n,
            "molecules": n_molecules,
            "enzymes": n_enzymes,
            "identical": n - order_lost - set_mismatch,
            "differ_only_in_array_order": order_lost,
            "differ_in_content": set_mismatch,
            "relinked_order_sent": wanted,
            "relinked_order_returned": returned,
            "relinked_order_preserved": wanted == returned,
}
print(json.dumps(report, indent=1))
Path(sys.argv[4] if len(sys.argv) > 4 else "report.json").write_text(
    json.dumps(report, indent=1) + "\n"
)
for name, want, back in mismatches[:2]:
    print("MISMATCH", name)
    print(" sent:", json.dumps(want)[:600])
    print(" back:", json.dumps(back)[:600])
