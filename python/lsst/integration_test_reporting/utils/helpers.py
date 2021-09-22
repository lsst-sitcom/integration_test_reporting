# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

__all__ = ['check_correct_value', 'check_not_empty', 'efd_name', 'filter_measurements']


def check_correct_value(truth, value, message):
    """Check value against a truth value.

    Parameters
    ----------
    truth : any
        The reference value.
    value : any
        The value to check.
    message : str
        The base message to provide.
    """
    if truth is not None:
        if truth == value:
            print(f"{message} OK")
        else:
            print(f"{message} incorrect: {value}")


def check_not_empty(value, message):
    """Check value is not empty.

    Parameters
    ----------
    value : any
        The value to check.
    message : str
        The base message to provide.
    """
    if value.strip() == "":
        print(f"{message} cannot be empty!")
    elif value.strip() == "?":
        print(f"{message} cannot be {value.strip()}")
    else:
        print(f"{message} OK: {value}")


def efd_name(csc, topic):
    """Get a fully qualified EFD topic name.

    Parameters
    ----------
    csc : str
        The name of the CSC.
    topic : str
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
