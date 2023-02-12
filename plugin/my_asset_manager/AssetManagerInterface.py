#
#   Copyright 2013-2021 [The Foundry Visionmongers Ltd]
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
A single-class module, providing the MyAssetManagerInterface class.

The manager currently ignores all entity types.
"""

# Note that it should always be light-weight to construct instances of
# the this class. See the notes under the "Initialization" section of:
#   https://openassetio.github.io/OpenAssetIO/classopenassetio_1_1manager_a_p_i_1_1_manager_interface_1_1_manager_interface.html#details (pylint: disable=line-too-long)
# As such, any expensive module imports should be deferred.
from openassetio import constants, BatchElementError, TraitsData
from openassetio.managerApi import ManagerInterface


__all__ = [
    "MyAssetManagerInterface",
]


# TODO(TC): @pylint-disable
# As we are building out the implementation vertically, we have known
# fails for missing abstract methods.
# pylint: disable=abstract-method


class MyAssetManagerInterface(ManagerInterface):
    """
    Binds MyAssetManager to the OpenAssetIO ManagerInterface.

    This class contains none of the actual business logic implementing
    asset management, just bindings to the OpenAssetIO interface
    methods.
    """

    __reference_prefix = "my_asset_manager:///"

    def identifier(self):
        return "myorg.manager.myassetmanager"

    def initialize(self, managerSettings, hostSession):
        pass

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
        # pylint: disable=unused-argument
        return [TraitsData() for _ in traitSets]

    def isEntityReferenceString(self, someString, hostSession):
        return someString.startswith(self.__reference_prefix)

    def resolve(
        self, entityReferences, traitSet, context, hostSession, successCallback, errorCallback
    ):
        # Implement your resolution logic here.

        # This is a dummy manager which only has the "anAsset" entry.
        # For a better and more complete example implementation, which
        # deals with things such as entity access modes and malformed
        # entity references, see :
        # https://github.com/OpenAssetIO/OpenAssetIO-Manager-BAL/blob/main/plugin/openassetio_manager_bal/BasicAssetLibraryInterface.py
        for idx, ref in enumerate(entityReferences):
            print(ref.toString())
            if ref.toString() == "my_asset_manager:///anAsset":
                result = TraitsData()
                result.addTrait("number")
                result.setTraitProperty("number", "value", 42)
                successCallback(idx, result)
            else:
                error_result = BatchElementError(
                    BatchElementError.ErrorCode.kEntityResolutionError,
                    f"Entity '{ref.toString()}' not found",
                )
                errorCallback(idx, error_result)
