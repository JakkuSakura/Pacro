# Pacro
Pacro aims to be a language agnostic preprocess tool/macro system.

## Feature selection
One part is feature selection Just like Kconfig in linux kernel code

## Dirty macro

The macro works in the following steps:

1. Read through files, and check if any file contains `// @`
2. Convert the files into jinja template
3. Import an environment for jinja to work
4. Render jinja template


# Ship
Ship is a Rust cargo preprocessor. It can 
1) hook up libraries as they are in crates.io
2) execute all prebuild.sh in sub directories

To use, rename Cargo.toml for workspaces to workspace.toml. You can write the following as exclude.toml

```toml
crate1 = true
```