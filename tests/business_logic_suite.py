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
A manager test harness test case suite that validates that
MyAssetManager behaves with the correct business logic.
"""

# pylint: disable=invalid-name, missing-function-docstring, missing-class-docstring

import operator
import os

from unittest import mock

from openassetio import Context, TraitsData
from openassetio.exceptions import PluginError
from openassetio.test.manager.harness import FixtureAugmentedTestCase


class Test_resolve(FixtureAugmentedTestCase):
    """
    Tests that resolution returns the expected values.
    """

    __test_entity = (
        "my_asset_manager:///anAsset",
        {
            "number": {"value": 42},
        },
    )

    def test_when_refs_found_then_success_callback_called_with_expected_values(self):
        ref_str = self.__test_entity[0]
        entity_reference = self._manager.createEntityReference(ref_str)

        trait_set = {"number"}
        context = self.createTestContext(access=Context.Access.kRead)

        result = [None]

        def success_cb(idx, traits_data):
            result[0] = traits_data
            print(result)

        def error_cb(idx, batchElementError):
            self.fail(
                f"Unexpected error for '{entity_reference.toString()}':"
                f" {batchElementError.message}"
            )

        self._manager.resolve([entity_reference], trait_set, context, success_cb, error_cb)

        self.assertTrue(len(result) == 1)
        # Check all traits are present, and their properties.
        for trait in self.__test_entity[1].keys():
            self.assertTrue(result[0].hasTrait(trait))
            for property_, value in self.__test_entity[1][trait].items():
                self.assertEqual(result[0].getTraitProperty(trait, property_), value)
