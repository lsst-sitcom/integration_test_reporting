# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

import argparse

__all__ = ['create_parser']


def create_parser():
    """Create the argument parser for the main application.
    Returns
    -------
    argparse.ArgumentParser
        The application command-line parser.
    """
    description = ['This is the interface for Integration Test Reporting.']

    parser = argparse.ArgumentParser(description=' '.join(description),
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-l', '--location', dest='location',
                        help='Set the location of the test for EFD mapping.')

    parser.add_argument("--xml", dest="xml", help="The XML version to check")
    parser.add_argument("--sal", dest="sal", help="The SAL version to check")

    parser.add_argument("--index-auto", action="store_true",
                        help="Set a backlook index for auto-enabled CSCs.")

    parser.add_argument('sut', type=str,
                        help='File containing list of systems (CSCs) under test or a comma '
                             'delimited string of CSC names.')

    parser.set_defaults(location='tucson_efd')

    return parser
