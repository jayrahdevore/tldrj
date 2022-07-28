#
#
# tl;drj | boil a json file down to the basics
#
#

import json
from dataclasses import dataclass
from typing import Optional, Union, List, Dict
from enum import Enum, auto
import argparse


class DataTypes(Enum):
    int = auto()
    str = auto()
    float = auto()
    list = auto()

    @classmethod
    def from_type(cls, typeval: type):
        return {int: cls.int, str: cls.str, float: cls.float, list: cls.list}[typeval]


@dataclass
class Element:
    example: any

    @property
    def type(self):
        return type(self.example)

    @property
    def mwe(self):
        """returns first (minimum working example)"""
        return self.example

    @property
    def describe(self):
        """describe types"""
        return DataTypes.from_type(type(self.example)).name

    @property
    def level(self):
        """base level element (leaf)"""
        if self.type is list:
            """empty list"""
            return 0
        return 1


class ElementList(Element):
    key: Optional[str] = None

    def __init__(self, *, example: any, key: str = None):
        self.key = key
        super().__init__(example=example)

    @property
    def type(self):
        if self.key:
            return type(self.key), self.example.type
        return self.example.type

    @property
    def mwe(self):
        """returns first (minimum working example)"""
        if self.key:
            return {self.key: self.example.mwe}
        return [self.example.mwe]

    @property
    def describe(self):
        """describe types"""
        if self.key:
            return {self.key: self.example.describe}
        return [self.example.describe]

    @property
    def level(self):
        """level from leaf"""
        return 1 + self.example.level


@dataclass
class ElementDict(Element):
    @property
    def type(self):
        return type(None)

    @property
    def mwe(self):
        return {k: None if e is None else e.mwe for k, e in self.example.items()}

    @property
    def describe(self):
        return {k: None if e is None else e.describe for k, e in self.example.items()}

    @property
    def level(self):
        """level from leaf"""
        if len(self.example.values()) == 0:
            return 1
        return 1 + max([0 if e is None else e.level for e in self.example.values()])


def parse(data) -> Element | ElementList | ElementDict:
    if type(data) in [int, str, float]:
        return Element(example=data)

    if type(data) is list:
        if len(data) > 0:
            maxv = None
            for d in data:
                parsed = parse(d)
                if maxv is None or maxv.level < parsed.level:
                    maxv = parsed
            return ElementList(example=maxv)
        else:
            return ElementList(example=Element(data))

    if type(data) is dict:
        return ElementDict(example={k: parse(v) for k, v in data.items()})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="file to parse", type=str)

    verb = parser.add_mutually_exclusive_group(required=True)
    verb.add_argument(
        "-m",
        "--mwe",
        help="show a minimum working example",
        action="store_true",
    )
    verb.add_argument("-t", "--type", help="show datatypes", action="store_true")

    args = parser.parse_args()

    data = json.load(open(args.filepath))
    if args.mwe:
        print(json.dumps(parse(data).mwe, indent=4))

    if args.type:
        print(json.dumps(parse(data).describe, indent=4))
