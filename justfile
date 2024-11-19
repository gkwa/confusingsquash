set shell := ["bash", "-uec"]

default:
    @just --list

fmt:
    shfmt -w -s -i 4 *.sh
    prettier --ignore-path=.prettierignore --config=.prettierrc.json --write .
    ruff format .
    just --unstable --fmt
