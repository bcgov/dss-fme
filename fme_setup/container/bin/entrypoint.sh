#!/bin/bash

# this option causes the script to exit immediatly upon error
set -o errexit

readonly REQUIRED_ENV_VARS=(
	"FME_LICENSING_SERVER"
	"FME_EDITION_NAME")


for evar in ${REQUIRED_ENV_VARS[@]}; do
  if [[ -z "${!evar}" ]]; then
    echo "Error: The env var '$evar' must be set."
    exit 1
  fi
done

./fmelicensingassistant --floating $FME_LICENSING_SERVER $FME_EDITION_NAME
echo "Floating license set successfully."

exec "$@"
