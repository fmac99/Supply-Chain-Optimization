# Supply-Chain-Optimization
A repository of Supply Chain Optimization Programs


# Network Optimization Current Model Details:

This program solves the assignment problem for a supply chain network with Production Centers, Hubs and Distribution Centers. The objective function minimizes total network cost.  A couple of things to note here is that the production cost is a flat cost/unit. I am working on building a more robust version that breaks that out to fixed production cost and variable production costs. I also have not modeled customer deliveries from the dc which is another important problem when looking to minimize cost in a supply chain. I would use the minimum production capacity if you want to ensure each production line has a minimum amount of work hours. 

# Future updates:
1. Model production capacity in hours not units
2. Add a slack variable for production capacity to allow you to run "over-capacity" this allows for easier identification of over capacity situations and capture what those look like
3. Including a data file for the model for users to run examples
4. As mentioned above breaking out fixed and variable costs
5. Potentially adding customer nodes from dcs to customers


# Dependencies

Pyomo

Python 3.X

Pandas

Numpy

Seaborn and/or matplotlib


# Getting Started
To get started make sure to download the required dependencies using the pip install command on in the command prompt/shell. 
Make sure that you have all data needed to run the model(examples will be added)

Network Opt:
1. Distribution Centers
2. Production Centers
3. Products
4. Production Lines
5. Cost/Unit for each product
6. Cost/Unit for each transportation lane
7. Maximum and Minimum Production Capacities
8. Demands for both directly shipped and hubbed products

For now you must have a way to make that data into a dat file. I will be adding a program that will handle that for you from most formats. You can also alter the code so that it will except other data sources using the pyomo.DataPortal method.

From there the code allow you to define an optimizer object and a dat file to read for the optimization. After a successful execution you should get a response from the optimizer with results


# How to Contribute

Making the model better either via better mathematical formulation or better programming

Any suggestions for frameworks 

Suggestions for desired features or solutions to problems that are similar
