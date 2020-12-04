# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

from lsst.integration_test_reporting.utils import create_parser


class TestArgumentParser():

    def setup_class(cls):
        cls.parser = create_parser()

    def test_object_after_construction(self):
        assert self.parser is not None

    def test_help_documentation(self):
        assert self.parser.format_help() is not None

    def test_behavior_with_no_arguments(self):
        args = self.parser.parse_args(['sut.dat'])
        assert args.location == 'tucson_efd'
        assert args.sut == 'sut.dat'

    def test_location(self):
        args = self.parser.parse_args(['-l', 'ncsa_efd', 'sut.dat'])
        assert args.location == 'ncsa_efd'
        args = self.parser.parse_args(['--location', 'summit_efd', 'sut.dat'])
        assert args.location == 'summit_efd'
