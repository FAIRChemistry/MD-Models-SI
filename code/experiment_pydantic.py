"""
This file contains Pydantic model definitions for data validation.

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
https://docs.pydantic.dev/

WARNING: This is an auto-generated file.
Do not edit directly - any changes will be overwritten.
"""


## This is a generated file. Do not modify it manually!

from __future__ import annotations

from enum import Enum
from typing import Generic, Optional, TypeVar
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

# Filter Wrapper definition used to filter a list of objects
# based on their attributes
Cls = TypeVar("Cls")


class FilterWrapper(Generic[Cls]):
    """Wrapper class to filter a list of objects based on their attributes"""

    def __init__(self, collection: list[Cls], **kwargs):
        self.collection = collection
        self.kwargs = kwargs

    def filter(self) -> list[Cls]:
        for key, value in self.kwargs.items():
            self.collection = [
                item for item in self.collection if self._fetch_attr(key, item) == value
            ]
        return self.collection

    def _fetch_attr(self, name: str, item: Cls):
        try:
            return getattr(item, name)
        except AttributeError:
            raise AttributeError(f"{item} does not have attribute {name}")


# JSON-LD Helper Functions
def add_namespace(obj, prefix: str | None, iri: str | None):
    """Adds a namespace to the JSON-LD context

    Args:
        prefix (str): The prefix to add
        iri (str): The IRI to add
    """
    if prefix is None and iri is None:
        return
    elif prefix and iri is None:
        raise ValueError("If prefix is provided, iri must also be provided")
    elif iri and prefix is None:
        raise ValueError("If iri is provided, prefix must also be provided")

    obj.ld_context[prefix] = iri  # type: ignore


def validate_prefix(term: str | dict, prefix: str):
    """Validates that a term is prefixed with a given prefix

    Args:
        term (str): The term to validate
        prefix (str): The prefix to validate against

    Returns:
        bool: True if the term is prefixed with the prefix, False otherwise
    """

    if isinstance(term, dict) and not term["@id"].startswith(prefix + ":"):
        raise ValueError(f"Term {term} is not prefixed with {prefix}")
    elif isinstance(term, str) and not term.startswith(prefix + ":"):
        raise ValueError(f"Term {term} is not prefixed with {prefix}")


# Model Definitions


class Experiment(BaseModel):
    model_config: ConfigDict = ConfigDict(  # type: ignore
        validate_assignment=True,
    )  # type: ignore

    name: Optional[str] = Field(
        default=None,
        description="""A unique identifier or descriptive name for the
        experiment""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Detailed description of the experimental
        procedure, objectives, and expected
        outcomes""",
    )
    molecules: list[Molecule] = Field(
        default_factory=list,
        description="""Array of all chemical compounds involved in the
        reaction (substrates, products, cofactors,
        inhibitors)""",
    )
    enzymes: list[Enzyme] = Field(
        default_factory=list,
        description="""Array of all enzymes used as catalysts in the
        experiment""",
    )
    conditions: Optional[Conditions] = Field(
        default=None,
        description="""Environmental parameters under which the
        experiment is conducted""",
    )

    # JSON-LD fields
    ld_id: str = Field(
        serialization_alias="@id",
        default_factory=lambda: "md:Experiment/" + str(uuid4()),
    )
    ld_type: list[str] = Field(
        serialization_alias="@type",
        default_factory=lambda: [
            "md:Experiment",
        ],
    )
    ld_context: dict[str, str | dict] = Field(
        serialization_alias="@context",
        default_factory=lambda: {
            "md": "http://mdmodel.net",
            "Molecule": "http://mdmodel.net#Molecule/",
            "Enzyme": "http://mdmodel.net#Enzyme/",
            "Conditions": "http://mdmodel.net#Conditions/",
        },
    )

    def filter_molecules(self, **kwargs) -> list[Molecule]:
        """Filters the molecules attribute based on the given kwargs

        Args:
            **kwargs: The attributes to filter by.

        Returns:
            list[Molecule]: The filtered list of Molecule objects
        """

        return FilterWrapper[Molecule](self.molecules, **kwargs).filter()

    def filter_enzymes(self, **kwargs) -> list[Enzyme]:
        """Filters the enzymes attribute based on the given kwargs

        Args:
            **kwargs: The attributes to filter by.

        Returns:
            list[Enzyme]: The filtered list of Enzyme objects
        """

        return FilterWrapper[Enzyme](self.enzymes, **kwargs).filter()

    def set_attr_term(
        self,
        attr: str,
        term: str | dict,
        prefix: str | None = None,
        iri: str | None = None,
    ):
        """Sets the term for a given attribute in the JSON-LD object

        Example:
            # Using an IRI term
            >> obj.set_attr_term("name", "http://schema.org/givenName")

            # Using a prefix and term
            >> obj.set_attr_term("name", "schema:givenName", "schema", "http://schema.org")

            # Usinng a dictionary term
            >> obj.set_attr_term("name", {"@id": "http://schema.org/givenName", "@type": "@id"})

        Args:
            attr (str): The attribute to set the term for
            term (str | dict): The term to set for the attribute

        Raises:
            AssertionError: If the attribute is not found in the model
        """

        assert attr in self.model_fields, (
            f"Attribute {attr} not found in {self.__class__.__name__}"
        )

        if prefix:
            validate_prefix(term, prefix)

        add_namespace(self, prefix, iri)
        self.ld_context[attr] = term

    def add_type_term(
        self, term: str, prefix: str | None = None, iri: str | None = None
    ):
        """Adds a term to the @type field of the JSON-LD object

        Example:
            # Using a term
            >> obj.add_type_term("https://schema.org/Person")

            # Using a prefixed term
            >> obj.add_type_term("schema:Person", "schema", "https://schema.org/Person")

        Args:
            term (str): The term to add to the @type field
            prefix (str, optional): The prefix to use for the term. Defaults to None.
            iri (str, optional): The IRI to use for the term prefix. Defaults to None.

        Raises:
            ValueError: If prefix is provided but iri is not
            ValueError: If iri is provided but prefix is not
        """

        if prefix:
            validate_prefix(term, prefix)

        add_namespace(self, prefix, iri)
        self.ld_type.append(term)

    def add_to_molecules(
        self,
        name: Optional[str] = None,
        initial_concentration: Optional[float] = None,
        role: Optional[Role] = None,
        **kwargs,
    ):
        params = {
            "name": name,
            "initial_concentration": initial_concentration,
            "role": role,
        }

        if "id" in kwargs:
            params["id"] = kwargs["id"]

        self.molecules.append(Molecule(**params))

        return self.molecules[-1]

    def add_to_enzymes(
        self,
        name: Optional[str] = None,
        initial_concentration: Optional[float] = None,
        role: Optional[Role] = None,
        **kwargs,
    ):
        params = {
            "name": name,
            "initial_concentration": initial_concentration,
            "role": role,
        }

        if "id" in kwargs:
            params["id"] = kwargs["id"]

        self.enzymes.append(Enzyme(**params))

        return self.enzymes[-1]


class Molecule(BaseModel):
    model_config: ConfigDict = ConfigDict(  # type: ignore
        validate_assignment=True,
    )  # type: ignore

    name: Optional[str] = Field(
        default=None,
        description="""Chemical name or identifier (IUPAC name, common
        name, or database ID)""",
    )
    initial_concentration: Optional[float] = Field(
        default=None,
        description="""Starting concentration of the molecule in the
        reaction mixture (typically in mM or μM)""",
    )
    role: Optional[Role] = Field(
        default=None,
        description="""Role of the molecule in the reaction (substrate,
        product, cofactor, inhibitor)""",
    )

    # JSON-LD fields
    ld_id: str = Field(
        serialization_alias="@id", default_factory=lambda: "md:Molecule/" + str(uuid4())
    )
    ld_type: list[str] = Field(
        serialization_alias="@type",
        default_factory=lambda: [
            "md:Molecule",
        ],
    )
    ld_context: dict[str, str | dict] = Field(
        serialization_alias="@context",
        default_factory=lambda: {
            "md": "http://mdmodel.net",
            "Role": "http://mdmodel.net#Role/",
        },
    )

    def set_attr_term(
        self,
        attr: str,
        term: str | dict,
        prefix: str | None = None,
        iri: str | None = None,
    ):
        """Sets the term for a given attribute in the JSON-LD object

        Example:
            # Using an IRI term
            >> obj.set_attr_term("name", "http://schema.org/givenName")

            # Using a prefix and term
            >> obj.set_attr_term("name", "schema:givenName", "schema", "http://schema.org")

            # Usinng a dictionary term
            >> obj.set_attr_term("name", {"@id": "http://schema.org/givenName", "@type": "@id"})

        Args:
            attr (str): The attribute to set the term for
            term (str | dict): The term to set for the attribute

        Raises:
            AssertionError: If the attribute is not found in the model
        """

        assert attr in self.model_fields, (
            f"Attribute {attr} not found in {self.__class__.__name__}"
        )

        if prefix:
            validate_prefix(term, prefix)

        add_namespace(self, prefix, iri)
        self.ld_context[attr] = term

    def add_type_term(
        self, term: str, prefix: str | None = None, iri: str | None = None
    ):
        """Adds a term to the @type field of the JSON-LD object

        Example:
            # Using a term
            >> obj.add_type_term("https://schema.org/Person")

            # Using a prefixed term
            >> obj.add_type_term("schema:Person", "schema", "https://schema.org/Person")

        Args:
            term (str): The term to add to the @type field
            prefix (str, optional): The prefix to use for the term. Defaults to None.
            iri (str, optional): The IRI to use for the term prefix. Defaults to None.

        Raises:
            ValueError: If prefix is provided but iri is not
            ValueError: If iri is provided but prefix is not
        """

        if prefix:
            validate_prefix(term, prefix)

        add_namespace(self, prefix, iri)
        self.ld_type.append(term)


class Enzyme(BaseModel):
    model_config: ConfigDict = ConfigDict(  # type: ignore
        validate_assignment=True,
    )  # type: ignore

    name: Optional[str] = Field(
        default=None,
        description="""Enzyme name, EC number, or protein identifier from
        databases like UniProt""",
    )
    initial_concentration: Optional[float] = Field(
        default=None,
        description="""Starting concentration of the enzyme in the
        reaction mixture (typically in mg/mL or
        μM)""",
    )
    role: Optional[Role] = Field(
        default=None,
        description="""Role of the enzyme in the reaction (enzyme,
        cofactor, inhibitor)""",
    )

    # JSON-LD fields
    ld_id: str = Field(
        serialization_alias="@id", default_factory=lambda: "md:Enzyme/" + str(uuid4())
    )
    ld_type: list[str] = Field(
        serialization_alias="@type",
        default_factory=lambda: [
            "md:Enzyme",
        ],
    )
    ld_context: dict[str, str | dict] = Field(
        serialization_alias="@context",
        default_factory=lambda: {
            "md": "http://mdmodel.net",
            "Role": "http://mdmodel.net#Role/",
        },
    )

    def set_attr_term(
        self,
        attr: str,
        term: str | dict,
        prefix: str | None = None,
        iri: str | None = None,
    ):
        """Sets the term for a given attribute in the JSON-LD object

        Example:
            # Using an IRI term
            >> obj.set_attr_term("name", "http://schema.org/givenName")

            # Using a prefix and term
            >> obj.set_attr_term("name", "schema:givenName", "schema", "http://schema.org")

            # Usinng a dictionary term
            >> obj.set_attr_term("name", {"@id": "http://schema.org/givenName", "@type": "@id"})

        Args:
            attr (str): The attribute to set the term for
            term (str | dict): The term to set for the attribute

        Raises:
            AssertionError: If the attribute is not found in the model
        """

        assert attr in self.model_fields, (
            f"Attribute {attr} not found in {self.__class__.__name__}"
        )

        if prefix:
            validate_prefix(term, prefix)

        add_namespace(self, prefix, iri)
        self.ld_context[attr] = term

    def add_type_term(
        self, term: str, prefix: str | None = None, iri: str | None = None
    ):
        """Adds a term to the @type field of the JSON-LD object

        Example:
            # Using a term
            >> obj.add_type_term("https://schema.org/Person")

            # Using a prefixed term
            >> obj.add_type_term("schema:Person", "schema", "https://schema.org/Person")

        Args:
            term (str): The term to add to the @type field
            prefix (str, optional): The prefix to use for the term. Defaults to None.
            iri (str, optional): The IRI to use for the term prefix. Defaults to None.

        Raises:
            ValueError: If prefix is provided but iri is not
            ValueError: If iri is provided but prefix is not
        """

        if prefix:
            validate_prefix(term, prefix)

        add_namespace(self, prefix, iri)
        self.ld_type.append(term)


class Conditions(BaseModel):
    model_config: ConfigDict = ConfigDict(  # type: ignore
        validate_assignment=True,
    )  # type: ignore

    temperature: Optional[float] = Field(
        default=None,
        description="""Temperature of the reaction mixture (typically
        in °C)""",
    )
    pH: Optional[float] = Field(
        default=None,
        description="""pH of the reaction mixture (typically in pH units)""",
    )

    # JSON-LD fields
    ld_id: str = Field(
        serialization_alias="@id",
        default_factory=lambda: "md:Conditions/" + str(uuid4()),
    )
    ld_type: list[str] = Field(
        serialization_alias="@type",
        default_factory=lambda: [
            "md:Conditions",
        ],
    )
    ld_context: dict[str, str | dict] = Field(
        serialization_alias="@context",
        default_factory=lambda: {
            "md": "http://mdmodel.net",
        },
    )

    def set_attr_term(
        self,
        attr: str,
        term: str | dict,
        prefix: str | None = None,
        iri: str | None = None,
    ):
        """Sets the term for a given attribute in the JSON-LD object

        Example:
            # Using an IRI term
            >> obj.set_attr_term("name", "http://schema.org/givenName")

            # Using a prefix and term
            >> obj.set_attr_term("name", "schema:givenName", "schema", "http://schema.org")

            # Usinng a dictionary term
            >> obj.set_attr_term("name", {"@id": "http://schema.org/givenName", "@type": "@id"})

        Args:
            attr (str): The attribute to set the term for
            term (str | dict): The term to set for the attribute

        Raises:
            AssertionError: If the attribute is not found in the model
        """

        assert attr in self.model_fields, (
            f"Attribute {attr} not found in {self.__class__.__name__}"
        )

        if prefix:
            validate_prefix(term, prefix)

        add_namespace(self, prefix, iri)
        self.ld_context[attr] = term

    def add_type_term(
        self, term: str, prefix: str | None = None, iri: str | None = None
    ):
        """Adds a term to the @type field of the JSON-LD object

        Example:
            # Using a term
            >> obj.add_type_term("https://schema.org/Person")

            # Using a prefixed term
            >> obj.add_type_term("schema:Person", "schema", "https://schema.org/Person")

        Args:
            term (str): The term to add to the @type field
            prefix (str, optional): The prefix to use for the term. Defaults to None.
            iri (str, optional): The IRI to use for the term prefix. Defaults to None.

        Raises:
            ValueError: If prefix is provided but iri is not
            ValueError: If iri is provided but prefix is not
        """

        if prefix:
            validate_prefix(term, prefix)

        add_namespace(self, prefix, iri)
        self.ld_type.append(term)


class Role(Enum):
    COFACTOR = "cofactor"
    ENZYME = "enzyme"
    INHIBITOR = "inhibitor"
    PRODUCT = "product"
    SUBSTRATE = "substrate"
