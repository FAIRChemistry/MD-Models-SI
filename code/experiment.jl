# This file contains Julia type definitions with JSON serialization.
#
# WARNING: This is an auto-generated file.
# Do not edit directly - any changes will be overwritten.

module ModelSpecification

using JSON3
using StructTypes

#=
  Type Definitions
  ---------------
  Main struct definitions with their fields and JSON serialization support.
=#


"""
Conditions encompass the critical environmental and physical
parameters that govern the experimental setup and directly influence
enzyme activity, reaction kinetics, and overall experimental outcomes.
These parameters must be carefully controlled and documented for
reproducible results.
"""
Base.@kwdef mutable struct Conditions
    """
    Temperature of the reaction mixture (typically in °C)
    """
    temperature::Union{ Float64, Nothing} = nothing

    """
    pH of the reaction mixture (typically in pH units)
    """
    pH::Union{ Float64, Nothing} = nothing

end

export Conditions


"""
An enzyme is a biological catalyst, typically a protein, that
facilitates and accelerates specific chemical reactions by lowering
the activation energy required. Enzymes are highly specific to
their substrates and play crucial roles in metabolic pathways and
biotechnological applications.
"""
Base.@kwdef mutable struct Enzyme
    """
    Enzyme name, EC number, or protein identifier from databases like
    UniProt
    """
    name::Union{ String, Nothing} = nothing

    """
    Starting concentration of the enzyme in the reaction mixture
    (typically in mg/mL or μM)
    """
    initial_concentration::Union{ Float64, Nothing} = nothing

    """
    Role of the enzyme in the reaction (enzyme, cofactor, inhibitor)
    """
    role::Union{ String, Nothing} = nothing

end

export Enzyme


"""
A molecule represents a chemical compound or substrate involved in
the biological reaction, including both reactants and products. This
encompasses small molecules, cofactors, inhibitors, and any other
chemical species that participate in or influence the enzymatic
process.
"""
Base.@kwdef mutable struct Molecule
    """
    Chemical name or identifier (IUPAC name, common name, or database ID)
    """
    name::Union{ String, Nothing} = nothing

    """
    Starting concentration of the molecule in the reaction mixture
    (typically in mM or μM)
    """
    initial_concentration::Union{ Float64, Nothing} = nothing

    """
    Role of the molecule in the reaction (substrate, product, cofactor,
    inhibitor)
    """
    role::Union{ String, Nothing} = nothing

end

export Molecule


"""
A single experiment represents a complete biological assay or reaction
study, capturing all the essential components and parameters needed to
reproduce and analyze the experimental results. Each experiment serves
as a discrete unit of scientific investigation with defined inputs,
conditions, and measurable outcomes.
"""
Base.@kwdef mutable struct Experiment
    """
    A unique identifier or descriptive name for the experiment
    """
    name::Union{ String, Nothing} = nothing

    """
    Detailed description of the experimental procedure, objectives, and
    expected outcomes
    """
    description::Union{ String, Nothing} = nothing

    """
    Array of all chemical compounds involved in the reaction (substrates,
    products, cofactors, inhibitors)
    """
    molecules::Union{Vector{ Molecule }, Nothing} = nothing

    """
    Array of all enzymes used as catalysts in the experiment
    """
    enzymes::Union{Vector{ Enzyme }, Nothing} = nothing

    """
    Environmental parameters under which the experiment is conducted
    """
    conditions::Union{ Conditions, Nothing} = nothing

end

export Experiment


end # module model_specification