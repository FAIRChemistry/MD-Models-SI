/**
 * This file contains Zod schema definitions for data validation.
 *
 * Zod is a TypeScript-first schema declaration and validation library.
 * It allows you to create schemas that validate data at runtime while
 * providing static type inference.
 *
 * Usage example:
 * ```typescript
 * import { TestSchema } from './schemas';
 *
 * // Validates data at runtime
 * const result = TestSchema.parse(data);
 *
 * // Type-safe - result has correct TypeScript types
 * console.log(result.name);
 *
 * // Will throw error if validation fails
 * try {
 *   TestSchema.parse(invalidData);
 * } catch (err) {
 *   console.error(err);
 * }
 * ```
 *
 * @see https://github.com/colinhacks/zod
 *
 * WARNING: This is an auto-generated file.
 * Do not edit directly - any changes will be overwritten.
 */


import { z } from 'zod';


const BaseSchema = z.object({});

// Model Specification Type definitions
// A single experiment represents a complete biological assay or reaction
// study, capturing all the essential components and parameters needed
// to reproduce and analyze the experimental results. Each experiment
// serves as a discrete unit of scientific investigation with defined
// inputs, conditions, and measurable outcomes.
export const ExperimentSchema = z.lazy(() => BaseSchema.extend({
  name: z.string().nullable().describe(`
    A unique identifier or descriptive name for the experiment
  `),
  description: z.string().nullable().describe(`
    Detailed description of the experimental procedure, objectives, and
    expected outcomes
  `),
  molecules: z.array(MoleculeSchema).describe(`
    Array of all chemical compounds involved in the reaction (substrates,
    products, cofactors, inhibitors)
  `),
  enzymes: z.array(EnzymeSchema).describe(`
    Array of all enzymes used as catalysts in the experiment
  `),
  conditions: ConditionsSchema.nullable().describe(`
    Environmental parameters under which the experiment is conducted
  `),
}));

export type Experiment = z.infer<typeof ExperimentSchema>;

// A molecule represents a chemical compound or substrate involved in the
// biological reaction, including both reactants and products. This
// encompasses small molecules, cofactors, inhibitors, and any other
// chemical species that participate in or influence the enzymatic
// process.
export const MoleculeSchema = z.lazy(() => BaseSchema.extend({
  name: z.string().nullable().describe(`
    Chemical name or identifier (IUPAC name, common name, or database ID)
  `),
  initial_concentration: z.number().nullable().describe(`
    Starting concentration of the molecule in the reaction mixture
    (typically in mM or μM)
  `),
  role: RoleSchema.nullable().describe(`
    Role of the molecule in the reaction (substrate, product, cofactor,
    inhibitor)
  `),
}));

export type Molecule = z.infer<typeof MoleculeSchema>;

// An enzyme is a biological catalyst, typically a protein, that
// facilitates and accelerates specific chemical reactions by lowering
// the activation energy required. Enzymes are highly specific to
// their substrates and play crucial roles in metabolic pathways and
// biotechnological applications.
export const EnzymeSchema = z.lazy(() => BaseSchema.extend({
  name: z.string().nullable().describe(`
    Enzyme name, EC number, or protein identifier from databases like
    UniProt
  `),
  initial_concentration: z.number().nullable().describe(`
    Starting concentration of the enzyme in the reaction mixture
    (typically in mg/mL or μM)
  `),
  role: RoleSchema.nullable().describe(`
    Role of the enzyme in the reaction (enzyme, cofactor, inhibitor)
  `),
}));

export type Enzyme = z.infer<typeof EnzymeSchema>;

// Conditions encompass the critical environmental and physical
// parameters that govern the experimental setup and directly
// influence enzyme activity, reaction kinetics, and overall
// experimental outcomes. These parameters must be carefully
// controlled and documented for reproducible results.
export const ConditionsSchema = z.lazy(() => BaseSchema.extend({
  temperature: z.number().nullable().describe(`
    Temperature of the reaction mixture (typically in °C)
  `),
  pH: z.number().nullable().describe(`
    pH of the reaction mixture (typically in pH units)
  `),
}));

export type Conditions = z.infer<typeof ConditionsSchema>;

// Model Specification Enum definitions
export enum Role {
  COFACTOR = 'cofactor',
  ENZYME = 'enzyme',
  INHIBITOR = 'inhibitor',
  PRODUCT = 'product',
  SUBSTRATE = 'substrate',
}

export const RoleSchema = z.nativeEnum(Role);