# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2023 The Foundry Visionmongers Ltd

"""
Manager test harness test case fixtures for My Asset Manager.
"""
from openassetio import constants
from openassetio_mediacreation.traits.content import LocatableContentTrait
from openassetio_mediacreation.traits.application import ConfigTrait
from openassetio_mediacreation.traits.usage import EntityTrait

IDENTIFIER = "myorg.manager.my_asset_manager"

VALID_REF = "my_asset_manager:///AssetIdentifier"
NON_REF = "not a Ŕeference"
MALFORMED_REF = "my_asset_manager:///AssetIdentifier?unsupportedQueryParam"
EXISTING_REF = "my_asset_manager:///anAsset"
MISSING_ENTITY_REF = "my_asset_manager:///missing_entity"
ERROR_MSG_MALFORMED_REF = "Entity identifier is malformed"
ERROR_MSG_MISSING_ENTITY = "Entity 'my_asset_manager:///missing_entity' not found"
ERROR_READ_ONLY_ACCESS = "Entities are read-only"

# This dictionary serves as expected outputs for the OpenAssetIO api
# compliance suite. This suite tests that your implementation functions
# as expected as far as integrating structurally into OpenAssetIO is
# concerned, (eg, are the correct callbacks being called, are errors
# being emitted when they should be, etc.)
fixtures = {
    "identifier": IDENTIFIER,
    "shared": {
        "a_valid_reference": VALID_REF,
        "an_invalid_reference": NON_REF,
    },
    "Test_identifier": {"test_matches_fixture": {"identifier": IDENTIFIER}},
    "Test_displayName": {"test_matches_fixture": {"display_name": "My Asset Manager"}},
    "Test_info": {
        "test_matches_fixture": {
            "info": {constants.kInfoKey_EntityReferencesMatchPrefix: "my_asset_manager:///"}
        }
    },
    "Test_resolve": {
        "shared": {
            "a_reference_to_a_readable_entity": EXISTING_REF,
            "a_set_of_valid_traits": {LocatableContentTrait.kId},
            "a_reference_to_a_readonly_entity": EXISTING_REF,
            "the_error_string_for_a_reference_to_a_readonly_entity": "Entities are read-only",
            "a_reference_to_a_missing_entity": MISSING_ENTITY_REF,
            "the_error_string_for_a_reference_to_a_missing_entity": (
                "Entity 'my_asset_manager:///missing_entity' not found"
            ),
            "a_malformed_reference": MALFORMED_REF,
            "the_error_string_for_a_malformed_reference": "Entity identifier is malformed",
        }
    },
    "Test_entityTraits": {
        "shared": {
            "a_reference_to_a_readonly_entity": EXISTING_REF,
            "a_reference_to_a_missing_entity": MISSING_ENTITY_REF,
            "a_malformed_reference": MALFORMED_REF,
        },
        "test_when_querying_malformed_reference_then_malformed_reference_error_is_returned": {
            "expected_error_message": ERROR_MSG_MALFORMED_REF,
        },
        "test_when_querying_missing_reference_for_read_then_resolution_error_is_returned": {
            "expected_error_message": ERROR_MSG_MISSING_ENTITY
        },
        "test_when_read_only_entity_queried_for_write_then_access_error_is_returned": {
            "expected_error_message": ERROR_READ_ONLY_ACCESS
        },
        "test_when_multiple_references_for_read_then_same_number_of_returned_trait_sets": {
            "first_entity_reference": "my_asset_manager:///anAsset",
            "second_entity_reference": "my_asset_manager:///anAsset2",
            "first_entity_trait_set": {
                EntityTrait.kId,
                LocatableContentTrait.kId,
            },
            "second_entity_trait_set": {
                EntityTrait.kId,
                LocatableContentTrait.kId,
                ConfigTrait.kId,
            },
        },
    },
}
