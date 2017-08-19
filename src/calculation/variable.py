#a variable instance has two tkinter class variables: one for the entry fields and one for the labels
#additionally, the variables have a "valid" attribute which is true when the variable is in a range where it can be used in calculation, false otherwise
#holds all names/units to be displayed in the UI
import tkinter as tk
from tkinter import messagebox # required for messagebox to work, even with tkinter/tk.messagebox as messagebox import isn't part of tkinter __init__

class Variable:
    #inits with all variables 0 (ints), 0.0 (doubles) or False (bools)
    #takes 
    def __init__(self, name, unit):
        print("creating variable [" + name + "]")
        
        self.valid = False
        self.name = name
        self.unit = unit
        
        self.entry = tk.DoubleVar()
        self.entry.set(0.0)
        self.value = tk.DoubleVar()
        self.value.set(0.0)
        
        self.error = tk.StringVar()
        self.error.set("enter values")
        
    #sets the status_label class double as the current entry value
    def entry_to_value(self):
        self.value.set(self.entry.get())
    
    #sets the entry class value equal to the value of the value class variable
    def value_to_entry(self):
        self.entry.set(self.value.get())
        
    #checks the current entry value and sets the status accordingly
    #returns the status it set as a boolean
    def valid_input(self):
        #if the value of entry is not a double (also empty), calling .get() will raise a TclError
        try:
            self.entry.get()
            #if the input doesn't raise a TclError it's a double
            return True
        #if this happens print to the console and throw a GIU popup warning
        #set valid to false, the status error message to "invalid input" and return False
        except tk.TclError:
            print("invalid input for [" + self.name + "]")    
            self.valid = False
            self.error.set("invalid input")
            tk.messagebox.showerror("Variable error", "The input for [" + self.name + "] is invalid")
            return False