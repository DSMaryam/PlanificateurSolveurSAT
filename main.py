import time 
from pycryptosat import Solver
from encoder import PlanningProblemEncoder

import sys, os
# Make sure you have cloned pddl-parser git repo 
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './pddl-parser'))
sys.path.append(module_path)
from PDDL import PDDL_Parser
import argparse


if __name__ == "__main__":   

    parser = argparse.ArgumentParser('argument for training')
    parser.add_argument('--domain', type=str, help='domain.pddl')
    parser.add_argument('--problem', type=str, help='problem.pddl')
    parser.add_argument('--immutablepreds', type=list, default=[['can_move_on_top'], ['can_place_on_top']], help='immutable predicates',nargs='+')
    opt = parser.parse_args()

    domain = opt.domain
    problem = opt.problem

    immutable_predicates=[]
    for i in opt.immutablepreds:
        immutable_predicates.append(i[0])
    
    parser = PDDL_Parser()

    t= time.time()
    parser.parse_domain(domain)
    parser.parse_problem(problem)



    step=0
    sat = False
    ## CHANGE THE IMMUTABLE PREDICATES IF YOU CHANGE THE PROBLEM ##
    # or simply just delete the parameter if you don't know the problem
      
    pb = PlanningProblemEncoder(parser, immutable_predicates = immutable_predicates)
    
    while not sat:
      # add length until satisfaction
      print('no plan found of length = ',step)
      pb.add_step(step)
      step+=1
      indexing, clauses = pb.formulas_to_sat()
      sat_solver = Solver()
      sat_solver.add_clauses(clauses)
      sat, valuation = sat_solver.solve()
    
    plan = pb.build_plan(valuation, indexing)
    print('time needed for execution :', time.time()-t)
    print(f"Plan found of length {step}!")
    for act, *objs in plan:
        print(f'{act} --> {objs}')
    
