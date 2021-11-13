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
    files = []
    if os.path.isdir(file):
        files.append(os.path.join(file, "pacro_menu.toml"))
        files.append(os.path.join(file, "Cargo.toml"))
    else:
        files.append(file)
    for file in files:
        try:
            content = Path(file).read_text()
            config = toml.loads(content)
            if 'features' in content:
                config = config['features']
            feature_set = FeatureSet.parse_obj(config)
            break
        except FileNotFoundError:
            pass
    else:
        print('Could not open file', files)
        exit(-1)
    compiled = compile_feature_set(feature_set)
    display(compiled)

    enabled = []
    for key, value in compiled.values.items():
        if value is True:
            enabled.append(key)
    print(','.join(enabled))


if __name__ == "__main__":
    main()
