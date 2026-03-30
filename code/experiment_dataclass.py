"""
This file contains dataclass definitions for data validation.

Dataclasses are a built-in Python library that provides a way to define data models
with type hints and automatic serialization to JSON.

Usage example:
```python
from my_model import MyModel

# Validates data at runtime
my_model = MyModel(name="John", age=30)

# Type-safe - my_model has correct type hints
print(my_model.name)
```

For more information see:
https://docs.python.org/3/library/dataclasses.html

WARNING: This is an auto-generated file.
Do not edit directly - any changes will be overwritten.
"""


## This is a generated file. Do not modify it manually!

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import uuid4

from dataclasses_json import config, dataclass_json


@dataclass_json
@dataclass
class Experiment:
    name: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    description: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    molecules: list[Molecule] = field(default_factory=list)
    enzymes: list[Enzyme] = field(default_factory=list)
    conditions: Optional[Conditions] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )

    # JSON-LD fields
    id: str = field(
        metadata=config(field_name="@id"),
        default_factory=lambda: "md:Experiment/" + str(uuid4()),
    )
    __type__: list[str] = field(
        metadata=config(field_name="@type"),
        default_factory=lambda: [
            "md:Experiment",
        ],
    )
    __context__: dict[str, str | dict] = field(
        metadata=config(field_name="@context"),
        default_factory=lambda: {
            "md": "http://mdmodel.net",
            "Experiment": "http://mdmodel.net#Experiment/",
            "Molecule": "http://mdmodel.net#Molecule/",
            "Enzyme": "http://mdmodel.net#Enzyme/",
            "Conditions": "http://mdmodel.net#Conditions/",
            "Role": "http://mdmodel.net#Role/",
        },
    )

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


@dataclass_json
@dataclass
class Molecule:
    name: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    initial_concentration: Optional[float] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    role: Optional[Role] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )

    # JSON-LD fields
    id: str = field(
        metadata=config(field_name="@id"),
        default_factory=lambda: "md:Molecule/" + str(uuid4()),
    )
    __type__: list[str] = field(
        metadata=config(field_name="@type"),
        default_factory=lambda: [
            "md:Molecule",
        ],
    )
    __context__: dict[str, str | dict] = field(
        metadata=config(field_name="@context"),
        default_factory=lambda: {
            "md": "http://mdmodel.net",
            "Experiment": "http://mdmodel.net#Experiment/",
            "Molecule": "http://mdmodel.net#Molecule/",
            "Enzyme": "http://mdmodel.net#Enzyme/",
            "Conditions": "http://mdmodel.net#Conditions/",
            "Role": "http://mdmodel.net#Role/",
        },
    )


@dataclass_json
@dataclass
class Enzyme:
    name: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    initial_concentration: Optional[float] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    role: Optional[Role] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )

    # JSON-LD fields
    id: str = field(
        metadata=config(field_name="@id"),
        default_factory=lambda: "md:Enzyme/" + str(uuid4()),
    )
    __type__: list[str] = field(
        metadata=config(field_name="@type"),
        default_factory=lambda: [
            "md:Enzyme",
        ],
    )
    __context__: dict[str, str | dict] = field(
        metadata=config(field_name="@context"),
        default_factory=lambda: {
            "md": "http://mdmodel.net",
            "Experiment": "http://mdmodel.net#Experiment/",
            "Molecule": "http://mdmodel.net#Molecule/",
            "Enzyme": "http://mdmodel.net#Enzyme/",
            "Conditions": "http://mdmodel.net#Conditions/",
            "Role": "http://mdmodel.net#Role/",
        },
    )


@dataclass_json
@dataclass
class Conditions:
    temperature: Optional[float] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    pH: Optional[float] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )

    # JSON-LD fields
    id: str = field(
        metadata=config(field_name="@id"),
        default_factory=lambda: "md:Conditions/" + str(uuid4()),
    )
    __type__: list[str] = field(
        metadata=config(field_name="@type"),
        default_factory=lambda: [
            "md:Conditions",
        ],
    )
    __context__: dict[str, str | dict] = field(
        metadata=config(field_name="@context"),
        default_factory=lambda: {
            "md": "http://mdmodel.net",
            "Experiment": "http://mdmodel.net#Experiment/",
            "Molecule": "http://mdmodel.net#Molecule/",
            "Enzyme": "http://mdmodel.net#Enzyme/",
            "Conditions": "http://mdmodel.net#Conditions/",
            "Role": "http://mdmodel.net#Role/",
        },
    )


class Role(Enum):
    COFACTOR = "cofactor"
    ENZYME = "enzyme"
    INHIBITOR = "inhibitor"
    PRODUCT = "product"
    SUBSTRATE = "substrate"
