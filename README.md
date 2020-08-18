# Supply-Chain-Optimization
A repository of Supply Chain Optimization Programs


# Network Optimization Current Model Details:

This program solves the assignment problem for a supply chain network with Production Centers, Hubs and Distribution Centers. The objective function minimizes total network cost.  A couple of things to note here is that the production cost is a flat cost/unit. I am working on building a more robust version that breaks that out to fixed production cost and variable production costs. I also have not modeled customer deliveries from the dc which is another important problem when looking to minimize cost in a supply chain. I would use the minimum production capacity if you want to ensure each production line has a minimum amount of work hours. 

Future updates:
Model production capacity in hours not units
Add a slack variable for production capacity to allow you to run "over-capacity" this allows for easier identification of over capacity situations and capture what those look like
Including a data file for the model for users to run examples
As mentioned above breaking out fixed and variable costs
potentially adding customer nodes from dcs to customers
