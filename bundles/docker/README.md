## Building the VERACore docker image (Linux only)

```bash
./scripts/build_image.sh
```

## Running the bundle

`./scripts/run_image.sh` and open your browser to `http://localhost:8080/`.

## Building OSMesa

The default is to build the EGL version of the docker image.

If you wish to build the OSMesa version, set this environment variable before
running the scripts:

```bash
export VERA_CORE_DOCKER_USE_OSMESA=1
```
