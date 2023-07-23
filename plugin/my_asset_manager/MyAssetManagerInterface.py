# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2023 The Foundry Visionmongers Ltd

# pylint: disable=invalid-name
"""
A single-class module, providing the MyAssetManagerInterface class.
This is the entry-point for the logic of your asset manager.
"""

# Note that it should always be light-weight to construct instances of
# the this class. See the notes under the "Initialization" section of:
# https://openassetio.github.io/OpenAssetIO/classopenassetio_1_1v1_1_1manager_api_1_1_manager_interface.html#details (pylint: disable=line-too-long)
# As such, any expensive module imports should be deferred.
from openassetio import constants, BatchElementError, TraitsData
from openassetio.managerApi import ManagerInterface
from openassetio_mediacreation.traits.content import LocatableContentTrait
from openassetio_mediacreation.traits.managementPolicy import ManagedTrait

# OpenAssetIO is building out the implementation vertically, there are
# known fails for missing abstract methods.
# pylint: disable=abstract-method
# Methods in C++ end up with "missing docstring"
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments, unused-argument


class MyAssetManagerInterface(ManagerInterface):
    """
    Implement the OpenAssetIO ManagerInterface.
    https://openassetio.github.io/OpenAssetIO/classopenassetio_1_1manager_api_1_1_manager_interface_1_1_manager_interface.html
    """

    # Entity references provided to this asset manager should be
    # prefixed with this string to be considered valid.
    # eg. "my_asset_manager:///my_entity_id"
    __reference_prefix = "my_asset_manager:///"

    def identifier(self):
        return "myorg.manager.my_asset_manager"

    def initialize(self, managerSettings, hostSession):
        # Do any necessary heavy initialization here, allowing for the
        # manager to be constructed quickly in situations where full
        # initialization would be unnecessary and undesirable. See :
        # https://openassetio.github.io/OpenAssetIO/classopenassetio_1_1v1_1_1host_api_1_1_manager.html#aa52c7436ff63ae96e33d7db8d6fd38df
        print(managerSettings)
        if managerSettings != {}:
            raise KeyError(
                "MyAssetManager should take no settings, but managerSettings is not empty"
            )

    def displayName(self):
        return "My Asset Manager"

    def info(self):
        # This hint allows the API middleware to short-circuit calls to
        # `isEntityReferenceString` using string prefix comparisons. If
        # your implementation's entity reference format supports this
        # kind of matching, you should set this key. It allows for
        # multi-threaded reference testing in C++ as it avoids the need
        # to acquire the GIL and enter Python.
        return {constants.kField_EntityReferencesMatchPrefix: self.__reference_prefix}

    def managementPolicy(self, traitSets, context, hostSession):
        # The management policy defines which traits the manager is
        # capable of imbuing queried traitSets with. In this case, we
        # manage locations of assets only, and only in a read, not a
        # write, context. Note `LocatableContentTrait` is a trait from
        # the openassetio-mediacreation library, see :
        # https://github.com/OpenAssetIO/OpenAssetIO-MediaCreation
        policies = []
        for traitSet in traitSets:
            policy = TraitsData()
            # The host asks specifically if a sets of traits are
            # supported In this case, if any of the input traitSets are
            # for read, and contain LocatableContent, as we can supply
            # data for that trait, we imbue a managed policy response,
            # as well as the traits we are able to supply data for. It's
            # important to get this right, for more info, see:
            # https://openassetio.github.io/OpenAssetIO/classopenassetio_1_1v1_1_1host_api_1_1_manager.html#acdf7d0c3cef98cce7abaf8fb5f004354
            if context.isForRead() and LocatableContentTrait.kId in traitSet:
                ManagedTrait.imbueTo(policy)
                LocatableContentTrait.imbueTo(policy)

            policies.append(policy)

        return policies

    def isEntityReferenceString(self, someString, hostSession):
        # This function is used by the host to determine if an entity
        # reference is recognized as one handled by this manager.
        #
        # This should be a lightweight, textual sort of comparison,
        # don't make backend calls here.
        #
        # If this function returns false for a string, your manager will
        # not be invoked any further for that string.
        #
        # The recommended way to do this is to use a prefix, as that
        # allows OpenAssetIO some room to perform optimizations. See
        # info()
        return someString.startswith(self.__reference_prefix)

    def resolve(
        self, entityReferences, traitSet, context, hostSession, successCallback, errorCallback
    ):
        # If your resolver doesn't support write, like this one, reject
        # a write context via calling the error callback.
        if context.isForWrite():
            result = BatchElementError(
                BatchElementError.ErrorCode.kEntityAccessError, "Entities are read-only"
            )
            for idx in range(len(entityReferences)):
                errorCallback(idx, result)
            return

        # If the requested traitSet (which is constant for the batch),
        # doesn't contain LocatableContent trait ID, there is no need to
        # do any further processing, early out.
        if LocatableContentTrait.kId not in traitSet:
            for idx in range(len(entityReferences)):
                successCallback(idx, TraitsData())
            return

        # You should attempt to retrieve your data at this point,
        # especially if your backend supports batch operations. It's
        # likely that there will be many entityReferences, and avoiding
        # costly call-outs inside the loop below will be advantageous.
        #
        # For the purposes of this template, we use this fake map
        # of LocatableContent paths to serve as our "database".
        # Replace this with querying your backend systems.
        managed_filesystem_locations = {
            "my_asset_manager:///anAsset": "file:///some/filesystem/path",
            "my_asset_manager:///anAsset2": "file:///some/filesystem/path2",
            "my_asset_manager:///anAsset3": "file:///some/filesystem/path3",
        }

        # Iterate over all the entity references, calling the correct
        # error/success callbacks into the host.
        # You should handle success/failure on an entity-by-entity
        # basis, do not abort your entire resolve because any single
        # entity is malformed/can't be processed for any reason, use
        # the error callback and continue.
        for idx, ref in enumerate(entityReferences):
            # It may be that one of the references you are provided is
            # recognized for this manager, but has some syntax error or
            # is otherwise incorrect for your specific resolve context.
            # For example, an asset reference that specifies a version
            # for an un-versioned entity could be considered malformed.
            #
            # N.B. It's not required to perform an explicit check here
            # if this is naturally serviced during your backend lookup,
            # the key is not to error the whole batch, but use the error
            # callback for relevant references.
            identifier_is_malformed = is_malformed_ref(ref)
            if identifier_is_malformed:
                error_result = BatchElementError(
                    BatchElementError.ErrorCode.kMalformedEntityReference,
                    "Entity identifier is malformed",
                )
                errorCallback(idx, error_result)
            else:
                # If our manager has the asset in question, we can
                # let the host know about the LocatableContent for
                # this specific entity.
                if ref.toString() in managed_filesystem_locations:
                    success_result = TraitsData()
                    trait = LocatableContentTrait(success_result)
                    trait.setLocation(managed_filesystem_locations[ref.toString()])
                    successCallback(idx, success_result)
                else:
                    # Otherwise, we haven't got the entity available for
                    # resolution, to call the error callback with an
                    # entity resolution error for this specific entity.
                    error_result = BatchElementError(
                        BatchElementError.ErrorCode.kEntityResolutionError,
                        f"Entity '{ref.toString()}' not found",
                    )
                    errorCallback(idx, error_result)


# Internal function used in Resolve, replace with logic based on what a
# malformed ref means in your backend. For the demonstrative purposes of
# this template, we pretend to support query parameters, then invent a
# completely arbitrary query parameter that we don't support. (We then
# test our implementation using the api compliance suite, see
# fixtures.py)
def is_malformed_ref(entityReference):
    return "?unsupportedQueryParam" in entityReference.toString()
