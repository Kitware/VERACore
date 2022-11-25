#!/usr/bin/env bash
CURRENT_DIR=`dirname "$0"`

# Since Mac doesn't come with realpath by default, let's set the full
# paths using PWD.
pushd . > /dev/null
cd $CURRENT_DIR/..
DEPLOY_DIR=$PWD
popd > /dev/null

if [[ ! -v VERA_CORE_DATA_PATH ]]; then
  echo "VERA_CORE_DATA_PATH must be set to the data path!"
  exit 1
fi

if [[ ! -v TRAME_PARAVIEW ]]; then
  echo "TRAME_PARAVIEW must be set to the path to ParaView!"
  exit 1
fi

set extra_args
if [[ $VERA_CORE_DOCKER_USE_OSMESA == 1 ]]; then
  docker_image=kitware/trame
else
  docker_image=kitware/trame:glvnd
  extra_args=("--gpus" "all")
fi

docker run \
    -it \
    --rm \
    "${extra_args[@]}" \
    -p 8080:80 \
    -e TRAME_PARAVIEW=/opt/paraview \
    -v "$TRAME_PARAVIEW:/opt/paraview" \
    -v "$DEPLOY_DIR:/deploy" \
    -v $VERA_CORE_DATA_PATH:/opt/vera-core/data.h5 \
    $docker_image
