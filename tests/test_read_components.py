import unittest
import pandas as pd
import eeschema_script_control
from eeschema_script_control import get_component_lines, SymbolReader
import sexpdata

schematic_f = "tests/test/test.kicad_sch"

class TestReadComponents(unittest.TestCase):
    def test_get_component_lines(self):
        '''
        Check that the correct number of components is found
        '''
        with open(schematic_f, 'r') as f:
            schematic = sexpdata.loads(f.read())

        self.assertEqual(len(get_component_lines(schematic)), 1)

    def test_read_write_symbol(self):
        with open(schematic_f, 'r') as f:
            schematic = sexpdata.loads(f.read())

        part_line = schematic[get_component_lines(schematic)[0]]
        symbol = SymbolReader(part_line)
        symbol_write = SymbolReader(symbol.write())
        self.assertEqual(str(symbol), str(symbol_write))

    def test_read_write_schematic(self):
        with open(schematic_f, 'r') as f:
            schematic = sexpdata.loads(f.read())
        self.assertEqual(1,1)


if __name__ == "__main__":
    unittest.main()
