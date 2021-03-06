# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

import os

__all__ = ["CSC"]

INDEX_DELIM = ':'


class CSC:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __eq__(self, other):
        return other.name == self.name and other.index == self.index

    @property
    def full_name(self):
        _csc_name = f"{self.name}"
        if self.index:
            _csc_name += f"{INDEX_DELIM}{self.index}"
        return _csc_name

    def efd_topic(self, topic_name):
        return f'lsst.sal.{self.name}.{topic_name}'

    @classmethod
    def from_entry(cls, csc_str):
        if INDEX_DELIM in csc_str:
            parts = csc_str.split(INDEX_DELIM)
            return CSC(parts[0], int(parts[1]))
        else:
            return CSC(csc_str, None)

    @classmethod
    def get_from_file(cls, csc_file):
        cscs = []
        if '~' in csc_file:
            csc_file = os.path.expanduser(csc_file)
        with open(csc_file, 'r') as ifile:
            for line in ifile:
                v = line.strip()
                if v.startswith('#'):
                    continue
                cscs.append(CSC.from_entry(v))

        return cscs

    @classmethod
    def get_from_list(cls, csc_list):
        csc_entries = csc_list.split(',')
        cscs = []
        for csc_entry in csc_entries:
            cscs.append(CSC.from_entry(csc_entry))
        return cscs

    @classmethod
    def get_from_source(cls, source):
        if ',' in source:
            return cls.get_from_list(source)
        else:
            return cls.get_from_file(source)
