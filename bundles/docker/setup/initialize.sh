# Install app from local directory
# Skip dependencies, since we don't want h5py or vtk
# (they will clash with the ones in paraview)
# Instead, we specify all dependencies in the install_requirements.txt file

# You can install it locally, but make sure the vue components are built
pip install --no-deps /local-app

# Alternatively, it can be installed from PyPI
# pip install --no-deps vera-core
