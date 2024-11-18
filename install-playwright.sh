#!/bin/bash

usage() {
    echo "Usage: $0 [--npm-ct | --npm | --pnpm | --pnpm-ct]"
    echo "  --npm:     Install Playwright without component testing using npm"
    echo "  --npm-ct:  Install Playwright with component testing (--ct) using npm"
    echo "  --pnpm:    Install Playwright using pnpm without component testing"
    echo "  --pnpm-ct: Install Playwright using pnpm with component testing (--ct)"
    exit 1
}

# Check if an argument is provided
if [ $# -eq 0 ]; then
    usage
fi

# Common setup commands
setup_dir() {
    rm -rf t && mkdir t && cd t
}

# Common pnpm setup
setup_pnpm() {
    corepack enable
    corepack prepare pnpm@latest --activate
    pnpm --version
}

# Common dependencies installation
install_deps_npm() {
    npm install --save-dev --save-exact typescript prettier
}

install_deps_pnpm() {
    pnpm add --save-dev --save-exact typescript prettier
}

# Process arguments
case "$1" in
--npm-ct)
    setup_dir
    echo y | npm init playwright@latest -- --ct --browser=chromium --quiet --gha --lang=Typescript
    install_deps_npm
    ;;
--npm)
    setup_dir
    echo y | npm init playwright@latest -- --browser=chromium --quiet --gha --lang=Typescript
    install_deps_npm
    ;;
--pnpm)
    setup_dir
    setup_pnpm
    pnpm create playwright --browser=chromium --install-deps --quiet --gha --lang=Typescript
    install_deps_pnpm
    ;;
--pnpm-ct)
    setup_dir
    setup_pnpm
    pnpm create playwright --ct --browser=chromium --install-deps --quiet --gha --lang=Typescript
    install_deps_pnpm
    ;;
*)
    usage
    ;;
esac
