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

    efd_auth = parser.add_mutually_exclusive_group()

    efd_auth.add_argument('-f', '--efd-auth-file', dest='efd_auth_file',
                          help='Supply a file containing EFD authentication information.')

    parser.add_argument('sut', type=str,
                        help='File containing list of systems (CSCs) under test.')

    parser.set_defaults(location='tucson')

    return parser
