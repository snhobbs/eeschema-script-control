# eeschema-script-control

There isn't currently a way to script Kicad's schematic entry in the way the PCB layout can be.
The file format is in a simple and standard S-expression format so some script control can be done by parsing the file into a S-expression tree and editing the file programatically.
This first goal of this project was to change the visibility of part fields which is implimented currently.

