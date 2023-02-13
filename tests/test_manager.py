#
#   Copyright 2013-2023 The Foundry Visionmongers Ltd
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
"""
Test cases for MyAssetManager that make use of the OpenAssetIO
manager test harness.
Note that this file simply wraps the openassetio.test.manager harness in
a pytest test, so that it can be run as part of the project test suite.
It also serves as an example of how to programmatically execute the test
harness, by extending it with additional checks for MyManagerPlugins
specific business logic.
It is not required in order to make use of the test harness. The base
API compliance tests can simply be run from a command line with
openassetio available, and the target plugin on
$OPENASSETIO_PLUGIN_PATH:
  python -m openassetio.test.manager -f path/to/fixtures.py
"""

import os
import pytest

# pylint: disable=invalid-name,redefined-outer-name
# pylint: disable=missing-class-docstring,missing-function-docstring

from openassetio.test.manager import harness, apiComplianceSuite
from openassetio.pluginSystem import PythonPluginSystemManagerPlugin


#
# Tests
#

# MyAssetManager exposes an entry point, so can be pip installed without
# need to extend OPENASSETIO_PLUGIN_PATH.
# Tests should be invoked from an install
#
#   python -m pip install .
#   python -m pip install -r tests/requirements.txt
#   python -m pytest tests


class Test_MyAssetManager:
    def test_passes_apiComplianceSuite(self, harness_fixtures):
        assert harness.executeSuite(apiComplianceSuite, harness_fixtures)

    def test_passes_my_asset_manager_business_logic_suite(
        self, my_asset_manager_business_logic_suite, harness_fixtures
    ):
        assert harness.executeSuite(my_asset_manager_business_logic_suite, harness_fixtures)


class Test_MyAssetManager_Plugin:  # pylint: disable=too-few-public-methods
    def test_exposes_plugin_attribute_with_correct_type(self):
        import my_asset_manager  # pylint: disable=import-outside-toplevel

        assert issubclass(my_asset_manager.plugin, PythonPluginSystemManagerPlugin)


@pytest.fixture
def my_asset_manager_business_logic_suite(base_dir):
    module_path = os.path.join(base_dir, "tests", "business_logic_suite.py")
    return harness.moduleFromFile(module_path)