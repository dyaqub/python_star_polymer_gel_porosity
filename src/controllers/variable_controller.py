import calculation.variable as var
import tkinter as tk
from tkinter import messagebox # required for messagebox to work, even with tkinter/tk.messagebox as messagebox import isn't part of tkinter __init__
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename 
import sys

#TODO: update comments with dicts instead of lists
#TODO: write class description comments
class VariableController:
    
    def __init__(self):
        print("initializing variable controller")
        
        #creates the empty variable lists
        #NOTE: variable object instances cannot be created until the tkinter.Tk() master/root is initialized because it builds on tkinter class variables
        self.create_variables()
    
    #creates the variable objects and adds them to the respective dicts using the variable name as the dict key
    #the reason the variable nanme is also the dict key, is so that the variable objects can be accessed and stores easier during file loading/saving
    #note that this method defines the variables and variable lists which make up the UI
    def create_variables(self):
        print("creating variables")
        
        self.polymer_constant_variables = {"repeating unit MW" : var.Variable("repeating unit MW", "g/mol"),
                                           "average bond length" : var.Variable("average bond length", "nm"),
                                           "characteristic ratio": var.Variable("characteristic ratio", " ? "),
                                           "Flory parameter" : var.Variable("Flory parameter", " ? "),
                                           "specific volume polymer" : var.Variable("specific volume polymer", "mL/g"),
                                           "swelling agent molar volume" : var.Variable("swelling agent molar volume", "mL/mol")}
        
        self.network_architecture_variables = {"arm molecular weight" : var.Variable("arm molecular weight", "g/mol"),
                                               "degree of crosslinking in arm" : var.Variable("degree of crosslinking in arm", " - "),
                                               "degree of crosslinking in core" : var.Variable("degree of crosslinking in core", " - ")}
        
        self.experimental_swelling_variables = {"polymer volume fraction equilibrium" : var.Variable("polymer volume fraction equilibrium", " - "),
                                                "polymer volume fraction synthesis" : var.Variable("polymer volume fraction synthesis", " - ")}
        
        #dictionary links variable dict titles to the variable dict containing the variable object instances (ditionary of dictionaries)
        self.variable_dicts = {"Polymer Constants" : self.polymer_constant_variables,
                               "Network Architecture" : self.network_architecture_variables,
                               "Experimental Swelling" : self.experimental_swelling_variables}
    
    #validates the current entries (actual validation with error handling is done by variable class), and changes the labels accordingly (both value and color)
    def update_variable_list(self, variable_dict_title, status_label_widgets_dict):
        print("\nUpdating variable list [" + variable_dict_title + "]:")
        
        all_valid = True # returned by the method, set to false if any invalid vars are encountered
        
        #iterates through all variable objects, checks if the input is valid and in bounds, and updates the status label accordingly
        for variable_name, variable_object in self.variable_dicts[variable_dict_title].items():
            
            status_label_widget = status_label_widgets_dict[variable_object] # get the respective status label from the dict using the object variable key
            
            #first check if the entry input is valid (only checks for valid double/float type)
            if variable_object.valid_input():
                #if valid transfer the entry value to the current status value, display the current status on the label and adjust the color to creen
                variable_object.entry_to_value()
                variable_object.valid = True
                status_label_widget.configure(textvariable = variable_object.value, fg = "green")
                print("[" + variable_name + "] successfully set to " + str(variable_object.value.get()))
            #if no set the status label to display the error message in red
            else:
                variable_object.valid = False
                status_label_widget.configure(textvariable = variable_object.error, fg = "red")
                all_valid = False
        
        return all_valid # returns true if all variable objects are valid, false otherwise
    
    #takes the title of the variable list as a parameter
    #saves the respective variable list to a file if all variable objects are valid, otherwise returns False
    def write_to_file(self, variable_dict_title):
        
        print("\ntrying to write [" + variable_dict_title + "] variables to file")
        
        #check if all variable objects have a True .valid attribute, otherwise return false
        for variable_name, variable_object in self.variable_dicts[variable_dict_title].items():
            print("checking validity of variable [" + variable_name + "]")
            if variable_object.valid == False:
                print("invalid variable [" + variable_name + "] \ncancelling writing to file")
                tk.messagebox.showerror("Invalid variable", "Cannot save variables to file. \nThe variable [" + variable_name + "] is invalid.")
                return False
        print("all variables in [" + variable_dict_title + "] valid")        
        
        #creating the file is put in a try/except block in case the file save is cancelled or a different error occurs
        try:
            #get the file path to save using tkinter asksaveagdialog
            file_path = asksaveasfilename(initialdir = "", defaultext=".png", filetypes =(("Text File", "*.txt"),), title = "Choose a file.")
            print("\nchosen file path: " + file_path)
        
            #initialize the file for writing (overwrite allowed, the user is prompted during asksaveasfilename)
            save_file = open(file_path, 'w') # mode w means the file will be empty and overwritten
            
            #write the variable list header and values
            save_file.write(variable_dict_title + "\n")
            print("written header line [" + variable_dict_title + "]")

            for variable_name, variable_object in self.variable_dicts[variable_dict_title].items():
                save_file.write(variable_name + "=" + str(variable_object.value.get()) + "\n") # double value converted to string
                print("written variable [" + variable_name + "] with value " + str(variable_object.value.get()))
            
            #close the file
            save_file.close()
            tk.messagebox.showinfo("File saved", "File written successfully")
            print("file written successfully")
        
        #if any errors occur during the try block, print the error type and message
        except:
            print("\nerror during file saving")
            print(sys.exc_info()[0].__name__)
            print(sys.exc_info()[1])
            return False
    
    #opens a file for a variable block (passed to the function as an argument)
    def load_file(self, variable_dict_title, status_label_widgets_dict):
        #open the load file fialog
        file_path = askopenfilename(initialdir="", filetypes =(("Text File", "*.txt"),), title = "Choose a file.")
        print ("\nloading file: " + file_path)
        
        #use a try/except in case the user closes the file dialog or any error occurs
        try:
            variable_list_file = open(file_path, 'r')
                
            #load all lines into an array, and remove the newline ends
            #TODO: change to lambda
            file_lines_raw = variable_list_file.readlines()
            file_lines = []
            for raw_line in file_lines_raw:
                file_lines.append(raw_line.rstrip('\n'))
            print("File readout:\n" + str(file_lines))
            
            #check if the first line is a part of the variable list titles, otherwise exit
            header = file_lines[0]
            
            #chechk if the header occurs as a key in the variable lists dict of the controller, if yes delete the header, if no exit method by returning false
            if header in list(self.variable_dicts.keys()): # .keys() on a dict returns a dict_keys object, not a list directly
                print("found variable list header: [" + header + "]")
                del file_lines[0]           
            else:
                print("no variable list header recognized, cancelled file load")
                tk.messagebox.showerror("Header error", "The header [" + header + "] is not a recognized variable list")
                variable_list_file.close()
                return False
            
            #raise an error message and return false if the file header is not equal to the variables list title passed this method
            if header != variable_dict_title:
                print("header [" + header + "] not equal to the variable list [" + variable_dict_title + "]\ncancelling file load")
                tk.messagebox.showerror("Wrong header line in file", "header [" + header + "] not equal to the variable list [" + variable_dict_title + "]")
                return False
                
            #go through the list of lines (now without header) and create lists [variable name, value] by splitting at '='
            print("converting lines to name-variable pairs")
            for line in file_lines:
                split_line_input = line.split('=')
                name, value = [split_line_input[0], float(split_line_input[1])] # convert the value from string to float/double
                print("variable name: [" + name + "], value: " + str(value))
                
                try:
                    #if the name of the variable exists as a variable object in the dict created previously from the variable list, set the value and label
                    if name in list(self.variable_dicts[header].keys()):
                        variable_object = self.variable_dicts[header][name]
                        variable_object.value.set(value)
                        variable_object.value_to_entry() # update the value of the entry field to display the loaded value as well
                        variable_object.valid = True  
                        status_label_widgets_dict[variable_object].configure(textvariable = variable_object.value, fg = "green")
                        print("variable [" + name + "] found, set value to " + str(value))
                except KeyError:
                    print("variable [" + name + "] not a part of variable list [" + variable_dict_title + "]")
            
            variable_list_file.close() # close the file
            tk.messagebox.showinfo("File loaded", "File loaded successfully")
            print("file loaded successfully")
        
        #if any errors occur during the try block, print the error type and message
        except:
            print("\nerror during file loading")
            print(sys.exc_info()[0].__name__)
            print(sys.exc_info()[1])
            return False