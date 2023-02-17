# Template-OpenAssetIO-Manager-Python

An [OpenAssetIO](https://github.com/OpenAssetIO/OpenAssetIO) Python
manager plugin template.

This template has been written so that it works "out of the box",
including test and lint infrastructure, integrated with github actions.

## Using the template

### Manager Name

Once you have cloned the repository, you'll want to rename the template.
The template uses placeholder strings, (eg: "MyAssetManager") throughout
to facilitate easy replacement.

Firstly, rename the directory

```bash
plugins/my_asset_manager
```

 and the file at

```bash
plugins/my_asset_manager/MyAssetManagerInterface.py
```

substituting in the name of your asset manager in the appropriate style.

Then, run a global find and replace across the project file contents to
replace the following strings with the name of your asset manager, in
the matching styles.

```bash
MyAssetManager
my_asset_manager
My Asset Manager
```

Finally, also globally replace the string

```bash
myorg
```

with the name of your organization.

> **Note**
>
> `myorg` is the first item in a reverse-dns identifier string, See the
> `identifier()` methods in
> [`__init__.py`](plugin/my_asset_manager/__init__.py) and
> [`MyAssetManagerInterface.py`](plugin/my_asset_manager/AssetManagerInferface.py)

### Install and Test

You should then be able to install the asset manager into you Python
environment. From the project root.

```shell
python -m pip install .
```

and invoke the included tests

```shell
python -m pip install -r tests/requirements.txt
python -m pytest ./tests
```

### Using the manager with a host

The manager is setup for entry point based plugin discovery. This means
that it needs only be installed into your Python environment, and then
an `OpenAssetIO` host can load it automatically, simply via configuring
to the [manager identifier](plugin/my_asset_manager/__init__.py#L35),
(usually by using a [default config
file.](https://openassetio.github.io/OpenAssetIO/glossary.html#default_config_var))

Alternatively, you can avoid installing the plugin by adding the
`plugin` directory to the `$OPENASSETIO_PLUGIN_PATH` environment
variable.

## Project walkthrough

```
.
├── .github
|   ├── workflows
|       ├── code-quality.yml
|       ├── test.yml
|       ├── build-wheels.yml
|       └── deploy-pypi.yml
├── plugin
│   ├── my_asset_manager
│       ├── MyAssetManagerInterface.py
│       └── __init__.py
├── pyproject.toml
└── tests
    ├── business_logic_suite.py
    ├── conftest.py
    ├── fixtures.py
    ├── requirements.txt
    └── test_apiCompliance.py
```

### .github

This folder contains github actions scripts.
These are configured to run on each pull-request.

- [`code-quality.yml`](.github/workflows/code-quality.yml): Runs pylint
and black linters.
- [`test.yml`](.github/workflows/test.yml): Installs the manager and
invokes pytest.
- [`build-wheels.yml`](.github/workflows/build-wheels.yml): When a new
commit is pushed to main, builds wheels for distribution.
- [`deploy-pypi.yml`](.github/workflows/deploy-pypi.yml): When a new
release is made, deploys wheels to PyPI.

### plugin

Source directory for the asset manager

- [`MyAssetManagerInterface.py`](plugin/my_asset_manager/AssetManagerInferface.py):
Manager interface implementation. Implements methods such as `resolve`
from the `OpenAssetIO` manager interface. This is the place to go to
start implementing your manager logic.
- [`__init__.py`](plugin/my_asset_manager/__init__.py)  The manager
module itself. Boilerplate responsible for exposing the asset manager
interface and manager identifier to `OpenAssetIO`

### pyproject.toml

Python project configuration. Allows the manager to be `pip install`'ed,
as well as setting linter configuration settings.

### tests

Test directory, assumes a `pytest` testing environment. Uses the
[OpenAssetIO test
harness](https://openassetio.github.io/OpenAssetIO/testing.html#testing_manager_plugins)
to run apiCompliance checks, as well as business logic tests.

- [`business_logic_suite.py`](test/business_logic_suite.py): Tests for
the behaviour of the manager. Does it resolve assets correctly, etc.
Invoked from `tests.py`
- [`conftest.py`](test/conftest.py): Pytest fixtures necessary for
  running the tests.
- [`fixtures.py`](test/fixtures.py): Data concerning the manager
necessary to run the test harness. See [the
documentation.](https://openassetio.github.io/OpenAssetIO/testing.html#testing_manager_plugins_fixtures)
- [`requirements.txt`](test/requirements.txt): Requirements necessary to
run the tests. Generally installed with `python -m pip install -r
tests/requirements.txt` from the root directory.
- [`tests.py`](test/tests.py): Main test entry point. Executes the
 manager `business_logic_suite`, as well as [OpenAssetIOs
 apiComplianceSuite.](https://github.com/OpenAssetIO/OpenAssetIO/blob/main/src/openassetio-python/package/openassetio/test/manager/apiComplianceSuite.py)

### Releases

The repository is setup to use the [OpenAssetIO release process](https://github.com/OpenAssetIO/OpenAssetIO/blob/main/doc/contributing/PROCESS.md#release-process.)

Note that for the PyPI deploy to work correctly, you will have to create
a project on testPyPI and PyPI, and then add `TEST_PYPI_ACCESS_TOKEN`
and `PYPI_ACCESS_TOKEN` to the repository as secrets. As each release
is unique, the project does not come pre configured with these access
tokens.
