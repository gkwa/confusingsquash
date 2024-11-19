#!/bin/bash
set -e
rm -rf t && mkdir t && cd t

npm init -y

echo y | npm init playwright@latest -- --browser=chromium --quiet --gha --lang=Typescript --install-deps
