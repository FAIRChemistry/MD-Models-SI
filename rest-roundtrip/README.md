# REST round trip

Checks what a record keeps when it goes through the generated REST API and back
(Supporting Information, section "REST round trip").

`roundtrip.py` deploys `../model.md` as the generated FastAPI service on an SQLite
database, creates 100 random `Experiment` records (fixed seed 42) with
`POST /experiment/`, reads each back with `GET /experiment/{id}?full=true`, and
compares the two after dropping the database `id` columns. A second check links the
existing `Molecule` rows of the first record into a new `Experiment` in reverse order
and reports whether that order is returned.

```bash
pip install "mdmodels[rest]" httpx
python roundtrip.py ../model.md roundtrip.db 100 report.json
```

Result with py-mdmodels 0.4.0 on mdmodels-core 0.3.1 (`report.json`): all 100
records (347 molecules, 199 enzymes) are returned identical, including array order.
Re-linked molecules sent in the order 6, 5, 4, 3, 2, 1 come back as 1, 2, 3, 4, 5, 6:
the link tables have no position column, so array order follows row order.
