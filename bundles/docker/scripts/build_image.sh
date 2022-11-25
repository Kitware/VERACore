#!/usr/bin/env bash
CURRENT_DIR=`dirname "$0"`

. $CURRENT_DIR/build_server.sh

tag="vera-core"

set extra_args
if [[ $VERA_CORE_DOCKER_USE_OSMESA == 1 ]]; then
  extra_args=("--build-arg" "BASE_IMAGE=kitware/trame" "--build-arg" "PV_URL=https://www.paraview.org/files/v5.11/ParaView-5.11.0-osmesa-MPI-Linux-Python3.9-x86_64.tar.gz")
  tag="vera-core:osmesa"
fi

cd $CURRENT_DIR/..
docker build -t $tag "${extra_args[@]}" .
cd -
