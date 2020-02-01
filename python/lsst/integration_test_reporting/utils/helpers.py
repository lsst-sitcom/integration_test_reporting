# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

__all__ = ['efd_name', 'filter_measurements']


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


def filter_measurements(measurements, csc_name, topic_name):
    """Filter full list of measurements looking for CSC plus topic name.

    Parameters
    ----------
    measurements : list[str]
        The list of all available measurements.
    csc_name : str
        Name of the CSC to filter on.
    topic_name : str
        Name of the topic to filter on.

    Returns
    -------
    list[str]
        Filtered list of topics.
    """
    csc_filtered = [measurement.split('.')[-1] for measurement in measurements
                    if csc_name in measurement]
    topic_filtered = [topic for topic in csc_filtered if topic_name in topic]
    return topic_filtered
