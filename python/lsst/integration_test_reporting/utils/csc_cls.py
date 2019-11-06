import os

__all__ = ["CSC"]


class CSC:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    @property
    def full_name(self):
        _csc_name = f"{self.name}"
        if self.index:
            _csc_name += f":{self.index}"
        return _csc_name

    @classmethod
    def from_entry(cls, csc_str):
        if '=' in csc_str:
            parts = csc_str.split('=')
            return CSC(parts[0], int(parts[1]))
        else:
            return CSC(csc_str, 0)

    @classmethod
    def get_from_file(cls, csc_file):
        cscs = []
        if '~' in csc_file:
            csc_file = os.path.expanduser(csc_file)
        with open(csc_file, 'r') as ifile:
            for line in ifile:
                v = line.strip()
                cscs.append(CSC.from_entry(v))

        return cscs
