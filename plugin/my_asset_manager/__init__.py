#
#   Copyright 2013-2023 [The Foundry Visionmongers Ltd]
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
Module Documentation for MyAssetManager here.
"""

# pylint: disable=import-outside-toplevel
#
# It is important to minimise imports here. This module will be loaded
# when the plugin system scans for plugins. Postpone importing any
# of the actual implementation until it is needed by the
# PythonPluginSystemManagerPlugin's implementation.

from openassetio.pluginSystem import PythonPluginSystemManagerPlugin


class MyAssetManagerPlugin(PythonPluginSystemManagerPlugin):
    """
    The PythonPluginSystemManagerPlugin is responsible for constructing
    instances of the manager's implementation of the OpenAssetIO
    interfaces and returning them to the host.
    """

    @staticmethod
    def identifier():
        # The identifier here _must_ be the same as the one returned by
        # the interface implementation for it's `identifier` method.
        return "myorg.manager.my_asset_manager"

    @classmethod
    def interface(cls):
        from .AssetManagerInterface import MyAssetManagerInterface

        # Note that it should always be light-weight to construct
        # instances of the ManagerInterface class. See the notes under
        # the "Initialization" section of:
        # https://openassetio.github.io/OpenAssetIO/classopenassetio_1_1v1_1_1manager_api_1_1_manager_interface.html#details (pylint: disable=line-too-long)
        return MyAssetManagerInterface()


# Set the plugin class as the public entrypoint for the plugin system.
# A plugin is only considered if it exposes a `plugin` variable at this
# level, holding a class derived from PythonPluginSystemManagerPlugin.

# pylint: disable=invalid-name
plugin = MyAssetManagerPlugin
