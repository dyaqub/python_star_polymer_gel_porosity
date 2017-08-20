# a variable instance has two tkinter class variables: one for the entry fields and one for the labels
# additionally, the variables have a "valid" attribute which is true when the variable is in a range where it can be used in calculation, false otherwise
# holds all names/units to be displayed in the UI
import tkinter as tk
from tkinter import messagebox # required for messagebox to work, even with tkinter/tk.messagebox as messagebox import isn't part of tkinter __init__

class Variable:
    
    # inits with all variables with value 0.0 (double), and the standard error message as "enter variables"
    def __init__(self, name, unit, lower_bound, upper_bound):
        print("creating variable [" + name + "]")
        
        self.valid = False
        self.name = name
        self.unit = unit
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
        self.entry = tk.DoubleVar()
        self.entry.set(0.0)
        self.value = tk.DoubleVar()
        self.value.set(0.0)
        
        self.error = tk.StringVar()
        self.error.set("enter values")
        
    # sets the value as the current value in the entry field (only call this after entry field validation using valid_entry_input)
    def entry_to_value(self):
        
        self.value.set(self.entry.get())
    
    # sets the entry value equal to the variable value
    def value_to_entry(self):
        
        self.entry.set(self.value.get())
        
    # checks the current entry value and sets the validity and possibly error message accordingly
    # returns the status as a boolean
    def valid_entry_input(self):
        print("checking entry validity for variable [" + self.name + "]")
        
        # if the value of entry is not a double (also empty), calling .get() will raise a TclError
        try:
            # if the input doesn't raise a TclError it is a double
            entry_value = self.entry.get()
            
            # check if the value is in bounds, return True if it is otherwise raise error message and return false
            if self.value_in_bounds(entry_value):
                
                return True
            
            else:
                
                tk.messagebox.showerror("Variable error", "The input for [" + self.name + "] is out of bounds")
                self.valid = False
                self.error.set("out of bounds")
                
        # if the entry is not a valid double, print to the console and throw a GIU popup warning.
        # set valid to false, the status error message to "invalid input" and return False
        except tk.TclError:
            
            print("invalid input for [" + self.name + "]")    
            self.valid = False
            self.error.set("invalid input")
            tk.messagebox.showerror("Variable error", "The input for [" + self.name + "] is invalid")
            return False
    
    # takes a value, returns True if it is within bounds for the variable object, False if it is not
    def value_in_bounds(self, value):
        
        if value < self.lower_bound or value > self.upper_bound:
            return False
        else: 
            return True
        