#!/bin/bash
set -e
rm -rf t && mkdir t && cd t

corepack enable
corepack prepare pnpm@latest --activate
pnpm --version

pnpm init
pnpm add --save-dev @playwright/test
pnpm create playwright --browser=chromium --quiet --gha --lang=Typescript --install-deps
pnpm add --save-dev --save-exact typescript prettier
