import sympy
from sympy.abc import x
import matplotlib
import numpy

class CalculationController:
    
    def __init__(self, var_controller):
        self.var_controller = var_controller # calculation controller has access to the variable controller because it needs all variables for plots and solving
        
        #set the variables resulting from calculations later
        self.solutions_Mc = []
        self.real_Mc = 0.0
        self.r0_average = 0.0
        self.mesh_size = 0.0
        
    
    #loads the variables from the variable object dictionaries in the variable controller and assigns them to the instance
    def load_variables(self):
        
        self.constants = self.var_controller.variable_dicts["Polymer Constants"]
        self.network = self.var_controller.variable_dicts["Network Architecture"]
        self.swelling = self.var_controller.variable_dicts["Experimental Swelling"]
        
        self.Mr = self.constants["repeating unit MW"].value.get()
        self.l = self.constants["average bond length"].value.get()
        self.Cn = self.constants["characteristic ratio"].value.get()
        self.X = self.constants["Flory parameter"].value.get()
        self.vp = self.constants["specific volume polymer"].value.get()
        self.V1 = self.constants["swelling agent molar volume"].value.get()
        
        self.Ma = self.network["arm molecular weight"].value.get()
        self.F1 = self.network["degree of crosslinking in arm"].value.get()
        self.F2 = self.network["degree of crosslinking in core"].value.get()
        
        self.v2s = self.swelling["polymer volume fraction equilibrium"].value.get()
        self.v2r = self.swelling["polymer volume fraction synthesis"].value.get()
        
    
    #creates an empty plot to be shown before variables are loaded
    def create_empty_Mc_plot(self):
        #creates the matplotlib figure, figsize=(width, height) in unknown units
        Mc_plot_figure = matplotlib.figure.Figure(figsize=(7, 4), dpi=100)
        #adds a subplot to the figure
        Mc_plot = Mc_plot_figure.add_subplot(111)
        Mc_plot.set_ylim([0,0.02])
        Mc_plot.set_xlim([0, 20000])
        #sets the range?
        self.Mc_range = numpy.arange(0.0, 20000.0, 1)
        
        Mc_plot.set_title('Corssing lines (continuous) are solutions for Mc')
        Mc_plot.set_xlabel('Mc [g/mol]')
        Mc_plot.set_ylabel('1/Mc [mol/g]')
        
        return Mc_plot_figure
    
    #updates the plot
    def update_plot(self):
        self.load_variables()
        
        #creates the matplotlib figure, figsize=(width, height) in unknown units
        Mc_plot_figure = matplotlib.figure.Figure(figsize=(7, 4), dpi=100)
        #adds a subplot to the figure
        Mc_plot = Mc_plot_figure.add_subplot(111)
        Mc_plot.set_ylim([0,0.001])
        
        #left side
        equation_left = 1.0/self.Mc_range
        #equation right side. Note that numpy .log = ln, whereas .log10 = log
        equation_right = 1.0/self.Ma - (self.vp/(self.v2r*self.V1)) * ( self.X*self.v2s*self.v2s + numpy.log(1.0-self.v2s) + self.v2s ) /(
                         (self.v2s/self.v2r)**(1.0/3.0) - ((2.0/self.F1) + 1.0/((self.Ma/self.Mc_range-1)*self.F2))*(self.v2s/self.v2r) )
        #may throw a RunTimeWarning - divide by zero, safe to ignore
        
        Mc_plot.plot(self.Mc_range, equation_left)
        Mc_plot.plot(self.Mc_range, equation_right)
        
        Mc_plot.set_title('Corssing lines (continuous) are solutions for Mc')
        Mc_plot.set_xlabel('Mc [g/mol]')
        Mc_plot.set_ylabel('1/Mc [mol/g]')
        
        self.solve_for_Mc()
        self.calculate_results()
        
        return Mc_plot_figure
    
    #create the plot showing the Mc equation using the matplotlib module
    def create_Mc_plot(self):
    
        #creates the matplotlib figure, figsize=(width, height) in unknown units
        figure = matplotlib.figure.Figure(figsize=(7, 4), dpi=100)
        #adds a subplot to the figure
        a = figure.add_subplot(111)
        a.set_ylim([0,0.001])
        #sets the range?
        Mc = numpy.arange(500.0, 20000.0, 1)
        
        #left side
        equation_left = 1.0/Mc
        #equation right side. Note that numpy .log = ln, whereas .log10 = log
        equation_right = 1.0/self.Ma - (self.vp/(self.v2r*self.V1)) * ( self.X*self.v2s*self.v2s + numpy.log(1.0-self.v2s) + self.v2s ) /(
                         (self.v2s/self.v2r)**(1.0/3.0) - ((2.0/self.F1) + 1.0/((self.Ma/Mc-1)*self.F2))*(self.v2s/self.v2r) )
        #may throw a RunTimeWarning - divide by zero, safe to ignore

        #plots the equations to the subplot
        a.plot(Mc, equation_left)
        a.plot(Mc, equation_right)
        a.set_title('Corssing lines (continuous) are solutions for Mc')
        a.set_xlabel('Mc [g/mol]')
        a.set_ylabel('1/Mc [mol/g]')
        
        return figure
    
    #solve Mc values
    def solve_for_Mc(self):
        print("starting Mc calculation")
        
        #the Mc solutions list is set to empty every time the method is called
        self.solutions_Mc = []
        
        #solves for y = 0, x = Mc
        ##################################################
        #
        #    This is the actual solving of the equation
        #
        #    Note that it solves the equation for zero, thus 1/Mc (here Mc = x) moves to the right side of the equation as - 1/Mc
        #
        #    As nsolve only gives one solution, it is solved multiple times with different guess values, and the solutions are added to a list
        #
        ##################################################
        
        #the function with 1/Mc moved to the other side so zero can be found by nsolve
        mc_calc_function = 1.0/self.Ma - 1.0/x - (self.vp/(self.v2r*self.V1)) * (self.X*self.v2s*self.v2s + sympy.ln(1.0-self.v2s) + self.v2s) / (
                           (self.v2s/self.v2r)**(1.0/3.0) - ((2.0/self.F1) + 1.0/( (self.Ma/x-1) * self.F2)) * (self.v2s/self.v2r) )

        #x_guesses which are the starting points for which the equation will be solved numerically
        x_guesses = [1, 100, 1000, 10000, 100000, 10000000]
        for x_guess in x_guesses:
            solution = sympy.nsolve(mc_calc_function, x_guess)
            if float(solution) not in self.solutions_Mc:
                self.solutions_Mc.append(float(solution))
        
        #the Mc used for calculations is the smallest value, because it can never be higher than the polymer arm molecular weight which is always a solution
        #TODO: exception catching for no solution / only arm MW solution
        self.real_Mc = self.solutions_Mc[0]

        #returns the solutions        
        print("Mc solutions found (g/mol): " + str(self.solutions_Mc))
        print("using value " + str(self.real_Mc))
        return self.solutions_Mc
        
    #calculate all other results after Mc is known
    def calculate_results(self):
        
        print("calculating r0_average")
        print("bond length l = " + str(self.l))
        print("MW between crosslinks Mc = " + str(self.real_Mc))
        print("MW arm Mr = " + str(self.Mr))
        print("characteristic ratio Cn = " + str(self.Cn))
        self.r0_average = self.l * ((2 * self.real_Mc / self.Mr)**0.5) * (self.Cn ** 0.5)
        print("calculated r0 = " + str(self.r0_average))
        
        print("calculating mesh size")        
        print("swollen polymer vol fraction v2s = " + str(self.v2s))
        print("end-to-end distance r0_average = " + str(self.r0_average))
        self.mesh_size = (self.v2s ** (-1.0/3.0)) * self.r0_average
        print("calculated mesh size = " + str(self.mesh_size))
        
        