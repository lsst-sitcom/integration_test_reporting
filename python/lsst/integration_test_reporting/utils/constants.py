# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

__all__ = ["NON_CONFIG_CSCS", "OFFLINE_CSCS"]

NON_CONFIG_CSCS = [
    "ATArchiver",
    "ATHeaderService",
    "ATMCS",
    "ATPneumatics",
    "ATPtg",
    "CCHeaderService",
    "CCArchiver",
    "DSM",
    "LinearStage",
    "MTPtg",
    "MTRotator",
    "ScriptQueue"
]

OFFLINE_CSCS = [
    "ATCamera",
    "CCCamera",
]
