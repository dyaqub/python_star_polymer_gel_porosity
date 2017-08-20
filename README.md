What does it do?
-------------
This program simplifies and visualizes the calculation of porosity information for crosslinked star polymers gels. It outputs the **molecular weight between crosslinks M<sub>c</sub> [g/mol]** and the **mesh size &xi; [nm]**. The required inputs are information about the swelling of the polymer during synthesis and in equilibrium, information about the network architecture/topology and several polymer and swelling agent constants. Specific sets of polymer constants, network architectures and swelling experiments can be saved and loaded as .txt files. 

![screenshot](https://user-images.githubusercontent.com/14539781/29494753-7aeeb278-85b1-11e7-8cce-c3613ee11b1e.JPG)

----------
How do I run the program?
-------------
In order to run the program, python 3 and the Tkinter, MatPlotLib and SymPy modules need to be installed. The program is started by running scr/main.py.  Installing Anaconda (available for Windows, Mac and Linux) will install all relevant packages without the need for admin access.

A compiled .exe will be added later for easier access.

----------
Where can I read more about the chemical background?
-------------
The original works on (hydro)gel porosity are conducted by Peppas and others. This article gives detailed information about the correlation of molecular weight between crosslinks and the network mesh size and end-to-end distance:

*Canal, T.; Peppas, N. A., Correlation between mesh size and equilibrium degree of swelling of polymeric networks. Journal of Biomedical Materials Research 1989, 23, 1183-1193.*

Due to the bimodal distribution of crosslinks in star polymer networks, Cima and Lopina derived a formula allowing the more accurate calculation of M<sub>c</sub> for crosslinked star polymer networks:

*Cima, L. G.; Lopina, S. T., Network Structures of Radiation-Cross-Linked Star Polymer Gels. Macromolecules 1995, 28, 6787-6794.*

----------
How does the program work?
-------------
The program is written in python 3, and used the Tkinter GUI module. It used the MatPlotLib module for plotting the graphs, and uses the SymPy module for numerically solving the equation giving M<sub>c</sub> .

----------
