import calculation.variable as var
import tkinter as tk
from tkinter import messagebox # required for messagebox to work, even with tkinter/tk.messagebox as messagebox import isn't part of tkinter __init__
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename 
import sys

# initialized by the main controller, and passed to the UI controller
# is responsible for creating, storing, updating, saving and loading variable objects, which are required for both the GUI and calculaations
class VariableController:
    
    def __init__(self):
        print("initializing variable controller")
    
    # creates the variable objects and adds them to the respective dicts using the variable name as the dict key
    # the reason the variable nanme is also the dict key, is so that the variable objects can be accessed and stored easier during file loading/saving
    # NOTE: this method defines the variables and variable lists which make up the UI, the UI controller accesses these and builds input fields for each
    # the variable bounds are chosen to accomodate more than chemically possible
    def create_variables(self):
        print("creating variables")
        
        self.polymer_constant_variables = {"repeating unit MW" : var.Variable("repeating unit MW", "g/mol", 1.0, 1000000.0),
                                           "average bond length" : var.Variable("average bond length", "nm", 0.05, 10.0),
                                           "characteristic ratio": var.Variable("characteristic ratio", " - ", 0.1, 1000.0),
                                           "Flory parameter" : var.Variable("Flory parameter", " - ", 0.01, 1000.0),
                                           "specific volume polymer" : var.Variable("specific volume polymer", "mL/g", 0.01, 100.0),
                                           "swelling agent molar volume" : var.Variable("swelling agent molar volume", "mL/mol", 0.1, 1000000.0)}
        
        self.network_architecture_variables = {"arm molecular weight" : var.Variable("arm molecular weight", "g/mol", 1.0, 1000000000.0),
                                               "degree of crosslinking in arm" : var.Variable("degree of crosslinking in arm", " - ", 0.01, 1000000.0),
                                               "degree of crosslinking in core" : var.Variable("degree of crosslinking in core", " - ", 0.01, 100000.0)}
        
        self.experimental_swelling_variables = {"polymer volume fraction equilibrium" : var.Variable("polymer volume fraction equilibrium", " - ", 0.0000001, 1.0),
                                                "polymer volume fraction synthesis" : var.Variable("polymer volume fraction synthesis", " - ", 0.0000001, 1.0)}
        
        #dictionary links variable dict titles to the variable dict containing the variable object instances (ditionary of dictionaries)
        self.variable_dicts = {"Polymer Constants" : self.polymer_constant_variables,
                               "Network Architecture" : self.network_architecture_variables,
                               "Experimental Swelling" : self.experimental_swelling_variables}
        
        self.manual_Mc = var.Variable("molecular weight between crosslinks", "g/mol", 1, 10000000000)
    
    # validates the current entries (actual validation with error handling is done by variable class), and changes the labels accordingly (both value and color)
    # this method takes the variable_dict_title to find the variables, and a dictionary of status lable widgets so it can modify them without access to the UI
    def update_variable_list(self, variable_dict_title, status_label_widgets_dict):
        print("\nUpdating variable list [" + variable_dict_title + "]:")
        
        # iterates through all variable objects in the dictionary, checks if the input is valid and in bounds, and updates the status label accordingly
        for variable_name, variable_object in self.variable_dicts[variable_dict_title].items():
            
            status_label_widget = status_label_widgets_dict[variable_object] # get the respective status label from the dict using the object variable key
            
            # first check if the entry input is valid (done by variable class, checks for both float/double type and value in bounds)
            if variable_object.valid_entry_input():
                
                variable_object.entry_to_value() # transfers the current value in the entry to the status value of the variable object
                variable_object.valid = True
                status_label_widget.configure(textvariable = variable_object.value, fg = "green") # sets the status label to display the value
                print("[" + variable_name + "] successfully set to " + str(variable_object.value.get()))
                
            # if invalid set the status label to display the error message in red
            else:
                
                variable_object.valid = False
                status_label_widget.configure(textvariable = variable_object.error, fg = "red") # sets the label to display the error (value set by var object) 
    
    # saves the variable dictionary (takes dictionary title as argument) to a .txt file if all variable objects are valid, returns False otherwise
    def write_to_file(self, variable_dict_title):
        print("\ntrying to write [" + variable_dict_title + "] variables to file")
        
        # check if all variable objects have a True .valid attribute, otherwise return false
        for variable_name, variable_object in self.variable_dicts[variable_dict_title].items():
            print("checking validity of variable [" + variable_name + "]")
            
            if variable_object.valid == False:
                
                print("invalid variable [" + variable_name + "] \ncancelling writing to file")
                tk.messagebox.showerror("Invalid variable", "Cannot save variables to file. \nThe variable [" + variable_name + "] is invalid.")
                return False
            
        print("all variables in [" + variable_dict_title + "] valid")        
        
        # creating the file is put in a try/except block in case the file save is cancelled (path = '') or a different error occurs
        try:
            # get the file path to save using tkinter asksaveagdialog
            file_path = asksaveasfilename(initialdir = "", filetypes = (("Text File", "*.txt"),), title = "Choose a file.")
            print("\nchosen file path: " + file_path)
        
            # initialize the file for writing (overwrite allowed, the user is prompted during asksaveasfilename)
            save_file = open(file_path, 'w') # mode w means the file will be empty and overwritten
            
            # write the variable list header and values
            save_file.write(variable_dict_title + "\n")
            print("written header line [" + variable_dict_title + "]")

            for variable_name, variable_object in self.variable_dicts[variable_dict_title].items():
                
                save_file.write(variable_name + "=" + str(variable_object.value.get()) + "\n") # double value converted to string
                print("written variable [" + variable_name + "] with value " + str(variable_object.value.get()))
            
            # close the file and show a success message
            save_file.close()
            tk.messagebox.showinfo("File saved", "File written successfully")
            print("file written successfully")
        
        # if any errors occur during the try block, print the error type and error message
        # NOTE: does not popup a GUI error message because the most likely except case is the user cancelling the file save
        except:
            print("\nerror during file saving")
            print(sys.exc_info()[0].__name__)
            print(sys.exc_info()[1])
            return False
    
    # opens a file for a variable dictionary, shows an error popup when the wrong file is loaded, and adjusts the variable status labels for all variables
    def load_file(self, variable_dict_title, status_label_widgets_dict):
        # open the load file fialog
        file_path = askopenfilename(initialdir = "", filetypes = (("Text File", "*.txt"),), title = "Choose a file.")
        print ("\nloading file: " + file_path)
        
        # use a try/except in case the user closes the file dialog or any error occurs
        try:
            variable_list_file = open(file_path, 'r')
                
            # load all lines into a list, and remove the newline ends
            file_lines = [line.strip('\n') for line in variable_list_file.readlines()] # in python3 map use is discouraged and ist comprehension is faster
                
            print("File readout:\n" + str(file_lines))
            
            header = file_lines[0] # the first line of the file is the dictionary name
            
            # check if the header occurs as a key in the variable lists dict of the controller, if yes delete the header, if no exit method by returning false
            if header in list(self.variable_dicts.keys()): # .keys() on a dict returns a dict_keys object, not a list directly
            
                print("found variable list header: [" + header + "]")
                del file_lines[0]           
            
            else:
                
                print("no variable list header recognized, cancelled file load")
                tk.messagebox.showerror("Header error", "The header [" + header + "] is not a recognized variable list")
                variable_list_file.close()
                return False
            
            # raise an error message and return false if the file header is not equal to the variables list title passed this method
            if header != variable_dict_title:
                
                print("header [" + header + "] not equal to the variable list [" + variable_dict_title + "]\ncancelling file load")
                tk.messagebox.showerror("Header error", "header [" + header + "] not equal to the variable list [" + variable_dict_title + "]")
                return False
                
            # go through the list of lines (now without header) and create lists [variable name, value] by splitting at '='
            print("converting lines to name-variable pairs")
            for line in file_lines:
                
                split_line_input = line.split('=')
                name, value = [split_line_input[0], float(split_line_input[1])] # convert the value from string to float/double
                print("variable name: [" + name + "], value: " + str(value))
                
                try:
                    # if the name of the variable exists as a variable object in the dict created previously from the variable list, set the value and label
                    if name in list(self.variable_dicts[header].keys()):
                        
                        variable_object = self.variable_dicts[header][name]
                        variable_object.value.set(value)
                        variable_object.value_to_entry() # update the value of the entry field to display the loaded value as well
                        variable_object.valid = True  
                        status_label_widgets_dict[variable_object].configure(textvariable = variable_object.value, fg = "green")
                        print("variable [" + name + "] found, set value to " + str(value))
                        
                except KeyError:
                    
                    print("variable [" + name + "] not a part of variable list [" + variable_dict_title + "]")
                    tk.messagebox.showerror("Variable load error", "variable [" + name + "] not a part of variable list [" + variable_dict_title + "]")
            
            variable_list_file.close() # close the file
            tk.messagebox.showinfo("File loaded", "File loaded successfully")
            print("file loaded successfully")
        
        # if any errors occur during the try block, print the error type and message
        except:
            print("\nerror during file loading")
            print(sys.exc_info()[0].__name__)
            print(sys.exc_info()[1])
            return False
        
    # returns True if all variable objects in all variable dictionaries have True .valid attributes, False otherwise
    def all_variables_valid(self):
        print("checking if all variables are valid")
        
        # iterates through all variable dictionaries, then all variables and returns False if one object has a False .valid attribute
        for dict_name, variable_dict in self.variable_dicts.items():
            
            for variable_name, variable_object in variable_dict.items():
                
                if not variable_object.valid:
                    print("variable [" + variable_name + "] is not valid")
                    return False
        
        print("all variables valid")
        
        return True