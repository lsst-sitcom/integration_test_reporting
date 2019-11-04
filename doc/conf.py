"""Sphinx configuration file for an LSST stack package.

This configuration only affects single-package Sphinx documentation builds.
"""

from documenteer.sphinxconfig.stackconf import build_package_configs
import lsst.integration.test.reporting


_g = globals()
_g.update(build_package_configs(
    project_name='integration_test_reporting',
    version=lsst.integration.test.reporting.version.__version__))
