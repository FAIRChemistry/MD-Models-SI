"""
This file contains Pydantic XML model definitions for data validation.

Pydantic is a data validation library that uses Python type annotations.
It allows you to define data models with type hints that are validated
at runtime while providing static type checking.

Usage example:
```python
from my_model import MyModel

# Validates data at runtime
my_model = MyModel(name="John", age=30)

# Type-safe - my_model has correct type hints
print(my_model.name)

# Will raise error if validation fails
try:
    MyModel(name="", age=30)
except ValidationError as e:
    print(e)
```

For more information see:
https://pydantic-xml.readthedocs.io/en/latest/

WARNING: This is an auto-generated file.
Do not edit directly - any changes will be overwritten.
"""

## This is a generated file. Do not modify it manually!

from __future__ import annotations

from enum import Enum
from typing import Optional
from xml.dom import minidom

from pydantic_xml import BaseXmlModel, element


class Experiment(
    BaseXmlModel,
    search_mode="unordered",
):
    """
    A single experiment represents a complete biological assay or reaction study,
    capturing all the essential components and parameters needed to reproduce
    and analyze the experimental results. Each experiment serves as a discrete
    unit of scientific investigation with defined inputs, conditions, and
    measurable outcomes.
    """

    name: Optional[str] = element(
        default=None,
        tag="name",
        description="""A unique identifier or descriptive name for the experiment""",
        json_schema_extra=dict(),
    )
    description: Optional[str] = element(
        default=None,
        tag="description",
        description="""Detailed description of the experimental procedure, objectives, and expected
            outcomes""",
        json_schema_extra=dict(),
    )
    molecules: list[Molecule] = element(
        default_factory=list,
        tag="molecules",
        description="""Array of all chemical compounds involved in the reaction (substrates, products,
            cofactors, inhibitors)""",
        json_schema_extra=dict(),
    )
    enzymes: list[Enzyme] = element(
        default_factory=list,
        tag="enzymes",
        description="""Array of all enzymes used as catalysts in the experiment""",
        json_schema_extra=dict(),
    )
    conditions: Optional[Conditions] = element(
        default=None,
        tag="conditions",
        description="""Environmental parameters under which the experiment is conducted""",
        json_schema_extra=dict(),
    )

    def add_to_molecules(
        self,
        name: Optional[str] = None,
        initial_concentration: Optional[float] = None,
        role: Optional[Role] = None,
        **kwargs,
    ):
        """Helper method to add a new Molecule to the molecules list."""
        params = {
            "name": name,
            "initial_concentration": initial_concentration,
            "role": role,
        }

        self.molecules.append(Molecule(**params))

        return self.molecules[-1]

    def add_to_enzymes(
        self,
        name: Optional[str] = None,
        initial_concentration: Optional[float] = None,
        role: Optional[Role] = None,
        **kwargs,
    ):
        """Helper method to add a new Enzyme to the enzymes list."""
        params = {
            "name": name,
            "initial_concentration": initial_concentration,
            "role": role,
        }

        self.enzymes.append(Enzyme(**params))

        return self.enzymes[-1]

    def xml(self, encoding: str = "unicode") -> str | bytes:
        """Converts the object to an XML string

        Args:
            encoding (str, optional): The encoding to use. If set to "bytes", will return a bytes string.
                                      Defaults to "unicode".

        Returns:
            str | bytes: The XML representation of the object
        """
        if encoding == "bytes":
            return self.to_xml()

        raw_xml = self.to_xml(encoding=None)
        parsed_xml = minidom.parseString(raw_xml)
        return parsed_xml.toprettyxml(indent="  ")


class Molecule(
    BaseXmlModel,
    search_mode="unordered",
):
    """
    A molecule represents a chemical compound or substrate involved in the
    biological reaction, including both reactants and products. This encompasses
    small molecules, cofactors, inhibitors, and any other chemical species that
    participate in or influence the enzymatic process.
    """

    name: Optional[str] = element(
        default=None,
        tag="name",
        description="""Chemical name or identifier (IUPAC name, common name, or database ID)""",
        json_schema_extra=dict(),
    )
    initial_concentration: Optional[float] = element(
        default=None,
        tag="initial concentration",
        description="""Starting concentration of the molecule in the reaction mixture (typically in mM
            or μM)""",
        json_schema_extra=dict(),
    )
    role: Optional[Role] = element(
        default=None,
        tag="role",
        description="""Role of the molecule in the reaction (substrate, product, cofactor, inhibitor)""",
        json_schema_extra=dict(),
    )

    def xml(self, encoding: str = "unicode") -> str | bytes:
        """Converts the object to an XML string

        Args:
            encoding (str, optional): The encoding to use. If set to "bytes", will return a bytes string.
                                      Defaults to "unicode".

        Returns:
            str | bytes: The XML representation of the object
        """
        if encoding == "bytes":
            return self.to_xml()

        raw_xml = self.to_xml(encoding=None)
        parsed_xml = minidom.parseString(raw_xml)
        return parsed_xml.toprettyxml(indent="  ")


class Enzyme(
    BaseXmlModel,
    search_mode="unordered",
):
    """
    An enzyme is a biological catalyst, typically a protein, that facilitates and
    accelerates specific chemical reactions by lowering the activation energy
    required. Enzymes are highly specific to their substrates and play crucial
    roles in metabolic pathways and biotechnological applications.
    """

    name: Optional[str] = element(
        default=None,
        tag="name",
        description="""Enzyme name, EC number, or protein identifier from databases like UniProt""",
        json_schema_extra=dict(),
    )
    initial_concentration: Optional[float] = element(
        default=None,
        tag="initial concentration",
        description="""Starting concentration of the enzyme in the reaction mixture (typically in mg/mL
            or μM)""",
        json_schema_extra=dict(),
    )
    role: Optional[Role] = element(
        default=None,
        tag="role",
        description="""Role of the enzyme in the reaction (enzyme, cofactor, inhibitor)""",
        json_schema_extra=dict(),
    )

    def xml(self, encoding: str = "unicode") -> str | bytes:
        """Converts the object to an XML string

        Args:
            encoding (str, optional): The encoding to use. If set to "bytes", will return a bytes string.
                                      Defaults to "unicode".

        Returns:
            str | bytes: The XML representation of the object
        """
        if encoding == "bytes":
            return self.to_xml()

        raw_xml = self.to_xml(encoding=None)
        parsed_xml = minidom.parseString(raw_xml)
        return parsed_xml.toprettyxml(indent="  ")


class Conditions(
    BaseXmlModel,
    search_mode="unordered",
):
    """
    Conditions encompass the critical environmental and physical parameters that
    govern the experimental setup and directly influence enzyme activity,
    reaction kinetics, and overall experimental outcomes. These parameters must
    be carefully controlled and documented for reproducible results.
    """

    temperature: Optional[float] = element(
        default=None,
        tag="temperature",
        description="""Temperature of the reaction mixture (typically in °C)""",
        json_schema_extra=dict(),
    )
    pH: Optional[float] = element(
        default=None,
        tag="pH",
        description="""pH of the reaction mixture (typically in pH units)""",
        json_schema_extra=dict(),
    )

    def xml(self, encoding: str = "unicode") -> str | bytes:
        """Converts the object to an XML string

        Args:
            encoding (str, optional): The encoding to use. If set to "bytes", will return a bytes string.
                                      Defaults to "unicode".

        Returns:
            str | bytes: The XML representation of the object
        """
        if encoding == "bytes":
            return self.to_xml()

        raw_xml = self.to_xml(encoding=None)
        parsed_xml = minidom.parseString(raw_xml)
        return parsed_xml.toprettyxml(indent="  ")


class Role(Enum):
    """Enumeration for Role values"""

    COFACTOR = "cofactor"
    ENZYME = "enzyme"
    INHIBITOR = "inhibitor"
    PRODUCT = "product"
    SUBSTRATE = "substrate"
