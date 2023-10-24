FROM kitware/trame:glvnd
COPY --chown=trame-user:trame-user .deploy-release/setup /deploy/setup
COPY --chown=trame-user:trame-user .deploy-release/server /deploy/server
COPY --chown=trame-user:trame-user . /app
RUN /opt/trame/entrypoint.sh build