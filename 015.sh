#!/bin/bash
set -e
rm -rf t && mkdir t && cd t

corepack enable
corepack prepare pnpm@latest --activate
pnpm --version

pnpm init

pnpm create playwright --ct --browser=chromium --quiet --gha --lang=Typescript --install-deps