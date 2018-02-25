opticam-dbx
===========

A tool for downloading Opticam surveillance camera videos from Dropbox.

Development
===========

.. code:: sh

    python -m venv venv
    venv/bin/python setup.py develop

Install
=======

.. code:: sh

    pip install opticam-dbx


Usage
=====

See `opticam-dbx --help` for all options.

.. code:: sh

    # Set the Dropbox token to be used via environment variable
    # See https://github.com/dropbox/dropbox-sdk-python
    export OPTICAM_DBX_TOKEN=...

    # Note that you can pass --env-file=path/to/env_file to
    # opticam-dbx and environment variables are read from
    # that file

    opticam-dbx --dest=videos/ --remove-downloaded
