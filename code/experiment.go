// Package model specification contains Go struct definitions with JSON serialization.
//
// WARNING: This is an auto-generated file.
// Do not edit directly - any changes will be overwritten.

package model_specification

//
// Type definitions
//

// Experiment
//
// A single experiment represents a complete biological assay or reaction study,
// capturing all the essential components and parameters needed to reproduce and
// analyze the experimental results. Each experiment serves as a discrete unit
// of scientific investigation with defined inputs, conditions, and measurable
// outcomes.
type Experiment struct {
	Name        string     `json:"name,omitempty" `
	Description string     `json:"description,omitempty" `
	Molecules   []Molecule `json:"molecules,omitempty" `
	Enzymes     []Enzyme   `json:"enzymes,omitempty" `
	Conditions  Conditions `json:"conditions,omitempty" `
}

// Molecule
//
// A molecule represents a chemical compound or substrate involved in the
// biological reaction, including both reactants and products. This encompasses
// small molecules, cofactors, inhibitors, and any other chemical species that
// participate in or influence the enzymatic process.
type Molecule struct {
	Name                 string  `json:"name,omitempty" `
	InitialConcentration float64 `json:"initial_concentration,omitempty" `
	Role                 Role    `json:"role,omitempty" `
}

// Enzyme
//
// An enzyme is a biological catalyst, typically a protein, that facilitates and
// accelerates specific chemical reactions by lowering the activation energy
// required. Enzymes are highly specific to their substrates and play crucial
// roles in metabolic pathways and biotechnological applications.
type Enzyme struct {
	Name                 string  `json:"name,omitempty" `
	InitialConcentration float64 `json:"initial_concentration,omitempty" `
	Role                 Role    `json:"role,omitempty" `
}

// Conditions
//
// Conditions encompass the critical environmental and physical parameters that
// govern the experimental setup and directly influence enzyme activity,
// reaction kinetics, and overall experimental outcomes. These parameters must
// be carefully controlled and documented for reproducible results.
type Conditions struct {
	Temperature float64 `json:"temperature,omitempty" `
	PH          float64 `json:"pH,omitempty" `
}

// Enum definitions
type Role string

const (
	COFACTOR  Role = "cofactor"
	ENZYME    Role = "enzyme"
	INHIBITOR Role = "inhibitor"
	PRODUCT   Role = "product"
	SUBSTRATE Role = "substrate"
)
