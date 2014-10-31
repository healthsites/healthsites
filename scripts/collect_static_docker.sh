#!/bin/bash
source ${BASH_SOURCE%/*}/functions.sh
manage collectstatic --noinput
