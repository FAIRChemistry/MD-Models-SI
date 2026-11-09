"""LinkML export round-trip check for MD-Models.

For each input model the script exports a LinkML schema with MD-Models, reads it
back with the LinkML runtime (``SchemaView``), and compares the modelling
features of the source model against the reloaded schema. Features that do not
survive the conversion are written to ``report.json``.

Run with:  uv run roundtrip.py
"""

from __future__ import annotations

import importlib.metadata
import json
import pathlib
import sys

import mdmodels_core as mdm
from linkml_runtime import SchemaView

HERE = pathlib.Path(__file__).parent
MODELS = {
    "experiment-demo": HERE.parent / "model.md",
    "enzymeml-v2": HERE / "models" / "enzymeml_v2.md",
}
PRIMITIVES = {"string", "float", "integer", "boolean", "number", "date", "bytes"}


def _version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


def _expand(curie: str, prefixes: dict[str, str]) -> str:
    if not curie or "://" in curie:
        return curie
    if ":" in curie:
        pfx, local = curie.split(":", 1)
        if pfx in prefixes:
            return prefixes[pfx] + local
    return curie


def _option_key(opt) -> str | None:
    if isinstance(opt, dict):
        return opt.get("key")
    return getattr(opt, "key", None) or getattr(opt, "name", None)


# --------------------------------------------------------------------------- #
# source-side feature extraction (MD-Models)
# --------------------------------------------------------------------------- #
def source_features(md_path: pathlib.Path) -> dict:
    model = mdm.DataModel.from_markdown(str(md_path)).model
    prefixes = dict(getattr(model.config, "prefixes", {}) or {})

    slots: dict[str, dict] = {}
    defaults: list[str] = []
    constraints: dict[str, list[str]] = {}
    xml_annotations: list[str] = []

    for obj in model.objects:
        for attr in obj.attributes:
            key = f"{obj.name}.{attr.name}"
            dtypes = list(attr.dtypes or [])
            slots[key] = {
                "range": dtypes[0] if dtypes else None,
                "all_ranges": dtypes,
                "required": bool(attr.required),
                "multivalued": bool(attr.is_array),
                "has_description": bool((attr.docstring or "").strip()),
                "term": _expand(attr.term, prefixes) if attr.term else None,
            }
            if attr.default is not None:
                defaults.append(key)
            if attr.xml is not None:
                xml_annotations.append(key)
            opts = sorted(
                str(_option_key(o)).lower() for o in (attr.options or []) if _option_key(o)
            )
            if opts:
                constraints[key] = opts

    enums = {}
    for enum in model.enums:
        mappings = dict(enum.mappings)
        enums[enum.name] = {
            "values": sorted(mappings.keys()),
            "value_map": mappings,
            "has_description": bool((enum.docstring or "").strip()),
        }

    return {
        "classes": [o.name for o in model.objects],
        "slots": slots,
        "enums": enums,
        "defaults": sorted(defaults),
        "constraints": constraints,
        "xml_annotations": sorted(xml_annotations),
        "prefixes": prefixes,
    }


# --------------------------------------------------------------------------- #
# reloaded-side feature extraction (LinkML runtime)
# --------------------------------------------------------------------------- #
def linkml_features(yaml_text: str) -> dict:
    path = HERE / "_tmp_schema.yaml"
    path.write_text(yaml_text)
    try:
        view = SchemaView(str(path))
        prefixes = {p.prefix_prefix: p.prefix_reference for p in view.schema.prefixes.values()}
        default_range = view.schema.default_range

        slots: dict[str, dict] = {}
        constraints: dict[str, list[str]] = {}
        identifier_slots: list[str] = []
        # class_induced_slots merges attributes, slot_usage, default_range and
        # inheritance into the effective slot. Identifier slots are tracked
        # separately: LinkML induction marks them required, which the MD-Models
        # importer undoes, so that promotion is a mapping note, not a loss.
        for cn in view.all_classes():
            for slot in view.class_induced_slots(cn):
                key = f"{cn}.{slot.name}"
                if slot.identifier:
                    identifier_slots.append(key)
                slots[key] = {
                    "range": slot.range or default_range,
                    "required": bool(slot.required),
                    "identifier": bool(slot.identifier),
                    "multivalued": bool(slot.multivalued),
                    "has_description": bool((slot.description or "").strip()),
                    "term": _expand(slot.slot_uri, prefixes) if slot.slot_uri else None,
                }
                found = []
                if slot.pattern:
                    found.append("pattern")
                if slot.minimum_value is not None:
                    found.append("minimum")
                if slot.maximum_value is not None:
                    found.append("maximum")
                if found:
                    constraints[key] = sorted(found)

        enums = {}
        for en in view.all_enums():
            e = view.get_enum(en)
            pv = e.permissible_values or {}
            enums[en] = {
                "values": sorted(pv.keys()),
                # MD-Models writes the enum value into the permissible-value description
                "value_map": {k: (v.description or k) for k, v in pv.items()},
                "has_description": bool((e.description or "").strip()),
            }

        return {
            "classes": sorted(view.all_classes().keys()),
            "slots": slots,
            "enums": enums,
            "constraints": constraints,
            "identifier_slots": sorted(identifier_slots),
        }
    finally:
        path.unlink(missing_ok=True)


# --------------------------------------------------------------------------- #
# diff
# --------------------------------------------------------------------------- #
def _norm_range(rng: str | None) -> str | None:
    if rng is None:
        return None
    return rng.lower() if rng.lower() in PRIMITIVES else rng


def diff(src: dict, dst: dict) -> dict:
    lost: list[dict] = []
    changed: list[dict] = []

    for cls in src["classes"]:
        if cls not in dst["classes"]:
            lost.append({"feature": "class", "location": cls})

    for key, s in src["slots"].items():
        d = dst["slots"].get(key)
        if d is None:
            lost.append({"feature": "slot", "location": key})
            continue
        src_range = "string" if s["range"] == "Identifier" else s["range"]
        if len(s["all_ranges"]) <= 1 and _norm_range(src_range) != _norm_range(d["range"]):
            changed.append({"feature": "slot range", "location": key,
                            "source": s["range"], "reloaded": d["range"]})
        # An identifier slot is required by LinkML rule; the importer restores the
        # optional Identifier attribute, so skip that promotion here.
        if not (d.get("identifier") and not s["required"]):
            if s["required"] != d["required"]:
                changed.append({"feature": "required", "location": key,
                                "source": s["required"], "reloaded": d["required"]})
        if s["multivalued"] != d["multivalued"]:
            changed.append({"feature": "multivalued", "location": key,
                            "source": s["multivalued"], "reloaded": d["multivalued"]})
        if s["has_description"] and not d["has_description"]:
            lost.append({"feature": "slot description", "location": key})
        if s["term"] and not d["term"]:
            lost.append({"feature": "ontology term", "location": key})
        elif s["term"] and d["term"] and s["term"] != d["term"]:
            changed.append({"feature": "ontology term", "location": key,
                            "source": s["term"], "reloaded": d["term"]})

    for name, s in src["enums"].items():
        d = dst["enums"].get(name)
        if d is None:
            lost.append({"feature": "enum", "location": name})
            continue
        for v in s["values"]:
            if v not in d["values"]:
                lost.append({"feature": "permissible value", "location": f"{name}.{v}"})
        if s["value_map"] != d["value_map"]:
            changed.append({"feature": "enum value mapping", "location": name,
                            "source": s["value_map"], "reloaded": d["value_map"]})

    for key in src["defaults"]:
        lost.append({"feature": "default value", "location": key})

    for key, opts in src["constraints"].items():
        kept = set(dst["constraints"].get(key, []))
        for opt in opts:
            mapped = {"exclusiveminimum": None, "exclusivemaximum": None,
                      "minimum": "minimum", "maximum": "maximum",
                      "pattern": "pattern"}.get(opt, opt)
            if mapped is None or mapped not in kept:
                lost.append({"feature": f"constraint:{opt}", "location": key})

    for key in src["xml_annotations"]:
        lost.append({"feature": "xml-name annotation", "location": key,
                     "note": "auto-derived from the slot name; no LinkML slot"})

    return {"lost": lost, "changed": changed}


def summarise(src: dict) -> dict:
    return {
        "classes": len(src["classes"]),
        "slots": len(src["slots"]),
        "enumerations": len(src["enums"]),
        "slots_with_ontology_term": sum(1 for s in src["slots"].values() if s["term"]),
        "slots_with_default": len(src["defaults"]),
        "slots_with_constraint": len(src["constraints"]),
    }


def run_one(name: str, md_path: pathlib.Path) -> dict:
    yaml_text = mdm.DataModel.from_markdown(str(md_path)).convert_to(mdm.Templates.Linkml)
    src = source_features(md_path)
    dst = linkml_features(yaml_text)
    d = diff(src, dst)

    lost_by_feature: dict[str, int] = {}
    for item in d["lost"]:
        lost_by_feature[item["feature"]] = lost_by_feature.get(item["feature"], 0) + 1

    return {
        "model": name,
        "source": str(md_path.relative_to(HERE.parent)),
        "summary": summarise(src),
        "lost_count": len(d["lost"]),
        "changed_count": len(d["changed"]),
        "lost_by_feature": lost_by_feature,
        "lost": d["lost"],
        "changed": d["changed"],
        "notes": {
            "identifier_slots": dst.get("identifier_slots", []),
            "identifier_slots_comment": (
                "Slots with an Identifier range are written as LinkML "
                "'identifier: true' slots. LinkML then treats them as required; "
                "the MD-Models importer maps them back to an optional Identifier "
                "attribute, so the bidirectional round-trip is unaffected."
            ),
            "xml_name_annotation_comment": (
                "The xml-name annotation is auto-derived from the slot name and "
                "is regenerated identically on import; it has no LinkML slot."
            ),
        },
    }


def main() -> int:
    report = {
        "description": (
            "MD-Models to LinkML export round-trip. Each model is exported to a "
            "LinkML schema and reloaded with linkml-runtime SchemaView. The "
            "'lost' list holds source features with no representation in the "
            "reloaded schema; 'changed' holds features whose value differs."
        ),
        "mdmodels_core": _version("mdmodels-core"),
        "linkml_runtime": _version("linkml-runtime"),
        "results": [run_one(n, p) for n, p in MODELS.items()],
    }
    out = HERE / "report.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {out}\n")
    for res in report["results"]:
        print(f"  {res['model']:>16}: {res['lost_count']} lost, "
              f"{res['changed_count']} changed  {res['lost_by_feature']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
