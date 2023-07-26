# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2023 The Foundry Visionmongers Ltd

"""
Shared fixtures for MyAssetManager pytest coverage.
"""

# pylint: disable=invalid-name,redefined-outer-name
# pylint: disable=missing-class-docstring,missing-function-docstring

import os
import pytest

from openassetio.test.manager import harness


@pytest.fixture
def harness_fixtures(base_dir):
    """
    Provides the fixtues dict for MyAssetManager when used with
    the openassetio.test.manager.apiComplianceSuite.
    """
    fixtures_path = os.path.join(base_dir, "tests", "fixtures.py")
    return harness.fixturesFromPyFile(fixtures_path)


@pytest.fixture
def base_dir():
    """
    Provides the path to the base directory for the MyAssetManager
    codebase.
    """
    return os.path.dirname(os.path.dirname(__file__))
