from .config import FeatureSet, compile_feature_set

# import yaml
import toml
import argparse
import os
from pathlib import Path
from .console import display


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default=".")
    args = parser.parse_args()
    file = args.file

    if os.path.isdir(file):
        file = os.path.join(file, "pacro_menu.toml")

    content = Path(file).read_text()
    config = toml.loads(content)
    feature_set = FeatureSet.parse_obj(config)
    selected = display(compile_feature_set(feature_set))


if __name__ == "__main__":
    main()
