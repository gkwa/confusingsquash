#!/bin/bash
set -e
rm -rf t && mkdir t && cd t



npm init -y
npm install --save-dev @playwright/test
echo y | npm init playwright@latest -- --ct --browser=chromium --quiet --gha --lang=Typescript --install-deps