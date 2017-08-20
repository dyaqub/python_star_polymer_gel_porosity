import tkinter as tk

# initialized by the UI controller
# builds an input subview with a title, rows for input variables and update, load and save buttons
# initialized with a var_controller and a specific variable dictionary, variables are updated in the variable contorller when the submit button is pressed
class InputBlock:
    
    # initialized the master tkinter Frame, var controller, title, list of variable object instances. Initializes building the ID and packing sub-frames
    def __init__(self, master_frame, var_controller, title, variables_dict):
        print("initializing input block [" + title + "]")
        
        self.master_frame = master_frame
        self.var_controller = var_controller
        self.title = title
        self.variables_dict = variables_dict
        
        self.build_main_frame() # builds and packs all frames to the main frame, which is packed by the UI controller

    # builds the title and input (entry fields and buttons) frames and pack them
    def build_main_frame(self):
        print("building GUI input block [" + self.title + "]")
        
        # creates the tkinter Frame object holding the sub-frames (label, entry fields, buttons)
        self.main_frame = tk.Frame(self.master_frame, relief = tk.GROOVE, bd = 3)
        
        # build and pack the title frame of the input block
        self.build_title_frame()
        self.title_frame.pack()
        
        #  build and pack the entry fields frame of the input block 
        self.build_entry_fields()
        self.entry_fields_frame.pack()
        
        #  build and pack the buttons frame of the input block 
        self.build_buttons()
        self.buttons_frame.pack(pady = 5)
    
    # builds the frame for the title, adds a title label and packs it. Uses the title provided when initializing the input block object instance
    def build_title_frame(self):
        print("creating title frame for " + self.title)
        
        self.title_frame = tk.Frame(self.main_frame)
        
        tk.Label(self.title_frame, text = self.title, font = "Helvetica 16 bold").pack(pady = 5)
    
    # builds the entry fields and respective label widgets, and stores them in dictionaries {variable_object, widget}
    # packs the entry rows in grid layout with the following column sequence: description label, entry field, status label
    def build_entry_fields(self):
        print("creating input frame for [" + self.title + "]")
        
        self.entry_fields_frame = tk.Frame(self.main_frame)
        
        # create the empty dictionaries to store the widget objects as values with variable objects as keys
        self.description_label_widgets_dict = {}
        self.entry_field_widgets_dict = {}
        self.status_label_widgets_dict = {}
        
        row_counter = 0 # counts the grid position row for the variables
        
        # iterate through all variable objects in the variables list, create the widgets and store them in the respective dicts
        for var_name, var_object in self.variables_dict.items():
            
            # create and pack the description label with name and unit
            description_label_widget = tk.Label(self.entry_fields_frame, text= var_name + " [" + var_object.unit + "]")
            description_label_widget.grid(row = row_counter, column = 0, pady = 2)
            self.description_label_widgets_dict[var_object] = description_label_widget
            
            # create and pack the entry field
            entry_field_widget = tk.Entry(self.entry_fields_frame, textvariable = var_object.entry)
            entry_field_widget.grid(row = row_counter, column = 1, pady = 2, padx = 5)
            self.entry_field_widgets_dict[var_object] = entry_field_widget
            
            # create and pack the status label (orange font, status error value at start - see variable class for more info)
            status_label_widget = tk.Label(self.entry_fields_frame, textvariable = var_object.error, fg = "orange")
            status_label_widget.grid(row = row_counter, column = 2)
            self.status_label_widgets_dict[var_object] = status_label_widget
            
            row_counter += 1
    
    # builds and packs the button widgets to the button sub-frame, the commands link to local methods which in turn call to the var_controller
    def build_buttons(self):        
        print("creating buttons for [" + self.title +"]")
        
        self.buttons_frame = tk.Frame(self.main_frame)
        
        tk.Button(self.buttons_frame, text = "Update", command = self.update, padx = 10, pady = 2).grid(row = 0, column = 0, padx = 5)
        tk.Button(self.buttons_frame, text = "Save", command = self.save, padx = 10, pady = 2).grid(row = 0, column = 1, padx = 5)
        tk.Button(self.buttons_frame, text = "Load", command = self.load, padx = 10, pady = 2).grid(row = 0, column = 2, padx = 5)    
    
    # calls the variable controller to update the current variable list, passes the status labels dictionary for modification
    def update(self):
        self.var_controller.update_variable_list(self.title, self.status_label_widgets_dict)

    # calls the variable controller to save the current variables to a file
    def save(self):
        self.var_controller.write_to_file(self.title)
        
    # calls the variable controller to open a file, and passes the status label dictionary for modification
    def load(self):
        self.var_controller.load_file(self.title, self.status_label_widgets_dict)
        