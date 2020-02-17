# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

import os

from lsst.integration_test_reporting.utils import CSC


class TestCsc():

    def setup_class(cls):
        cls.csc1 = CSC("Environment", 1)
        cls.csc2 = CSC("ATArchiver", None)

        cls.csc_list = ["Environment:1", "ATArchiver"]
        cls.csc_obj_list = [cls.csc1, cls.csc2]

    def make_csc_file(self, filename):
        with open(filename, 'w') as ofile:
            for csc in self.csc_list:
                ofile.write(csc + os.linesep)

    def test_properties(self):
        assert self.csc1.full_name == "Environment:1"
        assert self.csc2.full_name == "ATArchiver"

    def test_efd_topic(self):
        topic_name = "logevent_summaryState"

        assert self.csc1.efd_topic(topic_name) == "lsst.sal.Environment.logevent_summaryState"
        assert self.csc2.efd_topic(topic_name) == "lsst.sal.ATArchiver.logevent_summaryState"

    def test_from_file(self):
        temp_file = "testing.dat"
        self.make_csc_file(temp_file)

        cscs = CSC.get_from_file(temp_file)
        assert cscs == self.csc_obj_list

        os.remove(temp_file)

    def test_from_list(self):
        truth_list = ",".join(self.csc_list)
        cscs = CSC.get_from_list(truth_list)
        assert cscs == self.csc_obj_list

    def test_from_source(self):
        truth_list = ",".join(self.csc_list)
        cscs = CSC.get_from_source(truth_list)
        assert cscs == self.csc_obj_list

        temp_file = "testing1.dat"
        self.make_csc_file(temp_file)
        cscs = CSC.get_from_source(temp_file)
        assert cscs == self.csc_obj_list
        os.remove(temp_file)
