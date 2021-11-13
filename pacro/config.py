from pydantic import BaseModel
from typing import Any, Optional


class FeatureSet(BaseModel):
    """
    binary features:

    default = ["feature1"]
    feature1 = []

    exclusive feature
    feature1 = []
    feature2 = []
    feature3 = []

    exclusive-feature123 = ["feature1", "feature2", "feature3"]

    value feature
    value-feature1 = ["int"]
    value-feature1 = ["int", "0"]
    value-feature2 = ["str", "default"]
    """

    __root__: dict[str, list[str]]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def items(self):
        return self.__root__.items()


class Feature(BaseModel):
    name: str
    take_value: str = ""
    description: str = ""


class FeatureRule(BaseModel):
    name: str = "rule"
    exclusive: list[str] = []
    dependency: list[str] = []


class CompiledFeatureSet:
    features: list[Feature] = []
    rules: list[FeatureRule] = []
    default: dict[str, Any] = {}

    def find_feature(self, name) -> Optional[Feature]:
        for f in self.features:
            if f.name == name:
                return f


def get_default_value(kind: str):
    return {"int": 0, "str": ""}[kind]


def parse_value(kind: str, value: str):
    if kind == "int":
        return int(value)
    return value


def compile_feature_set(feature_set: FeatureSet) -> CompiledFeatureSet:
    compiled = CompiledFeatureSet()
    for name, feature in feature_set.items():
        if name == "default":
            for f in feature:
                compiled.default[f] = True

        elif name.startswith("exclusive-"):
            compiled.rules.append(FeatureRule(name=name, exclusive=feature))
        elif name.startswith("value-"):
            name = name[len("value-"):]
            kind = feature[0]
            compiled.features.append(Feature(name=name, take_value=kind))
            if len(feature) > 1:
                default = parse_value(kind, feature[1])
            else:
                default = parse_value(kind, get_default_value(kind))
            compiled.default[name] = default
        else:
            compiled.features.append(Feature(name=name))
            compiled.rules.append(FeatureRule(name=name, dependency=feature))
            if name not in compiled.default:
                compiled.default[name] = False


    return compiled


class ConfigSelection(BaseModel):
    values: dict[str, Any] = {}
