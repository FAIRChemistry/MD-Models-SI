# LinkML export round-trip

`roundtrip.py` exports a model to a LinkML schema with `mdmodels-core`, reloads
it with the LinkML runtime (`SchemaView`), and compares the modelling features of
the source model against the reloaded schema. It reports which features do not
survive the conversion. The source model is read through the parsed-model object
that `mdmodels-core` returns.

Two models are checked:

| model | source |
| --- | --- |
| `experiment-demo` | `../model.md` |
| `enzymeml-v2` | `models/enzymeml_v2.md` (from the EnzymeML specifications repository) |

## Run

```bash
uv run roundtrip.py
```

Dependencies are declared in `pyproject.toml` (`mdmodels-core` is pinned to
0.2.11, `linkml-runtime` for the reload).

## Output

`report.json` lists, per model:

- `summary`: class, slot and enumeration counts, and how many slots carry an
  ontology term, a default, or a constraint.
- `lost`: source features with no representation in the reloaded schema.
- `changed`: features whose value differs after the round-trip.
- `notes`: the slots written as LinkML `identifier` slots, and the handling of
  the auto-derived XML-name annotation.

Classes, slots, ranges, the required and multivalued flags, enumerations with
their permissible values, descriptions and ontology terms are preserved for both
models. The losses are the XML-name annotations (auto-derived from the slot name,
regenerated on import) and, for EnzymeML v2, ten default values and one
`exclusive_minimum` bound, none of which have a LinkML slot.
