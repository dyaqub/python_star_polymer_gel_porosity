import matplotlib.backends.backend_tkagg
import tkinter as tk
from tkinter import messagebox # required for messagebox to work, even with tkinter/tk.messagebox as messagebox import isn't part of tkinter __init__

# responsible for building the UI elements surrounding the Mc equation plot and the results frame
# has access to the calculation controller from which the actual plot is retrieved (calc_controller has access to all variables and holds calculation methods)
class PlotFrame:
    
    def __init__(self, master, calc_controller):
        print("initializing plot and results frame")
        
        matplotlib.rcParams.update({'font.size': 8}) # sets the font size for all matplotlib text. Note that the axes font size is later overriden and smaller
        
        self.master = master # tkinter root passed from UI controller
        self.calc_controller = calc_controller
        
        self.build_main_frame() # builds all sub-frames and pack them to the main frame, which in turn is packed by the UI controller
        
    # builds and packs the sub-frames (plot, buttons, results) for the plot_results main frame
    def build_main_frame(self):
        print("creating plot and results frame")
        
        # create the main frame for the plot. Note that all sub-frames will be packed to this frame, but the main_frame itself is packed by the UI controller
        self.main_frame = tk.Frame(self.master, relief = tk.GROOVE, bd = 3)
        
        # build and pack the plot subframe which has the matplotlib plot on a canvas
        self.build_plot_frame()
        self.plot_frame.pack()
        
        # build and pack the button frame below the plot frame
        self.build_buttons_frame()
        self.button_frame.pack()
        
        # build and pack the results frame below the update button frame
        self.build_results_frame()
        self.results_frame.pack(fill = tk.X)
    
    # creates the sub-frame holding the plot created using the matplotlib module
    def build_plot_frame(self):
        print("creating plot frame")
        
        self.plot_frame = tk.Frame(self.main_frame)
        
        # when the plot_results frame is first built, create a canvas with an empty plot
        self.create_empty_Mc_plot()
        
        # add the matplotlib figure to the canvas and pack it
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.Mc_plot_figure, master = self.plot_frame)
        self.canvas._tkcanvas.pack()
        
    # creates a sub-frame with the button(s) below the plot sub-frame
    def build_buttons_frame(self):
        print("creating plot and results update button")
        
        self.button_frame = tk.Frame(self.main_frame)
        
        # creates the update button, which has the method to update both the plot and the results as the command
        self.update_button = tk.Button(self.button_frame, text = "update plot and results", command = self.update_plot_and_results)
        self.update_button.pack(pady = 5) # packs te button to the button sub-frame, which is packed in __init__ to the main frame by the UI element
    
    # creates a sub frame with final results of the calculations as a grid layout
    def build_results_frame(self):
        print("creating results frame")
        
        self.results_frame = tk.Frame(self.main_frame, relief = tk.GROOVE, bd = 3)
        
        tk.Label(self.results_frame, text = "Molecular weight between crosslinks").grid(column = 0, row = 0)
        tk.Label(self.results_frame, text = "square-root average end-to-end distance").grid(column = 0, row = 1)
        tk.Label(self.results_frame, text = "mesh size").grid(column = 0, row = 2)
        
        tk.Label(self.results_frame, text = "[g/mol]").grid(column = 2, row = 0)
        tk.Label(self.results_frame, text = "[nm]").grid(column = 2, row = 1)
        tk.Label(self.results_frame, text = "[nm]").grid(column = 2, row = 2)
        
        # the result labels are stored as attributes so they can be accessed and updated
        self.label_Mc = tk.Label(self.results_frame)
        self.label_r0 = tk.Label(self.results_frame)
        self.label_mesh_size = tk.Label(self.results_frame)
        self.label_Mc.grid(column = 1, row = 0)
        self.label_r0.grid(column = 1, row = 1)
        self.label_mesh_size.grid(column = 1, row = 2)
        
    # creates a matplotlib figure and adds an empty subplot to it
    def create_empty_Mc_plot(self):
        print("creating empty plot")
        
        # creates the matplotlib figure, figsize = (width, height)
        self.Mc_plot_figure = matplotlib.figure.Figure(figsize = (5, 3), dpi = 100)    
        
        # adds a subplot to the figure but doesn't plot a graph
        self.Mc_plot = self.Mc_plot_figure.add_subplot(111)
        self.Mc_plot.set_ylim( [0,0.002] )
        self.Mc_plot.set_xlim( [0, 40000] ) # this is overridden when the plot is updates and the calculation controller plots the graphs
        self.Mc_plot.tick_params(labelsize = 6) # sets the tick label font size for both axes
        self.Mc_plot.set_xlabel('Mc [g/mol]')
        self.Mc_plot.set_ylabel('1/Mc [mol/g]')
        
        # trims white edges from the plot figure
        # Note that .set_tight_layout(true) is preferable to .tight_layout(), which can only use the Agg renderer and throws a warning
        self.Mc_plot_figure.set_tight_layout(True)
        
    # update both the matplotlib plot and the results frame
    def update_plot_and_results(self):
        print("updating plot")
        
        # popup an error message and cancel if not all variable objects have a valid value
        if not self.calc_controller.var_controller.all_variables_valid():
            
            print("not all variables valid, cancelling plot and results update")
            tk.messagebox.showerror("Variable error", "Not all current variable values are valid.")
            return False
        
        self.update_plot()       
        self.update_results()
    
    # creates a new empty plot figure and calls to the calculation controller to add the actual plot graphs
    def update_plot(self):
        print("updating Mc plot")
       
        self.create_empty_Mc_plot() # first create the empty plot
        
        self.calc_controller.add_graphs_to_plot(self.Mc_plot) # calc controller plots the graphs to the subframe Mc_plot
        
        # clears the canvas and packs the plot again
        self.canvas.get_tk_widget().pack_forget()
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.Mc_plot_figure, master = self.plot_frame)
        self.canvas._tkcanvas.pack()
        
    # calls the calculation controller to re-calculate Mc and the final results, and updates the result labels
    def update_results(self):
        print("updating results")
        
        self.calc_controller.solve_for_Mc()
        self.calc_controller.calculate_results()
        
        # update the result labels, convert floating point numbers to strings with two decimals
        self.label_Mc.configure(text = "%.2f" % self.calc_controller.real_Mc, fg = "green")
        self.label_r0.configure(text = "%.2f" % self.calc_controller.r0_average, fg = "green")
        self.label_mesh_size.configure(text = "%.2f" % self.calc_controller.mesh_size, fg = "green")
