#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ENV_FILE=$SCRIPT_DIR/.env

# ======================================================================================================================

# The environment vairables below will be written
# to the .env file in the directory along with this script.

# Please keep environment variables in the current script
# alphabetically sorted and use double quotes around the values.

# You can read more why we need to use quotes here:
# https://stackoverflow.com/a/71538763/8431075

cat > $ENV_FILE << EOF
BUILDX_CACHE_DEST="/tmp/.buildx-cache-new"
BUILDX_CACHE_SRC="/tmp/.buildx-cache"
EOF

# ======================================================================================================================

cat << EOF

Default environment variables has been written to:
$ENV_FILE

This setup should just work fine right out of the box,
but you can adjust this file in the way you want.

EOF
