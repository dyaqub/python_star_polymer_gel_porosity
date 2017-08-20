import matplotlib.backends.backend_tkagg
import tkinter as tk
from tkinter import messagebox # required for messagebox to work, even with tkinter/tk.messagebox as messagebox import isn't part of tkinter __init__

#responsible for building the UI elements surrounding the Mc equation plot
#has access to the calculation controller from which the actual plot is retrieved (calc_controller has access to all variables and holds calculation methods)
class PlotFrame:
    
    def __init__(self, master, calc_controller):
        matplotlib.rcParams.update({'font.size': 8})
        
        #set the tk root to that passed by the UI controller
        self.master = master
        self.calc_controller = calc_controller
        
        #create the main frame for the plot
        self.main_frame = tk.Frame(master, relief = tk.GROOVE, bd = 3)
        
        #build and pack the title subframe
        #self.build_title_frame()
        #self.title_frame.pack()
        
        #build and pack the equation subframe
        self.build_plot_frame()
        self.plot_frame.pack()
        
        #build and pack the button frame below the plot frame
        self.build_buttons_frame()
        self.button_frame.pack()
        self.build_results_grid()
    
    #prepares the sub-frame holding the title label. the title_frame is packed in the init method of the PlotFrame instance
    def build_title_frame(self):
        self.title_frame = tk.Frame(self.main_frame)
        self.title_label = tk.Label(self.title_frame, text = "Equation for Mc", font = "Helvetica 16 bold")
        self.title_label.pack(pady = 5)
    
    #prepares the sub-frame holding the plot created using the matplotlib module
    def build_plot_frame(self):
        self.plot_frame = tk.Frame(self.main_frame)
        
        #get the empty plot frame from the calculation controller and store as an instance attribute
        self.create_empty_Mc_plot()
        
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.Mc_plot_figure, master = self.plot_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()
        self.canvas._tkcanvas.pack()
        
    #creates the buttons below the plot sub-frame
    def build_buttons_frame(self):
        self.button_frame = tk.Frame(self.main_frame)
        
        #creates the update button, which has the update method as a command
        self.update_button = tk.Button(self.button_frame, text = "update plot and results", command = self.update_plot_and_results)
        self.update_button.pack(pady = 5)
    
    def build_results_grid(self):
        self.results_frame = tk.Frame(self.main_frame, relief = tk.GROOVE, bd = 3)
        
        tk.Label(self.results_frame, text = "Molecular weight between crosslinks").grid(column = 0, row = 0)
        tk.Label(self.results_frame, text = "square-root average end-to-end distance").grid(column = 0, row = 1)
        tk.Label(self.results_frame, text = "mesh size").grid(column = 0, row = 2)
        
        tk.Label(self.results_frame, text = "[g/mol]").grid(column = 2, row = 0)
        tk.Label(self.results_frame, text = "[nm]").grid(column = 2, row = 1)
        tk.Label(self.results_frame, text = "[nm]").grid(column = 2, row = 2)
        
        self.label_Mc = tk.Label(self.results_frame)
        self.label_r0 = tk.Label(self.results_frame)
        self.label_mesh_size = tk.Label(self.results_frame)
        self.label_Mc.grid(column = 1, row = 0)
        self.label_r0.grid(column = 1, row = 1)
        self.label_mesh_size.grid(column = 1, row = 2)
        
        self.results_frame.pack(fill = tk.X)
        
    def create_empty_Mc_plot(self):
        #creates the matplotlib figure, figsize=(width, height) in unknown units
        self.Mc_plot_figure = matplotlib.figure.Figure(figsize=(5, 3), dpi=100)    
        
        #adds a subplot to the figure
        Mc_plot = self.Mc_plot_figure.add_subplot(111)
        Mc_plot.set_ylim([0,0.002])
        Mc_plot.set_xlim([0, 40000])
        Mc_plot.tick_params(labelsize=6)
        
        Mc_plot.set_xlabel('Mc [g/mol]')
        Mc_plot.set_ylabel('1/Mc [mol/g]')
        
        #trims white edges from the plot figure. Note that .set_tight_layout(true) is preferable to .tight_layout(), which can only use the Agg renderer and throws a warning
        self.Mc_plot_figure.set_tight_layout(True)
        
    #update
    def update_plot_and_results(self):
        print("updating plot")
        
        #raise an error and cancel if not all variable objects have a valid value
        if not self.calc_controller.var_controller.all_variables_valid():
            print("not all variables valid, cancelling plot and results update")
            tk.messagebox.showerror("Variable error", "Not all current variable values are valid.")
            return False
        
        #updates the plot graphs
        self.update_plot()

        #update the results calculation and values        
        self.update_results()
        
    #updates the results labels
    def update_results(self):
        print("updating results")
        
        #call the calc controller to re-calculate Mc and the final results
        self.calc_controller.solve_for_Mc()
        self.calc_controller.calculate_results()
        
        #convert floating point numbers to two decimals
        Mc_str = "%.2f" % self.calc_controller.real_Mc
        r0_str = "%.2f" % self.calc_controller.r0_average
        mesh_str = "%.2f" % self.calc_controller.mesh_size
        
        self.label_Mc.configure(text = Mc_str, fg = "green")
        self.label_r0.configure(text = r0_str, fg = "green")
        self.label_mesh_size.configure(text = mesh_str, fg = "green")
    
    #creates the plot figure but calls to the calculation controller to add the actual plot graphs
    def update_plot(self):
        
       
        #creates the matplotlib figure, figsize=(width, height) in unknown units
        self.Mc_plot_figure = matplotlib.figure.Figure(figsize=(5, 3), dpi=100)
        
        Mc_plot = self.Mc_plot_figure.add_subplot(111)
        Mc_plot.set_ylim([0,0.002])
        
        Mc_plot.set_xlabel('Mc [g/mol]')
        Mc_plot.set_ylabel('1/Mc [mol/g]')
        
        self.calc_controller.add_graphs_to_plot(Mc_plot)
        
        self.Mc_plot_figure.set_tight_layout(True)
        
        #clears the canvas and packs the plot again
        self.canvas.get_tk_widget().pack_forget()
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.Mc_plot_figure, master = self.plot_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()
        self.canvas._tkcanvas.pack()
        


    
        
    
        
        
        