# SAT based planner for automated classical planning
SAT planner for the Optimisation and Planning course.             
This repository implements a SAT approach for solving planning problems , usually described by a domain and a problem written in PDDL STRIPS.

## User guide :
First, you need to load a PDDL parser module , run the following command line:      

```git clone https://github.com/pucrs-automated-planning/pddl-parser.git```

This module comes with useful description of the PDDL problem as well as methods used for implementing the solver.                      
Then, install the CryptoMiniSat solver. The following pip package provides bindings to the solver :

```pip install pycryptosat```

## Execution :
To execute the solver, simply run the main program on an instance of your choice, using the following command line:

```python3 main.py --domain domain.pddl --problem problem.pddl --immutablepreds immutablepreds ```

Where :    

```domain.pddl```  : The file describing the domain                         
```problem.pddl```  : The file describing the problem
```immutablepreds``` : (Optional) List of immutable predicates 

## Modules :
* ```main.py``` : used for execution
* ```clause.py``` : class for manipulating clause objects, implements adding litterals
* ```encoder.py``` : encode and decode a planning problem into a sat problem
* ```check_plan.py``` : check validity of a plan 
