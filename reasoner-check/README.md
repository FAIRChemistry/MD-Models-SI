# OWL consistency check

`check.py` generates the OWL serialisation of a model with `mdmodels-core`,
parses it with `rdflib`, classifies it with the HermiT reasoner through
`owlready2`, and closes it under OWL-RL with `owlrl`. It reports whether each
ontology is logically consistent and how many external ontology terms the model
references.

Two models are checked:

| model | source |
| --- | --- |
| `experiment-demo` | `../model.md` |
| `enzymeml-v2` | `models/enzymeml_v2.md` (from the EnzymeML specifications repository) |

## Run

```bash
uv run check.py
```

Dependencies are declared in `pyproject.toml` (`mdmodels-core` is pinned to
0.2.11). HermiT needs a Java runtime on `PATH`.

## Output

`report.json` holds, per model: the triple, class and property counts of the
generated ontology, the external ontology terms it aligns to, the HermiT result,
and the OWL-RL closure size. Both models are consistent under both reasoners.
