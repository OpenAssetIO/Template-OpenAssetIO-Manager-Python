# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2023 The Foundry Visionmongers Ltd

"""
A manager test harness test case suite that validates that
MyAssetManager behaves with the correct business logic.
"""

# pylint: disable=invalid-name, missing-function-docstring, missing-class-docstring

from openassetio.access import ResolveAccess, EntityTraitsAccess
from openassetio.test.manager.harness import FixtureAugmentedTestCase
from openassetio_mediacreation.traits.content import LocatableContentTrait
from openassetio_mediacreation.traits.usage import EntityTrait


class Test_resolve(FixtureAugmentedTestCase):
    """
    Test suite for the Resolve business logic of MyAssetManager

    The test here is illustrative only, you should extend this suite
    to provide full coverage of all of the behaviour of your asset
    manager.
    """

    __test_entity = (
        "my_asset_manager:///anAsset",
        {
            LocatableContentTrait.kId: {"location": "file:///some/filesystem/path"},
        },
    )

    def test_when_refs_found_then_success_callback_called_with_expected_values(self):
        ref_str = self.__test_entity[0]
        entity_reference = self._manager.createEntityReference(ref_str)

        trait_set = {LocatableContentTrait.kId}
        context = self.createTestContext()

        result = [None]

        def success_cb(idx, traits_data):
            result[0] = traits_data

        def error_cb(idx, batchElementError):
            self.fail(
                f"Unexpected error for '{entity_reference.toString()}':"
                f" {batchElementError.message}"
            )

        self._manager.resolve(
            [entity_reference], trait_set, ResolveAccess.kRead, context, success_cb, error_cb
        )

        self.assertTrue(len(result) == 1)
        # Check all traits are present, and their properties.
        for trait in self.__test_entity[1]:
            self.assertTrue(result[0].hasTrait(trait))
            for property_, value in self.__test_entity[1][trait].items():
                self.assertEqual(result[0].getTraitProperty(trait, property_), value)


class Test_entityTraits(FixtureAugmentedTestCase):
    """
    Test suite for the EntityTraits business logic of MyAssetManager

    The test here is illustrative only, you should extend this suite
    to provide full coverage of all of the behaviour of your asset
    manager.
    """

    def test_when_refs_found_then_success_callback_called_with_expected_values(self):
        entity_reference = self._manager.createEntityReference("my_asset_manager:///anAsset")

        context = self.createTestContext()

        results = [None]

        def success_cb(idx, trait_set):
            print("Success", trait_set)
            results[idx] = trait_set

        def error_cb(idx, batchElementError):
            self.fail(
                f"Unexpected error for '{entity_reference.toString()}':"
                f" {batchElementError.message}"
            )

        self._manager.entityTraits(
            [entity_reference], EntityTraitsAccess.kRead, context, success_cb, error_cb
        )

        self.assertTrue(len(results) == 1)
        expected_trait_set = {EntityTrait.kId, LocatableContentTrait.kId}
        assert results[0] == expected_trait_set
