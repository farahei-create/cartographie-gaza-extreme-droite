#!/usr/bin/env bash
# Reconstruit vendor/blob-upload.js à partir de @vercel/blob (version de package.json).
set -euo pipefail
cd "$(dirname "$0")/../.."
npm install --no-audit --no-fund
npx --yes esbuild@0.25.0 tools/contrib/blob-upload-entry.js --bundle --minify --format=iife --platform=browser --target=es2019 \
  --banner:js="/* @vercel/blob/client upload() — Apache-2.0, https://github.com/vercel/storage */" \
  --outfile=vendor/blob-upload.js
