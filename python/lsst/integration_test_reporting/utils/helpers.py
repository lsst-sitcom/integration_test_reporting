# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

__all__ = ['efd_name']


def efd_name(csc, topic):
    """Get a fully qualified EFD topic name.

    Parameters
    ----------
    csc : str
        The name of the CSC.
    topic : TYPE
        The name of the topic.
    """
    return f"lsst.sal.{csc}.{topic}"
