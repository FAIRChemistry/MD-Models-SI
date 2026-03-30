import * as D from 'io-ts/Decoder';
import { isLeft } from "fp-ts/Either";

// Generic validate function
export function validate<T>(codec: D.Decoder<unknown, T>, value: unknown): T {
  const result = codec.decode(value);
  if (isLeft(result)) {
    throw new Error(D.draw(result.left));
  }
  return result.right;
}

// JSON-LD Types
export interface JsonLdContext {
  [key: string]: any;
}

export interface JsonLd {
  '@context'?: JsonLdContext;
  '@id'?: string;
  '@type'?: string;
}

// Model Specification Type definitions
/**
    A single experiment represents a complete biological assay or reaction
    study, capturing all the essential components and parameters
    needed to reproduce and analyze the experimental results. Each
    experiment serves as a discrete unit of scientific investigation
    with defined inputs, conditions, and measurable outcomes.

    * @param name - A unique identifier or descriptive name for the experiment
    * @param description - Detailed description of the experimental procedure, objectives, and
             expected outcomes
    * @param molecules - Array of all chemical compounds involved in the reaction (substrates,
             products, cofactors, inhibitors)
    * @param enzymes - Array of all enzymes used as catalysts in the experiment
    * @param conditions - Environmental parameters under which the experiment is conducted
**/
export interface Experiment extends JsonLd {
  name?: string | null;
  description?: string | null;
  molecules?: Molecule[] | null;
  enzymes?: Enzyme[] | null;
  conditions?: Conditions | null;
}

export const ExperimentCodec = D.lazy("Experiment", () => D.struct({
    name: D.nullable(D.string),
    description: D.nullable(D.string),
    molecules: D.array(MoleculeCodec),
    enzymes: D.array(EnzymeCodec),
    conditions: D.nullable(ConditionsCodec),
}));


/**
    A molecule represents a chemical compound or substrate involved in the
    biological reaction, including both reactants and products. This
    encompasses small molecules, cofactors, inhibitors, and any other
    chemical species that participate in or influence the enzymatic
    process.

    * @param name - Chemical name or identifier (IUPAC name, common name, or database ID)
    * @param initial_concentration - Starting concentration of the molecule in the reaction mixture
             (typically in mM or μM)
    * @param role - Role of the molecule in the reaction (substrate, product, cofactor,
             inhibitor)
**/
export interface Molecule extends JsonLd {
  name?: string | null;
  initial_concentration?: number | null;
  role?: Role | null;
}

export const MoleculeCodec = D.lazy("Molecule", () => D.struct({
    name: D.nullable(D.string),
    initial_concentration: D.nullable(D.number),
    role: D.nullable(RoleCodec),
}));


/**
    An enzyme is a biological catalyst, typically a protein, that
    facilitates and accelerates specific chemical reactions by
    lowering the activation energy required. Enzymes are highly
    specific to their substrates and play crucial roles in metabolic
    pathways and biotechnological applications.

    * @param name - Enzyme name, EC number, or protein identifier from databases like
             UniProt
    * @param initial_concentration - Starting concentration of the enzyme in the reaction mixture
             (typically in mg/mL or μM)
    * @param role - Role of the enzyme in the reaction (enzyme, cofactor, inhibitor)
**/
export interface Enzyme extends JsonLd {
  name?: string | null;
  initial_concentration?: number | null;
  role?: Role | null;
}

export const EnzymeCodec = D.lazy("Enzyme", () => D.struct({
    name: D.nullable(D.string),
    initial_concentration: D.nullable(D.number),
    role: D.nullable(RoleCodec),
}));


/**
    Conditions encompass the critical environmental and physical
    parameters that govern the experimental setup and directly
    influence enzyme activity, reaction kinetics, and overall
    experimental outcomes. These parameters must be carefully
    controlled and documented for reproducible results.

    * @param temperature - Temperature of the reaction mixture (typically in °C)
    * @param pH - pH of the reaction mixture (typically in pH units)
**/
export interface Conditions extends JsonLd {
  temperature?: number | null;
  pH?: number | null;
}

export const ConditionsCodec = D.lazy("Conditions", () => D.struct({
    temperature: D.nullable(D.number),
    pH: D.nullable(D.number),
}));


// Model Specification Enum definitions
export enum Role {
  COFACTOR = 'cofactor',
  ENZYME = 'enzyme',
  INHIBITOR = 'inhibitor',
  PRODUCT = 'product',
  SUBSTRATE = 'substrate',
}

export const RoleCodec = D.union(
  D.literal(Role.COFACTOR),
  D.literal(Role.ENZYME),
  D.literal(Role.INHIBITOR),
  D.literal(Role.PRODUCT),
  D.literal(Role.SUBSTRATE),
);