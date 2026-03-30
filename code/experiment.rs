//! This file contains Rust struct definitions with serde serialization.
//!
//! WARNING: This is an auto-generated file.
//! Do not edit directly - any changes will be overwritten.

use derive_builder::Builder;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use derivative::Derivative;

//
// Type definitions
//
/// A single experiment represents a complete biological assay or reaction
/// study, capturing all the essential components and parameters
/// needed to reproduce and analyze the experimental results. Each
/// experiment serves as a discrete unit of scientific investigation
/// with defined inputs, conditions, and measurable outcomes.
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema, Builder, Derivative)]
#[derivative(Default)]
#[serde(default)]
#[allow(non_snake_case)]
pub struct Experiment {
    /// A unique identifier or descriptive name for the experiment
    #[serde(skip_serializing_if = "Option::is_none")]
    #[builder(default, setter(into))]
    #[derivative(Default)]
    pub name: Option<String>,

    /// Detailed description of the experimental procedure, objectives, and
    /// expected outcomes
    #[serde(skip_serializing_if = "Option::is_none")]
    #[builder(default, setter(into))]
    #[derivative(Default)]
    pub description: Option<String>,

    /// Array of all chemical compounds involved in the reaction (substrates,
    /// products, cofactors, inhibitors)
    #[serde(skip_serializing_if = "Vec::is_empty")]
    #[builder(default, setter(into, each(name = "to_molecules")))]
    #[derivative(Default)]
    pub molecules: Vec<Molecule>,

    /// Array of all enzymes used as catalysts in the experiment
    #[serde(skip_serializing_if = "Vec::is_empty")]
    #[builder(default, setter(into, each(name = "to_enzymes")))]
    #[derivative(Default)]
    pub enzymes: Vec<Enzyme>,

    /// Environmental parameters under which the experiment is conducted
    #[serde(skip_serializing_if = "Option::is_none")]
    #[builder(default, setter(into))]
    #[derivative(Default)]
    pub conditions: Option<Conditions>,
}

/// A molecule represents a chemical compound or substrate involved in the
/// biological reaction, including both reactants and products. This
/// encompasses small molecules, cofactors, inhibitors, and any other
/// chemical species that participate in or influence the enzymatic
/// process.
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema, Builder, Derivative)]
#[derivative(Default)]
#[serde(default)]
#[allow(non_snake_case)]
pub struct Molecule {
    /// Chemical name or identifier (IUPAC name, common name, or database ID)
    #[serde(skip_serializing_if = "Option::is_none")]
    #[builder(default, setter(into))]
    #[derivative(Default)]
    pub name: Option<String>,

    /// Starting concentration of the molecule in the reaction mixture
    /// (typically in mM or μM)
    #[serde(skip_serializing_if = "Option::is_none")]
    #[builder(default, setter(into))]
    #[derivative(Default)]
    pub initial_concentration: Option<f64>,

    /// Role of the molecule in the reaction (substrate, product, cofactor,
    /// inhibitor)
    #[serde(skip_serializing_if = "Option::is_none")]
    #[builder(default, setter(into))]
    #[derivative(Default)]
    pub role: Option<Role>,
}

/// An enzyme is a biological catalyst, typically a protein, that
/// facilitates and accelerates specific chemical reactions by
/// lowering the activation energy required. Enzymes are highly
/// specific to their substrates and play crucial roles in metabolic
/// pathways and biotechnological applications.
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema, Builder, Derivative)]
#[derivative(Default)]
#[serde(default)]
#[allow(non_snake_case)]
pub struct Enzyme {
    /// Enzyme name, EC number, or protein identifier from databases like
    /// UniProt
    #[serde(skip_serializing_if = "Option::is_none")]
    #[builder(default, setter(into))]
    #[derivative(Default)]
    pub name: Option<String>,

    /// Starting concentration of the enzyme in the reaction mixture
    /// (typically in mg/mL or μM)
    #[serde(skip_serializing_if = "Option::is_none")]
    #[builder(default, setter(into))]
    #[derivative(Default)]
    pub initial_concentration: Option<f64>,

    /// Role of the enzyme in the reaction (enzyme, cofactor, inhibitor)
    #[serde(skip_serializing_if = "Option::is_none")]
    #[builder(default, setter(into))]
    #[derivative(Default)]
    pub role: Option<Role>,
}

/// Conditions encompass the critical environmental and physical
/// parameters that govern the experimental setup and directly
/// influence enzyme activity, reaction kinetics, and overall
/// experimental outcomes. These parameters must be carefully
/// controlled and documented for reproducible results.
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema, Builder, Derivative)]
#[derivative(Default)]
#[serde(default)]
#[allow(non_snake_case)]
pub struct Conditions {
    /// Temperature of the reaction mixture (typically in °C)
    #[serde(skip_serializing_if = "Option::is_none")]
    #[builder(default, setter(into))]
    #[derivative(Default)]
    pub temperature: Option<f64>,

    /// pH of the reaction mixture (typically in pH units)
    #[serde(skip_serializing_if = "Option::is_none")]
    #[builder(default, setter(into))]
    #[derivative(Default)]
    pub pH: Option<f64>,
}

//
// Enum definitions
//
#[allow(non_camel_case_types)]
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema, Default, PartialEq, Eq)]
pub enum Role {
    #[default]
    #[serde(rename = "cofactor")]
    Cofactor,

    #[serde(rename = "enzyme")]
    Enzyme,

    #[serde(rename = "inhibitor")]
    Inhibitor,

    #[serde(rename = "product")]
    Product,

    #[serde(rename = "substrate")]
    Substrate,
}