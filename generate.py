#!/usr/bin/env python3
import stat, pathlib
import json

test_combinations = [
    {"pm": "npm", "ct": False, "deps": True, "playwright_deps": True},
    {"pm": "npm", "ct": False, "deps": True, "playwright_deps": False},
    {"pm": "npm", "ct": False, "deps": False, "playwright_deps": True},
    {"pm": "npm", "ct": False, "deps": False, "playwright_deps": False},
    {"pm": "npm", "ct": True, "deps": True, "playwright_deps": True},
    {"pm": "npm", "ct": True, "deps": True, "playwright_deps": False},
    {"pm": "npm", "ct": True, "deps": False, "playwright_deps": True},
    {"pm": "npm", "ct": True, "deps": False, "playwright_deps": False},
    {"pm": "pnpm", "ct": False, "deps": True, "playwright_deps": True},
    {"pm": "pnpm", "ct": False, "deps": True, "playwright_deps": False},
    {"pm": "pnpm", "ct": False, "deps": False, "playwright_deps": True},
    {"pm": "pnpm", "ct": False, "deps": False, "playwright_deps": False},
    {"pm": "pnpm", "ct": True, "deps": True, "playwright_deps": True},
    {"pm": "pnpm", "ct": True, "deps": True, "playwright_deps": False},
    {"pm": "pnpm", "ct": True, "deps": False, "playwright_deps": True},
    {"pm": "pnpm", "ct": True, "deps": False, "playwright_deps": False},
]

pm_setups = {
    "npm": "",
    "pnpm": """corepack enable
corepack prepare pnpm@latest --activate
pnpm --version""",
}

script_template = """#!/bin/bash
set -e
rm -rf t && mkdir t && cd t

{pm_setup}

{init}
{playwright_deps}
{playwright_init}
{deps}
"""

ci_template = """name: Build & Test
"on":
  push:
    branches:
      - "*"
  pull_request:
    branches:
      - "*"
  schedule:
    - cron: 01 13 * * SAT
jobs:
  build:
    name: Build & Test
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest]
        script: {scripts}
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@cbb722410c2e876e24abbe8de2cc27693e501dcb
      - name: Setup Node.js
        uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af
        with:
          node-version: 20
      - name: Run Installation
        run: ./${{ matrix.script }}
      - name: List Installation Results
        run: |
          set -x
          cd t
          ls -la
          cat package.json
          [[ -f "playwright.config.ts" ]] && cat playwright.config.ts || true
          [[ -f "tsconfig.json" ]] && cat tsconfig.json || true"""

# Generate shell scripts
for i, combo in enumerate(test_combinations):
    script_path = pathlib.Path(f"{i:03d}.sh")

    init = f"{combo['pm']} init -y" if combo["pm"] == "npm" else "pnpm init"

    playwright_deps = ""
    if combo["playwright_deps"]:
        if combo["pm"] == "npm":
            playwright_deps = "npm install --save-dev --save-exact @playwright/test"
        else:
            playwright_deps = "pnpm add --save-dev --save-exact @playwright/test"

    ct_flag = " --ct" if combo["ct"] else ""

    if combo["pm"] == "npm":
        playwright_init = f"echo y | npm init playwright@latest --{ct_flag} --browser=chromium --quiet --gha --lang=Typescript --install-deps"
    else:
        playwright_init = f"pnpm create playwright{ct_flag} --browser=chromium --quiet --gha --lang=Typescript --install-deps"

    deps = ""
    if combo["deps"]:
        if combo["pm"] == "npm":
            deps = "npm install --save-dev --save-exact typescript prettier"
        else:
            deps = "pnpm add --save-dev --save-exact typescript prettier"

    content = script_template.format(
        pm_setup=pm_setups[combo["pm"]],
        init=init,
        playwright_deps=playwright_deps,
        playwright_init=playwright_init,
        deps=deps,
    )

    script_path.write_text(content.strip())
    script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)

# Generate ci.yml
scripts = [f"{i:03d}.sh" for i in range(len(test_combinations))]
scripts_yaml = json.dumps(scripts)
ci_content = ci_template.format(scripts=scripts_yaml)

workflows_dir = pathlib.Path(".github/workflows")
workflows_dir.mkdir(parents=True, exist_ok=True)
workflows_dir.joinpath("ci.yml").write_text(ci_content)

print("Generated scripts:")
for i in range(len(test_combinations)):
    print(f"{i:03d}.sh")
print("\nGenerated .github/workflows/ci.yml")
