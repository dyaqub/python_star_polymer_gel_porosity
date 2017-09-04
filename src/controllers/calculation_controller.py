import sympy
from sympy.abc import x
import numpy

# the calculation controller is responsible for solving the equaitons for Mc numerically and addings graphs to the Mc plot created by the respective UI element
# after solving Mc it furthermore calculates the final results (mesh size)
class CalculationController:
    
    def __init__(self, var_controller):
        self.var_controller = var_controller # calculation controller has access to the variable controller because it needs all variables for plots and solvin     
    
    # loads the variables from the variable object dictionaries in the variable controller and assigns them to calc_controller instance attributes
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
    
    # takes a matplotlib subplot as an argument and adds to it the graphs for the left and right equations in the Mc calculation
    def add_graphs_to_plot(self, Mc_plot):
        
        self.load_variables()
        
        self.Mc_range = numpy.arange(0.0, self.Ma+5000, 1) # sets the range to the arm molecular weight plus a margin
        Mc_plot.set_xlim([0, self.Ma+5000]) # note this is the plot axis limit, and Mc_range is the graph drawing x-range
        
        # left side using the Mc_range for x
        equation_left = 1.0/self.Mc_range
        # equation right side. Note that numpy .log = ln, whereas .log10 = log
        equation_right = 1.0/self.Ma - (self.vp/(self.v2r*self.V1)) * ( self.X*self.v2s*self.v2s + numpy.log(1.0-self.v2s) + self.v2s ) /(
                         (self.v2s/self.v2r)**(1.0/3.0) - ((2.0/self.F1) + 1.0/((self.Ma/self.Mc_range-1)*self.F2))*(self.v2s/self.v2r) )
        # may throw a RunTimeWarning - divide by zero, safe to ignore
        print("solving the equation may have throw a Runtime warning - divide by zero. This is safe to ignore")
        
        # plot the graphs created to the matplotlib subplot
        Mc_plot.plot(self.Mc_range, equation_left)
        Mc_plot.plot(self.Mc_range, equation_right)
    
    # solve the equation numerically for Mc, sets the list of solutions and sets the first (lowest) solution as the real value used for calculation
    def solve_for_Mc(self):
        print("starting Mc calculation")
        
        # the Mc solutions list is set to empty every time the method is called
        self.solutions_Mc = []
        
        ##################################################
        #
        #    This is the actual solving of the equation
        #
        #    Note that it solves the equation for zero, thus 1/Mc (here Mc = x) moves to the right side of the equation as - 1/Mc
        #
        #    As nsolve only gives one solution, it is solved multiple times with different guess values, and the solutions are added to a list
        #
        #    The arm molecular weight is always a solution, but the smaller solution is the real one required for the calculation, set as .real_Mc
        #
        ##################################################
        
        # the function with 1/Mc moved to the other side so y = 0 can be found by nsolve
        mc_calc_function = 1.0/self.Ma - 1.0/x - (self.vp/(self.v2r*self.V1)) * (self.X*self.v2s*self.v2s + sympy.ln(1.0-self.v2s) + self.v2s) / (
                           (self.v2s/self.v2r)**(1.0/3.0) - ((2.0/self.F1) + 1.0/( (self.Ma/x-1) * self.F2)) * (self.v2s/self.v2r) )

        # x_guesses which are the starting points for which the equation will be solved numerically
        x_guesses = [1, 100, 1000, 10000, 100000, 10000000]
        for x_guess in x_guesses:
            solution = sympy.nsolve(mc_calc_function, x_guess)
            if float(solution) not in self.solutions_Mc:
                self.solutions_Mc.append(float(solution))
        
        # the Mc used for calculations is the smallest value, because it can never be higher than the polymer arm molecular weight which is always a solution
        self.real_Mc = self.solutions_Mc[0]
        self.var_controller.manual_Mc.entry.set(self.real_Mc)
     
        print("Mc solutions found (g/mol): " + str(self.solutions_Mc))
        print("using value " + str(self.real_Mc))
        
    # calculate all other results after Mc is known. The most important result is mesh size but the r0 average end-to-end distance is calculated as well
    def calculate_results(self):
        print("calculating final results")
        
        print("calculating r0_average")
        self.r0_average = self.l * ((2 * self.real_Mc / self.Mr)**0.5) * (self.Cn ** 0.5)
        print("calculated square-root-average end-to-end distance r0 = " + str(self.r0_average))
        
        print("calculating mesh size")        
        self.mesh_size = (self.v2s ** (-1.0/3.0)) * self.r0_average
        print("calculated mesh size = " + str(self.mesh_size))