import copy

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
    values: dict[str, Any] = {}

    def find_feature(self, name) -> Optional[Feature]:
        for f in self.features:
            if f.name == name:
                return f

    def set(self, key: str, value: Any):
        if value is True:
            for rule in self.get_related_rules(key):
                for ex in rule.exclusive:
                    if ex != key:
                        self.set(ex, False)

            for dep in self.get_dependencies(key):
                self.set(dep, True)
        elif value is False:
            for rule in self.get_related_rules(key):
                if key in rule.dependency:
                    self.set(rule.name, False)

        self.values[key] = value
        self.validate_all()

    def get_related_rules(self, key: str):
        rules = []
        for rule in self.rules:
            append = False
            if key == rule.name:
                append = True
            if key in rule.dependency:
                append = True
            if key in rule.exclusive:
                append = True
            if append:
                rules.append(rule)
        return rules

    def get_dependencies(self, key) -> list[str]:
        for rule in self.rules:
            if key == rule.name and rule.dependency:
                return rule.dependency
        return []

    def validate_all(self) -> bool:
        for rule in self.rules:
            if rule.exclusive:
                count = 0
                for ex in rule.exclusive:
                    count += self.values.get(ex)
                if count > 1:
                    raise Exception("Exclusive rule violated: " + str(rule))
            if rule.dependency:
                if self.values[rule.name]:
                    for dep in rule.dependency:
                        if not self.values.get(dep):
                            raise Exception("Dependent rule violated: " + str(rule))
        return True


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
            compiled.default[name] = True
            for f in feature:
                compiled.default[f] = True

        if name.startswith("exclusive-"):
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
            for f in feature:
                if f not in compiled.default:
                    compiled.default[f] = False

    compiled.values = copy.copy(compiled.default)
    return compiled
