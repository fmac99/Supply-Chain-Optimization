# -*- coding: utf-8 -*-
"""


@author: frank mccormick
"""



import pyomo.environ as pyo
from pyomo.core import *
from pyomo.opt import SolverFactory


class Optimizer:
	def __init__(self,load_file,sovler):

		self.optimizer_results = []
		self.load_file = load_file
		self.model_instance = 0
		self.sovler = solver


	def RunNetworkOptimization(self):
		#Can Use glpk, cbc, gurobi, cplex, etc.
		opt = pyo.SolverFactory(self.sovler)
		#creating model instance
		model = pyo.AbstractModel()

		#Sets and Parameters for model

		model.PC = pyo.Set()#Production Centers
		model.Hub = pyo.Set()# Hubs
		model.Line = pyo.Set() #Production Lines
		model.DC = pyo.Set() #Distribution Centers
		model.Products = pyo.Set() #Products
		model.production_costs =pyo.Param(model.PC,model.Line, model.Products, within = pyo.NonNegativeReals) #Production Per Case by Product
    model.prhub_trans_costs = pyo.Param(model.PC,model.Hub,model.Products, within = pyo.NonNegativeReals)#transportation costs from PC to Hubs
		model.trans_costs = pyo.Param(model.PC, model.DC, model.Products, within = pyo.NonNegativeReals)#transportation costs from PC to DC
		model.trans_costs_hub = pyo.Param(model.Hub, model.DC,model.Products, within = pyo.NonNegativeReals)#transportation costs Hub to DC
		model.demands=pyo.Param(model.DC,model.Products, within = pyo.NonNegativeIntegers)#Demands for each location. Index = (DC, Product)
		model.hub_demands = pyo.Param(model.DC,model.Products, within = pyo.NonNegativeIntegers)#Demands at each Distribution Location
		model.max_cap= pyo.Param(model.Line, within = pyo.NonNegativeIntegers)#Production line max capacity
		model.min_cap = pyo.Param(model.Line,within = pyo.NonNegativeIntegers)#Production line min production capacity
		model.direct_lane = pyo.Var(model.PC,model.DC,model.Products, domain = pyo.Binary)#Binary Variable for selecting a direct lane from a pc to a dc
		model.production_cases = pyo.Var(model.PC, model.Line, model.Products, domain = pyo.NonNegativeIntegers)#cases_produced at a given location, on a specific line
		model.prhub_cases = pyo.Var(model.PC,model.Hub, model.Products, domain = pyo.NonNegativeIntegers)# cases produced for a hub
		model.hub_lane = pyo.Var(model.Hub,model.DC,model.Products, domain = pyo.Binary)#Binary Variable for selecting a direct lane from a hub to a dc
    
		def ObjectiveFunction1(model):
			 return (sum(model.production_costs_variable[p,l,k]*model.production_cases[p,l,k] for p in model.PC for l in model.Line for k in model.Products)
             + sum(model.production_costs_fixed[p]*use_pc[p] for p in model.PC)
				     + sum(model.prhub_trans_costs[p,h,k]*model.prhub_cases[p,h,k] for p in model.PC for h in model.Hub for k in model.Products)
				     + sum(model.trans_costs[p,j,k]* model.direct_lane[p,j,k] *model.demands[j,k] for p in model.PC for j in model.DC for k in model.Products)
				     +sum(model.trans_costs_hub[h,j,k]*model.hub_lane[h,j,k] *model.hub_demands[j,k] for h in model.Hub for j in model.DC for k in model.Products))#objective funtion to be optimized, minimize total cost.
		model.Obj= pyo.Objective(rule=ObjectiveFunction1)


		# Activate All Hubbed Demand Locations and allow one hub site
		def Hub_Source_Activation(model,DC,Products):
			 return  sum(model.hub_lane[h,DC,Products] for h in model.Hub) == 1
		model.ActivateSource = pyo.Constraint(model.DC, model.Products, rule=Hub_Source_Activation)

		# Activate All Direct Demand Locations and allow one production site
		def Direct_Source_Activation(model,DC,Products):
			 return sum(model.direct_lane[p,DC,Products] for p in model.PC)  == 1
		model.SingleSource1 = pyo.Constraint(model.DC, model.Products, rule=Direct_Source_Activation)


		# Conservation of flow for available cases on a specific direct lane
		def DirectConsFlow(model,PC,Products):
		   return sum(model.demands[j, Products]*model.direct_lane[PC,j,Products] for j in model.DC) == sum(model.production_cases[PC,l,Products]  for l in model.Line) 

		model.conserve_flow_direct = pyo.Constraint(model.PC,model.Products,rule = DirectConsFlow)

		# Conservation of flow for available cases on for production centers to hubs
		def PCHubConsFlow(model,PC,Products):
			 return sum(model.prhub_cases[PC,h,Products] for h in model.Hub) == sum(model.production_cases[PC,l,Products]  for l in model.Line) 
		model.conserve_flow_pc_h = pyo.Constraint(model.PC,model.Products,rule=PCHubConsFlow)

		# Conservation of flow for available cases on for production centers to hubs
		def HubDCConsFlow(model,Hub,Products):
			 return sum(model.hub_demands[j, Products]*model.hub_lane[Hub,j,Products] for j in model.DC) == sum(model.prhub_cases[p,Hub,Products]  for p in model.PC) 
		model.conserve_flow_h_dc = pyo.Constraint(model.Hub,model.Products, rule=HubDCConsFlow)

		#maximum production capacity by line
		def constraint2(model, Line):
			 return sum(model.production_cases[p, Line,k]  for p in model.PC for k in model.Products) <= model.supply[Line] 
		model.constraintsupply = pyo.Constraint(model.Line, rule = constraint2)

		#minimum production capacity by line
		def constraint3(model, Line):
			 return sum(model.production_cases[p,Line,k] for p in model.PC for k in model.Products)  >=model.minimum[Line]
		model.constraintmins = pyo.Constraint(model.Line, rule = constraint3)


		#Load Dat file into program, other formats are acceptable as well
		data = pyo.DataPortal()
		data.load(filename =self.load_file,param=(model.prhub_trans_costs,model.trans_costs,model.production_costs,model.demands,model.hub_demands,model.max_cap, model.min_cap,model.trans_cost_hub), index =(model.PC,model.Hub,model.Line,model.DC,model.Products))

		#Create Model Instance
		self.model_instance = model.create_instance(data)
		self.optimizer_results = opt.solve(self.model_instance)
		#Return Optimizer Results
		return self.optimizer_results

	#Write Results Files
	def WriteResults(filename,column_header_list,iterator_list):   
		with open(filename,'w') as f:
		    f.write(column_header_list)
		    for p in iterator_list[0]:
		           for j in iterator_list[1]:
		                for k in iterator_list[2]:
		                     f.write("{0},{1},{2},{3}\n".format(p,j,k,iterator_list[3][p,j,k].value))
		f.close()



