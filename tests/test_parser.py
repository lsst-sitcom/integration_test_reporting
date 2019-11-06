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
        assert args.location == 'tucson'
        assert args.sut == 'sut.dat'
        assert args.efd_auth_file is None

    def test_location(self):
        args = self.parser.parse_args(['-l', 'ncsa', 'sut.dat'])
        assert args.location == 'ncsa'
        args = self.parser.parse_args(['--location', 'summit', 'sut.dat'])
        assert args.location == 'summit'

    def test_efd_auth(self):
        args = self.parser.parse_args(['-f', '~/.efd_auth', 'sut.dat'])
        assert args.efd_auth_file == '~/.efd_auth'
