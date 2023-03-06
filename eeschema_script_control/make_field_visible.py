import os
import copy
import click
import sexpdata


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

def is_in_leaf(entry, level):
    return isinstance(level, list) and entry in level


def get_component_lines(tree):
    symbol_lines = []
    for i, level in enumerate(tree):
        if not is_in_leaf(sexpdata.Symbol("symbol"), level):
            continue
        symbol_lines.append(i)
    return symbol_lines


class Schematic:
    '''
    Store section before components, components, and section after
    '''
    def __init__(self, tree):
        lines = get_component_lines(tree)
        self._schematic = tree
        self._components = [SymbolReader(tree[line]) for line in lines]

    def __str__(self):
        pass


def depth_first_parsing(line):
    '''
    return a dictionary of dictionaries
    Follow all nodes
    turn each node into a dictionary entry with the key, values... format
    when all nodes are read return a dictionary of format key, nodes...
    recurse into this return a dictonary of dictionaries
    '''
    if isinstance(line, list):
        key = line[0]
        nodes = []
        for entry in line[1:]:
            node = depth_first_parsing(entry)
            nodes.append(node)
        try:
            d = {key.tosexp(): nodes}
        except AttributeError:
            d = nodes
        return d
    return line


def depth_first_writing(line):
    '''
    return a dictionary of dictionaries
    Follow all nodes
    turn each node into a dictionary entry with the key, values... format
    when all nodes are read return a dictionary of format key, nodes...
    recurse into this return a dictonary of dictionaries
    '''
    if isinstance(line, list):
        key = line[0]
        nodes = []
        for entry in line[1:]:
            node = depth_first_writing(entry)
            nodes.append(node)
        try:
            d = {key.tosexp(): nodes}
        except AttributeError:
            d = nodes
        return d
    return line

'''
    [Symbol('lib_id'), 'Device:R_Network03_US']
[Symbol('at'), 110.49, 73.66, 0]
[Symbol('unit'), 1]
[Symbol('in_bom'), Symbol('yes')]
[Symbol('on_board'), Symbol('yes')]
[Symbol('dnp'), Symbol('no')]
[Symbol('fields_autoplaced')]
[Symbol('uuid'), Symbol('ff792108-7fde-47e3-af0f-8899b454eee1')]
[Symbol('property'), 'Footprint', 'Resistor_THT:R_Array_SIP4', [Symbol('at'), 117.475, 73.66, 90], [Symbol('effects'), [Symbol('font'), [Symbol('size'), 1.27, 1.27]], Symbol('hide')]]
[Symbol('property'), 'Datasheet', 'http://www.vishay.com/docs/31509/csc.pdf', [Symbol('at'), 110.49, 73.66, 0], [Symbol('effects'), [Symbol('font'), [Symbol('size'), 1.27, 1.27]], Symbol('hide')]]
[Symbol('pin'), '1', [Symbol('uuid'), Symbol('16cd1ee7-7c36-4c7f-b5fb-93f0ff7689a9')]]
[Symbol('pin'), '2', [Symbol('uuid'), Symbol('65d62806-6e6f-4a73-9b07-fd93506a41f7')]]
[Symbol('pin'), '3', [Symbol('uuid'), Symbol('e83bc850-7d31-40c1-a5cc-278d9177cf28')]]
[Symbol('pin'), '4', [Symbol('uuid'), Symbol('d83f6266-388c-4a2c-a27c-7ceb300e6c3d')]]
[Symbol('instances'), [Symbol('project'), 'test', [Symbol('path'), '/01aac243-47cd-4173-af73-efa617c8d0d0', [Symbol('reference'), 'RN1'], [Symbol('unit'), 1]]]]
'''

'''
    def _read(self, tree):
        # use dict of arrays
        fields_dict = {}
        fields = tree[1:]
        for line in fields:
            key = line[0]
            value = line[1:]
            if key not in fields_dict:
                fields_dict[key] = []
            fields_dict[key].append(value)
        return fields_dict

    def read_properties(self):
        properties_dict = {}
        for line in self._dict[Symbol('property')]:
            key = line[0]
            value = line[1:]
            properties_dict[key] = value
        return properties_dict

    def write_properties(self, properties_dict):
        self._dict[Symbol('property')] = [[key, *value] for key, value in properties_dict.items()]

        def write
        lines = []
        for key, value in fields_dict.items():
            if key in ['lib_id', 'uuid']:
                lines.append([sexpdata.Symbol("property"), key, value])
            else:
                lines.append([sexpdata.Symbol("property"), key, value])
        return lines

    def read_fields(self):
'''
class SymbolReader:
    def __init__(self, tree):
        self._dict = {}
        self._dict.update(depth_first_parsing(tree))

    def write(self):
        return self._write(self._dict)

    def _write(self, fields_dict):



    def __repr__(self):
        return str(self._dict)

    def __getitem__(self, key):
        return self._dict[key]

    @property
    def lib_id(self):
        return self["lib_id"][0]


def replace_components(schematic, components):
    '''
    replace all components in schematic with list of components
    '''
    pass



def change_field_visibility(schematic, fields, exclude):
    tree = copy.deepcopy(schematic)
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
    return tree, lines


def replace_part(schematic, settings):
    '''
    settings: {from: {replacement: {replacement}, move: [x,y], rotate: {degrees}} }
    keep value and footprint
    '''
    pass



@click.command()
@click.option("--fname", "-f", required=True, help="Schematic file")
@click.option("--fields", required=True, multiple=True, help="Name of field to make visible")
@click.option("--exclude", "-x", required=False, multiple=True, help="Values to skip")
def main(fname, fields, exclude):
    fbase, ext = os.path.splitext(fname)
    fout = f"{fbase}_edit{ext}"
    with open(fname, 'r') as f:
        schematic = sexpdata.loads(f.read())

    tree, lines = change_field_visibility(schematic, fields, exclude)

    with open(fout, 'w') as f:
        f.write(sexpdata.dumps(tree))
    print(f"Changed {lines} lines. Written to {fout}")


if __name__ == "__main__":
    main()
