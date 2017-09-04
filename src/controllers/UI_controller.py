import UI_elements.input_block as input_block
import UI_elements.plot_frame as plot_frame
import tkinter as tk

# the UI controller deals with all UI aspects based on the Tkinter module
# it uses a Tkinter master (Tk()) with subframes for different views in the program 
# the UIcontroller is initialized with a var controller giving it access to the variable dictionaries required for displaying and editing var input blocks
class UIcontroller():
    
    # creates the tkinter root, builds and packs all input blocks based on variable lists from the var contorller
    def __init__(self, var_controller, calc_controller):
        print("initializing GUI controller")
        
        # NOTE: variable object instances cannot be created until the tkinter.Tk() master/root is initialized because it builds on tkinter class variables
        # therefore the variable controller variables are created after .Tk() is called 
        print("initializing GUI root / master frame")
        self.master = tk.Tk() # top level Frame, which also can start the program
        self.master.title("Calculate mesh size from swelling") # sets the title displayed in the window frame bar
        
        self.var_controller = var_controller
        self.var_controller.create_variables()
        
        self.calc_controller = calc_controller
        
        # controller cretaes a left (variable input blocks) and right (plot and results) frame 
        self.left_frame = tk.Frame(self.master)
        self.right_frame = tk.Frame(self.master)
        
        # create the input UI blocks based on the variable lists in the variable controller lists, saves them into a dictionary {title : input_block}
        print("creating GUI variable input frames")
        
        self.input_blocks = {}
        # create an input_block object for each variable dictiornary in the var controller
        for title, var_dict in self.var_controller.variable_dicts.items(): 
            self.input_blocks[title] = input_block.InputBlock(self.left_frame, self.var_controller, title, var_dict)
            self.input_blocks[title].main_frame.pack(fill = tk.X)
            
        # create the Mc solve plot and results subframe
        self.plot_frame = plot_frame.PlotFrame(self.right_frame, self.calc_controller, self.var_controller)
        self.plot_frame.main_frame.pack()
        
        # arranges the left and right frames in a grid layout
        self.left_frame.grid(column = 0, row = 0, sticky = tk.N)
        self.right_frame.grid(column = 1, row = 0, sticky = tk.N)
    
    # starts the main loop for the tkinter UI master/root
    def start_UI(self):
        print("starting GUI")
        
        self.master.mainloop()