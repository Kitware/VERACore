#!/usr/bin/env bash
CURRENT_DIR=`dirname "$0"`

if [[ $VERA_CORE_DOCKER_USE_OSMESA == 1 ]]; then
  docker_image=kitware/trame
else
  docker_image=kitware/trame:glvnd
fi

# Since Mac doesn't come with realpath by default, let's set the full
# paths using PWD.
pushd . > /dev/null
cd $CURRENT_DIR/..
DEPLOY_DIR=$PWD
cd $CURRENT_DIR/../../..
ROOT_DIR=$PWD
popd > /dev/null

docker run --rm          \
    -e TRAME_BUILD_ONLY=1 \
    -v "$DEPLOY_DIR:/deploy" \
    -v "$ROOT_DIR:/local-app"  \
    $docker_image
