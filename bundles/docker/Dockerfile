ARG BASE_IMAGE=kitware/trame:glvnd
FROM ${BASE_IMAGE}

# Install ParaView-EGL
ARG PV_URL=https://www.paraview.org/files/v5.11/ParaView-5.11.0-egl-MPI-Linux-Python3.9-x86_64.tar.gz

RUN mkdir -p /opt/paraview && cd /opt/paraview && wget -qO- $PV_URL | tar --strip-components=1 -xzv
ENV TRAME_PARAVIEW=/opt/paraview

# Copy the server directory
COPY --chown=trame-user:trame-user ./server /deploy/server
