
.. _contrib_and_license_header:

Contributing and License
========================

Contributing to the library
---------------------------

A bug you can fix? Improving documentation? Just wanna structure the code better? Every improvement matters.

Read this small guide to know how you can start contributing.

**If this is your first time contributing to an open source project, Welcome. You'd probably want to contribute to something you are confident about**

Setting Up the Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

May not be needed for documentation improvements.

Dependencies are listed in `requirements.txt <https://github.com/pssolanki111/polygon/blob/main/requirements.txt>`.
The list has ``sphinx`` and ``sphinx_rtd_theme`` which are only meant to build documentation.

It is highly recommended to install the dependencies in a virtual environment to avoid messing with your global interpreter.

.. code-block:: shell

  pip install virtualenv
  virtualenv venv
  . venv/bin/activate

The last instruction above is for *nix machines. For windows ``.\venv\Scripts\activate.bat`` (or similar) is used

Install the requirements using

.. code-block:: shell
  pip install -r requirements.txt

**Now you can make your changes**

Testing your changes
~~~~~~~~~~~~~~~~~~~~

Currently the project uses the actual endpoints to perform tests (Suggestions/PRs for better testing mechanism are welcome)

All test files are under directory ``tests``. You'd need a valid polygon API key to perform the tests as they are right now. If you don't have a
subscription, just make the changes, test them the way you like and raise the PR. I'll test the changes before merging.

However if you made changes to the documentation, run the below commands to build locally and test the documentation

.. code-block:: shell
  cd docs
  make html

The built docs would be placed under ``docs/_build/_html``. Open ``index.html`` here in a browser and see your changes. When you're happy with them, raise the PR.

Remember to document your changes like this library does already.

License
-------

Don't kid yourself. You don't care what license does the project use, do you? Anyways the project is licensed under
MIT License. See `License <https://github.com/pssolanki111/polygon/blob/main/LICENSE>`__ for more details.
