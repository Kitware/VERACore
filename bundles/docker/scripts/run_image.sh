#!/usr/bin/env bash

if [[ ! -v VERA_CORE_DATA_PATH ]]; then
  echo "VERA_CORE_DATA_PATH must be set to the data path!"
  exit 1
fi

set extra_args
tag="vera-core"

if [[ $VERA_CORE_DOCKER_USE_OSMESA == 1 ]]; then
  tag="vera-core:osmesa"
else
  extra_args=("--gpus" "all")
fi

docker run \
    -it \
    --rm \
    "${extra_args[@]}" \
    -v $VERA_CORE_DATA_PATH:/opt/vera-core/data.h5 \
    -p 8080:80 \
    $tag
