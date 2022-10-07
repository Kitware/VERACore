VERACore
========================================

VERACore is a Python application for visualization and engineering analyses of output data from VERA (Virtual Environment for Reactor Applications).
Implemented in Python, it provides instantaneous 2D and 3D images, 1D plots, and alphanumeric data from VERA multi-physics simulations.

Installing
----------------------------------------

VERACore can be installed via pip and can run locally or deployed as a service.
To use it locally within a virtual environment, you can run the following commands:

.. code-block:: console

    python3 -m venv ./vera-env
    source ./vera-env/bin/activate
    pip install -U pip
    pip install vera-core

    vera-core --data <path-to-vera-out-file>


Development
----------------------------------------

Setup a virtual environment with a modern Python 3.

.. code-block:: console

    python3 -m venv ./vera-env
    source ./vera-env/bin/activate
    pip install -U pip

Get the code base and build its widgets

.. code-block:: console

    git clone git@github.com:Kitware/VERACore.git
    cd VERACore

    # Build the custom UI widgets
    cd vue-components
    npm i
    npm run build
    cd ..

    # Install local repository into your venv
    pip install -e .

Run the application to test out your changes


.. code-block:: console

    vera-core --server

Licensing
----------------------------------------

VERACore is provided as an open source solution and follows the `Apache Software License <https://github.com/Kitware/VERACore/blob/master/LICENSE>`_
