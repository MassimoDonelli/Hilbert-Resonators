# Hilbert-Resonators
Hilbert_Resonator.py is a tool that permits the design of a planar Hilbert resonators. It also creates a DXF CAD file that can be imported with electromagnetic simulator or printed on a PCB. The code is written in python3 and it permits to save the wheels geometries in dxf format.
Usage: python3 Source/Hilbert_.Resonator.py < Examples/SquareSide_10mm_Level3.txt

There is a main file named Hilbert_Resonator.py placed in the Source dir. 
There are examples in the following dir:
..\EXAMPLE\    		 		   <---- This DIR contains a set of slides related to a Brain RMN   
InputSide_50mm_Level3.txt 	   <---- An example of resonator with a side of 10mm e 3 levels
Source\Hilbert_Resonator.py    <---The SW

Input example:
256          <---- dpi imagine taken from turtle visualization
300          <---- Desired frequency in [MHz] for the resonator
1.0          <---- Trace thickness PCB in [mm]
3.8          <---- Dielectric Permittivity of the PCB substrate
2            <---- Flag 0 fixed side, 1 fixed level, 2 fixed side and level
50.0         <---- Side of the Hilbert Square
3            <---- Level of the Hilbert curva 1 is the minimum
file_name    <---- Name of the dxf and png file   

Output example:

A turtle visualization and a DXF cad file.
Insert the DPI:256
Insert the frequency [MHz]:300.0
Insert the trace thickness [mm]:1.0
Insert substrate EPS:3.8
Insert mode 0 fixed side, 1 fixed level, 2 fixed side and level:2
Insert the square side [mm]:50.0
Insert the level:3
Insert the Filename:300MHz.dxf
The DXF has been created

License:
See LICENSE.txt for more information.

Contact: Massimo Donelli - massimo.donelli@unitn.it 

Project link: 
