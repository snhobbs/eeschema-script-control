import click
import sexpdata
import os


'''
eeschema schematic files are stored as standard sparameter files.
The format is standard allowing us to use generic tools to read the file.

We want to change the visibility of a given field in a schematic by removing the parameter "hide"

Each symbol and wire is stored as a top level entry. The parameters are stored as primarily as pairs with a key and value but not for all. The fields we're targeting are an entry in a top entry of a symbol.

+ Iterate through all levels
+ Skip lines that aren't lists
+ Skip lines whose first entry is not "symbol"
+ Iterate over the entered fields
+ Iterate over the symbols entries
+ Skip lines that do not start with "property"
+ Skip lines where the field does not match the entry (i.e. "property" "Reference"...)
+ Search for and remove the value "hide"
'''


class SymbolReader:
    def __init__(self, tree):
        self._dict = {}
        for line in tree:
            try:
                if line[0] == sexpdata.Symbol("property"):
                    self._dict[str(line[1])] = line[2]
            except (TypeError, IndexError, ValueError) as e:
                continue

            try:
                string = str(line[0])[len("Symbol(\""):-len("\")")]
                if string in ['lib_id', 'uuid']:
                    self._dict[string] = list(line[1:])
            except (TypeError, IndexError, ValueError) as e:
                continue

    def __repr__(self):
        return str(self._dict)

    def __getitem__(self, key):
        return self._dict[key]

    @property
    def lib_id(self):
        return self["lib_id"][0]

def is_in_leaf(entry, level):
    return isinstance(level, list) and entry in level

@click.command()
@click.option("--fname", "-f", required=True, help="Schematic file")
@click.option("--fields", required=True, multiple=True, help="Name of field to make visible")
@click.option("--exclude", "-x", required=False, multiple=True, help="Values to skip")
def main(fname, fields, exclude):

    fbase, ext = os.path.splitext(fname)
    fout = f"{fbase}_edit{ext}"
    with open(fname, 'r') as f:
        tree = sexpdata.loads(f.read())

    lines = 0
    for i, level in enumerate(tree):
        if not is_in_leaf(sexpdata.Symbol("symbol"), level):
            continue

        symbol = SymbolReader(level)
        if symbol.lib_id in exclude:
            continue

        for i2, level2 in enumerate(level):
            if not is_in_leaf(sexpdata.Symbol("property"), level2):
                continue

            if level2[1] not in fields:
                continue

            for i3, level3 in enumerate(level2):
                if not isinstance(level3, list):
                    continue

                if not sexpdata.Symbol("effects") in level3:
                    continue

                target = sexpdata.Symbol("hide")
                if target in level3:
                    level3.pop(level3.index(target))
                    lines += 1
                tree[i][i2][i3] = level3


    with open(fout, 'w') as f:
        f.write(sexpdata.dumps(tree))
    print(f"Changed {lines} lines. Written to {fout}")


main()
