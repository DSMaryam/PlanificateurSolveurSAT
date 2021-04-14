import time 
from pycryptosat import Solver
from encoder import PlanningProblemEncoder

import sys, os
# Make sure you have cloned pddl-parser git repo 
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './pddl-parser'))
sys.path.append(module_path)
from PDDL import PDDL_Parser


if __name__ == "__main__":
    
    domain = sys.argv[1]
    problem = sys.argv[2]
    
    parser = PDDL_Parser()

    t= time.time()
    parser.parse_domain(domain)
    parser.parse_problem(problem)


    # change length according to plan estimation
    i=0
    sat = False
    while not sat:
      # change length according to plan estimation
      print('no plan found of length = ',i)
      i+=1
      
      ## CHANGE THE IMMUTABLE PREDICATES IF YOU CHANGE THE PROBLEM ##
      # or simply just delete the parameter if you don't know the problem
      
      pb = PlanningProblemEncoder(parser, length = i, immutable_predicates = \
                                  ['can_move_on_top', 'can_place_on_top'] )
    
      indexing, clauses = pb.formulas_to_sat()
    
      sat_solver = Solver()
      sat_solver.add_clauses(clauses)
      sat, valuation = sat_solver.solve()
    
    plan = pb.build_plan(valuation, indexing)
    print('time needed for execution :', time.time()-t)
    print("Plan found !")
    for act, *objs in plan:
        print(f'{act} --> {objs}')
    
