import sys, os
# Make sure you have cloned pddl-parser git repo 
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './pddl-parser'))
sys.path.append(module_path)
from PDDL import PDDL_Parser

import pprint

domain = 'domain.pddl'
problem = 'problem.pddl'

parser = PDDL_Parser()

print('----------------------------')
pprint.pprint(parser.scan_tokens(domain))
print('----------------------------')
pprint.pprint(parser.scan_tokens(problem))
print('----------------------------')
parser.parse_domain(domain)
parser.parse_problem(problem)
print('Domain name: ' + parser.domain_name)
for act in parser.actions:
    print(act)
print('----------------------------')
print('Problem name: ' + parser.problem_name)
print('Objects: ' + str(parser.objects))
print('State: ' + str(parser.state))
print('Positive goals: ' + str(parser.positive_goals))
print('Negative goals: ' + str(parser.negative_goals))
    

