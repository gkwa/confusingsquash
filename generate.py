#!/usr/bin/env python3

package_managers = ['npm', 'npm-ct', 'pnpm', 'pnpm-ct']
deps_options = ['deps', 'no-deps']

script_template = '''#!/bin/bash
set -e
rm -rf t && mkdir t && cd t

{pm_setup}

{init_commands}

{deps_installation}
'''

pm_setups = {
    'npm': '',
    'npm-ct': '',
    'pnpm': '''corepack enable
corepack prepare pnpm@latest --activate
pnpm --version''',
    'pnpm-ct': '''corepack enable
corepack prepare pnpm@latest --activate
pnpm --version'''
}

init_commands = {
    'npm': '''npm init -y
npm install --save-dev @playwright/test
echo y | npm init playwright@latest -- --browser=chromium --quiet --gha --lang=Typescript --install-deps''',
    'npm-ct': '''npm init -y
npm install --save-dev @playwright/test
echo y | npm init playwright@latest -- --ct --browser=chromium --quiet --gha --lang=Typescript --install-deps''',
    'pnpm': '''pnpm init
pnpm add --save-dev @playwright/test
pnpm create playwright --browser=chromium --quiet --gha --lang=Typescript --install-deps''',
    'pnpm-ct': '''pnpm init
pnpm add --save-dev @playwright/test
pnpm create playwright --ct --browser=chromium --quiet --gha --lang=Typescript --install-deps'''
}

deps_installations = {
    'deps': {
        'npm': 'npm install --save-dev --save-exact typescript prettier',
        'npm-ct': 'npm install --save-dev --save-exact typescript prettier',
        'pnpm': 'pnpm add --save-dev --save-exact typescript prettier',
        'pnpm-ct': 'pnpm add --save-dev --save-exact typescript prettier'
    },
    'no-deps': {
        'npm': '',
        'npm-ct': '',
        'pnpm': '',
        'pnpm-ct': ''
    }
}

for pm in package_managers:
    for deps in deps_options:
        filename = f"install-playwright-{pm}-{deps}.sh"
        content = script_template.format(
            pm_setup=pm_setups[pm],
            init_commands=init_commands[pm],
            deps_installation=deps_installations[deps][pm]
        )
        
        with open(filename, 'w') as f:
            f.write(content.strip())

print("Generated scripts:")
for pm in package_managers:
    for deps in deps_options:
        print(f"install-playwright-{pm}-{deps}.sh")
