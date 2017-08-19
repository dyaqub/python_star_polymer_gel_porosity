import tkinter as tk

#initialized by the UI controller
#builds an input subview with a title, rows for input variables and update, load and save buttons
#initialized with a variable list and var_controller, variables are updated in the variable contorller when the submit button is pressed
class InputBlock:
    
    #initialized the master tkinter Frame, var controller, title, list of variable object instances. Initializes building the ID and packing sub-frames
    def __init__(self, master_frame, var_controller, title, variables_dict):
        self.master_frame = master_frame
        self.var_controller = var_controller
        self.title = title
        self.variables_dict = variables_dict
        
        self.build_input_block_frame() # 

    #builds the title and input (entry fields and buttons) frames and pack them
    def build_input_block_frame(self):
        print("building GUI input block [" + self.title + "]")
        
        #creates the tkinter Frame object holding the label frame and entry_fields_labels frame
        self.main_frame = tk.Frame(self.master_frame, relief = tk.GROOVE, bd = 3)
        
        #create the frame holding the titlem part of the input block main frame
        self.build_label_frame()
        self.title_frame.pack()
        
        #creates a grid frame as a part of the main frame, grid layout is 3 columns wide
        #holds the entry rows with the following column sequence: Left description label, middle entry field, right status label
        self.entry_frame = tk.Frame(self.main_frame)
        self.build_entry_fields()
        self.build_buttons()
        self.entry_frame.pack()
    
    #builds the frame for the label, adds a ttitle and packs it. uses the title provided when initializing the object instance
    def build_label_frame(self):
        print("creating title frame for " + self.title)
        
        #create a label for a title of this view in a sub-frame
        self.title_frame = tk.Frame(self.main_frame)
        tk.Label(self.title_frame, text = self.title, font = "Helvetica 16 bold", pady = 5).pack()
    
    #builds the entry fields and respective label widgets, and stores them in a dict {variable_object, widget}
    def build_entry_fields(self):
        print("creating input frame for [" + self.title + "]")
        
        #create the empty dictionaries to store the widget objects as values with variable objects as keys
        self.description_label_widgets_dict = {}
        self.entry_field_widgets_dict = {}
        self.status_label_widgets_dict = {}
        row_counter = 0 # counts the grid position row for the variables
        
        #iterate through all variable objects in the variables list
        for var_name, var_object in self.variables_dict.items():
            
            #create the description label with name and unit, store the widget in the respective dict
            description_label_widget = tk.Label(self.entry_frame, text= var_name + " [" + var_object.unit + "]")
            description_label_widget.grid(row = row_counter, column = 0, pady = 2)
            self.description_label_widgets_dict[var_object] = description_label_widget
            
            #create the entry field, store the widget in the respective dict
            entry_field_widget = tk.Entry(self.entry_frame, textvariable = var_object.entry)
            entry_field_widget.grid(row = row_counter, column = 1, pady = 2, padx = 5)
            self.entry_field_widgets_dict[var_object] = entry_field_widget
            
            #create the status label (orange font, status error value at start - see variable class for more info), store widget in the respective dict
            status_label_widget = tk.Label(self.entry_frame, textvariable = var_object.error, fg="orange")
            status_label_widget.grid(row = row_counter, column = 2)
            self.status_label_widgets_dict[var_object] = status_label_widget
            
            row_counter += 1
    
    #build the button widgets, and links the functions to the var_controller
    def build_buttons(self):
        print("creating buttons for [" + self.title +"]")
        #the buttons are positions below the entry field rows in the entry_frame grid layout
        buttons_grid_row = len(self.variables_dict) 
        
        tk.Button(self.entry_frame, text = "Update", command = self.update, padx = 10, pady = 2).grid(row = buttons_grid_row, column = 0, pady = 5)
        tk.Button(self.entry_frame, text = "Save", command = self.save, padx = 10, pady = 2).grid(row = buttons_grid_row, column = 1)
        tk.Button(self.entry_frame, text = "Load", command = self.load, padx = 10, pady = 2).grid(row = buttons_grid_row, column = 2)    
    
    #calls the variable controller to update the current variable list, passes the status label for modification
    def update(self):
        self.var_controller.update_variable_list(self.title, self.status_label_widgets_dict)

    #calls the variable controller to save the current variables to a file
    def save(self):
        self.var_controller.write_to_file(self.title)
        
    #calls the variable controller to open a file
    def load(self):
        self.var_controller.load_file(self.title, self.status_label_widgets_dict)
        