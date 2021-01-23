#!/usr/bin/env bash


set -eu
set -o pipefail


cd "$(dirname "$0")" || exit 1


java -cp languagetool-server.jar org.languagetool.server.HTTPServer -- --port 8080 --public --allow-origin '*' "$@"
