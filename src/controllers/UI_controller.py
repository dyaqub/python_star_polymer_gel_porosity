import UI_elements.input_block as input_block
import UI_elements.plot_frame as plot_frame

#the UI controller deals with all UI aspects based on the Tkinter module
#it uses a master with subframes for different views in the program 
#the UIcontroller is initialized with a var controller giving it access to the vars required for displaying and editing vars
class UIcontroller():
    
    #creates the tkinter root, builds and packs all input blocks based on variable lists from the var contorller
    def __init__(self, root, var_controller, calc_controller):
        print("initializing GUI controller")
        
        #master GUI frame
        self.master = root
        
        #var controller creates variable objects (NOTE: must happen after Tk() master/root is initialized becayse variables use tkinter class vars!)
        self.var_controller = var_controller
        
        self.calc_controller = calc_controller
        
        #starts the methods creating the frames/views holding the respective UI parts, based on the variable lists in the variable controller
        #create the input UI blocks based on the variable lists in the variable controller lists, saves them into a dictionary {title : input_block}
        print("creating GUI input frames")
        
        #creates the variable input blocks and adds them to a grid layout in column 0
        self.input_blocks = {}
        row_counter = 0
        for title, var_dict in self.var_controller.variable_dicts.items():
            self.input_blocks[title] = input_block.InputBlock(self.master, self.var_controller, title, var_dict)
            self.input_blocks[title].main_frame.grid(column = 0, row = row_counter, padx = 50, pady = 20)
            row_counter += 1
            
        #create the Mc solve plot subframe
        self.plot_frame = plot_frame.PlotFrame(self.master, self.calc_controller)
        self.plot_frame.main_frame.grid(column = 1, row = 0, padx = 50)
    
    #starts the main loop for the tkinter UI master/root
    def start_UI(self):
        self.master.mainloop()