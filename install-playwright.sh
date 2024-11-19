#!/bin/bash
set -e

BROWSER_ARG="--browser=chromium"
COMMON_ARGS="$BROWSER_ARG --quiet --gha --lang=Typescript"
INSTALL_DEPS_ARG="--install-deps"
CT_ARG="--ct"

usage() {
    echo "Usage: $0 [--npm-ct | --npm | --pnpm | --pnpm-ct] [--no-deps]"
    echo "  --npm:     Install Playwright without component testing using npm"
    echo "  --npm-ct:  Install Playwright with component testing (--ct) using npm"
    echo "  --pnpm:    Install Playwright using pnpm without component testing"
    echo "  --pnpm-ct: Install Playwright using pnpm with component testing (--ct)"
    echo "  --no-deps: Skip installing dependencies"
    exit 1
}

if [ $# -eq 0 ]; then
    usage
fi

INSTALL_METHOD=""
SKIP_DEPS=false

while [[ $# -gt 0 ]]; do
    case $1 in
    --npm | --npm-ct | --pnpm | --pnpm-ct) INSTALL_METHOD="$1" ;;
    --no-deps) SKIP_DEPS=true ;;
    *) usage ;;
    esac
    shift
done

if [ -z "$INSTALL_METHOD" ]; then
    usage
fi

setup_dir() {
    rm -rf t && mkdir t && cd t
}

setup_pnpm() {
    corepack enable
    corepack prepare pnpm@latest --activate
    pnpm --version
}

install_deps_npm() {
    if [ "$SKIP_DEPS" = false ]; then
        npm install --save-dev --save-exact typescript prettier
    fi
}

install_deps_pnpm() {
    if [ "$SKIP_DEPS" = false ]; then
        pnpm add --save-dev --save-exact typescript prettier
    fi
}

get_install_deps_arg() {
    if [ "$SKIP_DEPS" = false ]; then
        echo "$INSTALL_DEPS_ARG"
    fi
}

case "$INSTALL_METHOD" in
--npm)
    setup_dir
    npm init -y
    npm install --save-dev @playwright/test
    echo y | npm init playwright@latest -- $COMMON_ARGS $(get_install_deps_arg)
    install_deps_npm
    ;;
--npm-ct)
    setup_dir
    npm init -y
    npm install --save-dev @playwright/test
    echo y | npm init playwright@latest -- $CT_ARG $COMMON_ARGS $(get_install_deps_arg)
    install_deps_npm
    ;;
--pnpm)
    setup_dir
    setup_pnpm
    pnpm init
    pnpm add --save-dev @playwright/test
    pnpm create playwright $COMMON_ARGS $(get_install_deps_arg)
    install_deps_pnpm
    ;;
--pnpm-ct)
    setup_dir
    setup_pnpm
    pnpm init
    pnpm add --save-dev @playwright/test
    pnpm create playwright $CT_ARG $COMMON_ARGS $(get_install_deps_arg)
    install_deps_pnpm
    ;;
*)
    usage
    ;;
esac
