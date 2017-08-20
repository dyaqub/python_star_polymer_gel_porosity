# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:39:03 2017

@author: GC

Program goals:
    - GUI based on Tkinter
    - paramters are validated when entered (followed by pressing an update button) shown by the entered value and shown as red/green according to status
    - visualize Mc calculation using either numpy plot or own made plot based on tkinter canvas/polygons
    - ability to save and load constants and parameters into a YAML file
"""

import tkinter as tk
import controllers.UI_controller
import controllers.variable_controller
import controllers.calculation_controller

#main controller orchestrates conduction of the program
#it ensures the correct polymer values (constants and network architecture) are entered first
#it has access to a UIcontroller where all UI events and changes take place
#it has access to a variableController where all entered variables are stored/retrieved. An instance of the VarController is passed to UIcontroller
class MainController:   
    
    def __init__(self):
        print("\ninitializing programm")
        
        #the tkinter master/root must be set before any tkinter class variables (IntVar etc) can be initialized
        print("initializing GUI root")
        self.master = tk.Tk()
        self.master.title("Calculate mesh size from swelling") # sets the title displayed in the window frame bar
        
        self.var_controller = controllers.variable_controller.VariableController()
        self.calc_controller = controllers.calculation_controller.CalculationController(self.var_controller)
        self.ui_controller = controllers.UI_controller.UIcontroller(self.master, self.var_controller, self.calc_controller)
        
    def start(self):
        print("starting GUI")
        self.ui_controller.start_UI()
    
#starts the main controller
program = MainController()
program.start()