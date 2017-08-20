# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:39:03 2017

@author: GC

Program features:
    - calculates molecular weight between crosslinks (Mc) and the mesh size for crosslinked star polymer hydrogel networks
    
    - GUI based on Tkinter
    - paramters are validated when entered (followed by pressing an update button) shown by the entered value and shown as red/green according to status
    - visualize Mc calculation using matplotlib on a tkinter canvas
    - ability to save and load constants and parameters into a .txt file
    - updating the plot after changing variables immediately updates the final results

Notes for developers:
    - git version control is used
    - development takes place from the master branch, with specific features branching from master
    - feature branches are rebased from master, after which release is rebased using master
    - stable versions are pushed to remote from the release branch
    
    - function calling and key function events are printed to the console for faster debugging
    
    - the main controller creates the other controllers and starts the programm
    
    - the UI controller creates the master layout, sub layouts and fills them with the UI elements required
    - UI elements are blocks of variable input fields with update/save/load buttons and the graph plot and results frame
    - UI elements handle all UI aspects relevant for them, but call to calculation or variable controllers for actual functionality
    
    - the variable controller initiates and stores all variable objects, and handles updating/saving/loading of the variables
    - a variable object is created which uses two Tkinter ClassVars which can be linked to Tkinter labels in the GUI. It also can validate itself and has bounds
    - the variable controller stores variable objects in dictionaries, and additionally has a dictionary with all variable object dictionaries (in this case 3)
    
    - the calculation controller handles numerically solving for Mc using the sympy module, calculates the final results and adds the graphs to the plot

TODO
    - the numeric equation solving in sympy may yield a coplex number when no solution is found --> this should popup a GUI error

"""

import controllers.UI_controller
import controllers.variable_controller
import controllers.calculation_controller

# main controller creates the controllers and starts the program
# it has access to a UIcontroller where all UI events and changes take place
# it has access to a variableController where all entered variables are stored/retrieved. An instance of the Var Controller is passed to UIcontroller
class MainController:   
    
    def __init__(self):
        print("\ninitializing programm")
        
        # create the controllers
        self.var_controller = controllers.variable_controller.VariableController()
        self.calc_controller = controllers.calculation_controller.CalculationController(self.var_controller)
        self.ui_controller = controllers.UI_controller.UIcontroller(self.var_controller, self.calc_controller)
        
    # starts the program by calling the UI controller to start the Tkinter mainloop
    def start(self):
        
        print("starting program")
        
        self.ui_controller.start_UI()
    
    
# starts the main controller
program = MainController()
program.start()