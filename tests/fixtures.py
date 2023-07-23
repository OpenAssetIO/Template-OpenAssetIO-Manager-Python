"""
Manager test harness test case fixtures for My Asset Manager.
"""
from openassetio import constants
from openassetio_mediacreation.traits.content import LocatableContentTrait


IDENTIFIER = "myorg.manager.my_asset_manager"

VALID_REF = "my_asset_manager:///AssetIdentifier"
NON_REF = "not a Ŕeference"
MALFORMED_REF = "my_asset_manager:///AssetIdentifier?unsupportedQueryParam"
EXISTING_REF = "my_asset_manager:///anAsset"

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
            "info": {constants.kField_EntityReferencesMatchPrefix: "my_asset_manager:///"}
        }
    },
    "Test_resolve": {
        "a_reference_to_a_readable_entity": EXISTING_REF,
        "a_set_of_valid_traits": {LocatableContentTrait.kId},
        "a_reference_to_a_readonly_entity": EXISTING_REF,
        "the_error_string_for_a_reference_to_a_readonly_entity": "Entities are read-only",
        "a_reference_to_a_missing_entity": "my_asset_manager:///missing_entity",
        "the_error_string_for_a_reference_to_a_missing_entity": (
            "Entity 'my_asset_manager:///missing_entity' not found"
        ),
        "a_malformed_reference": MALFORMED_REF,
        "the_error_string_for_a_malformed_reference": "Entity identifier is malformed",
    },
}
