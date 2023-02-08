# eeschema-script-control

There isn't currently a way to script Kicad's schematic entry in the way the PCB layout can be.
However the file format is a standard format, it's well documented, and simple which makes it a relatively straight forward task to perform scripting tasks by editing the file directly.

The file format is in a simple and standard S-expression format so some script control can be done by parsing the file into a S-expression tree and editing the file programatically.


## Goals & Scripts
[x] Change the visibility of part fields
[ ] Map annotations of a hierarchical schematic sheet
[ ] Auto cleanup of an imported Diptrace -> Eagle -> Kicad schematic

## Resources
+ [KiCAD S-Expressions: https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html](https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html)
+ [esxpdata Library: https://sexpdata.readthedocs.io/en/latest/](https://sexpdata.readthedocs.io/en/latest/)
