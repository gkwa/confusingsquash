#!/usr/bin/env python3

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

for i, combo in enumerate(test_combinations):
    filename = f"{i:03d}.sh"

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

    with open(filename, "w") as f:
        f.write(content.strip())

print("Generated scripts:")
for i in range(len(test_combinations)):
    print(f"{i:03d}.sh")
