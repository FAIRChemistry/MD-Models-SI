---
repo: "https://github.com/FAIRChemistry/md-models-demo/"
prefix: "expm"
prefixes:
  schema: "https://schema.org/"
  OBO: "http://purl.obolibrary.org/obo/"
---

# Model Specification

## Types

### Experiment

A single experiment represents a complete biological assay or reaction study, capturing all the essential components and parameters needed to reproduce and analyze the experimental results. Each experiment serves as a discrete unit of scientific investigation with defined inputs, conditions, and measurable outcomes.

- name
  - Type: string
  - Description: A unique identifier or descriptive name for the experiment
  - Term: schema:name
- description
  - Type: string
  - Description: Detailed description of the experimental procedure, objectives, and expected outcomes
  - Term: schema:description
- molecules
  - Type: Molecule[]
  - Description: Array of all chemical compounds involved in the reaction (substrates, products, cofactors, inhibitors)
  - Term: OBO:CHEBI_23367
- enzymes
  - Type: Enzyme[]
  - Description: Array of all enzymes used as catalysts in the experiment
  - Term: OBO:PR_000000001
- conditions
  - Type: Conditions
  - Description: Environmental parameters under which the experiment is conducted

### Molecule

A molecule represents a chemical compound or substrate involved in the biological reaction, including both reactants and products. This encompasses small molecules, cofactors, inhibitors, and any other chemical species that participate in or influence the enzymatic process.

- name: string
  - Type: string
  - Description: Chemical name or identifier (IUPAC name, common name, or database ID)
  - Term: schema:name
- initial concentration
  - Type: float
  - Description: Starting concentration of the molecule in the reaction mixture (typically in mM or μM)
  - Term: OBO:PATO_0000033
- role
  - Type: Role
  - Description: Role of the molecule in the reaction (substrate, product, cofactor, inhibitor)
  - Term: OBO:CHEBI_50906

### Enzyme

An enzyme is a biological catalyst, typically a protein, that facilitates and accelerates specific chemical reactions by lowering the activation energy required. Enzymes are highly specific to their substrates and play crucial roles in metabolic pathways and biotechnological applications.

- name
  - Type: string
  - Description: Enzyme name, EC number, or protein identifier from databases like UniProt
  - Term: schema:name
- initial concentration
  - Type: float
  - Description: Starting concentration of the enzyme in the reaction mixture (typically in mg/mL or μM)
  - Term: OBO:PATO_0000033
- role
  - Type: Role
  - Description: Role of the enzyme in the reaction (enzyme, cofactor, inhibitor)
  - Term: OBO:CHEBI_50906

### Conditions

Conditions encompass the critical environmental and physical parameters that govern the experimental setup and directly influence enzyme activity, reaction kinetics, and overall experimental outcomes. These parameters must be carefully controlled and documented for reproducible results.

- temperature
  - Type: float
  - Description: Temperature of the reaction mixture (typically in °C)
  - Term: OBO:PATO_0000146
- pH
  - Type: float
  - Description: pH of the reaction mixture (typically in pH units)
  - Term: OBO:PATO_0001842

## Enumerations

### Role

```python
SUBSTRATE = "substrate"
PRODUCT = "product"
COFACTOR = "cofactor"
INHIBITOR = "inhibitor"
ENZYME = "enzyme"
```
