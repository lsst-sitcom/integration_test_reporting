# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

from lsst.integration_test_reporting.utils import CSC


class TestCsc():

    def setup_class(cls):
        cls.csc1 = CSC("Environment", 1)
        cls.csc2 = CSC("ATArchiver", None)

    def test_properties(self):
        assert self.csc1.full_name == "Environment:1"
        assert self.csc2.full_name == "ATArchiver"

    def test_efd_topic(self):
        topic_name = "logevent_summaryState"

        assert self.csc1.efd_topic(topic_name) == "lsst.sal.Environment.logevent_summaryState"
        assert self.csc2.efd_topic(topic_name) == "lsst.sal.ATArchiver.logevent_summaryState"
