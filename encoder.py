from enum import Enum
from itertools import *
from pycryptosat import Solver

import sys, os
# Make sure you have cloned pddl-parser git repo 
module_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), './pddl-parser'))
sys.path.append(module_path)
from PDDL import PDDL_Parser

class Operator(Enum):
    AND = 0,
    OR = 1,
    IMPLIES = 2


class Clause(object):

    def __init__(self, fluent=None):
        if fluent:
            self._clause = [fluent]
            self._single = True
        else:
            self._clause = []
            self._single = False

    def __repr__(self):
        return f"Clause object. {self._clause}"

    def __len__(self):
        return len(self._clause)

    def __getitem__(self, item):
        return self._clause[item]

    def __contains__(self, item):
        return True if item in self._clause else False

    def __eq__(self, other):
        if self._single == other.is_single and self._clause == other.clause:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def add(self, fluent, operator: Operator):
        if len(self._clause) == 0:
            self._single = True
        else:
            self._single = False
            self._clause.append(operator)
        self._clause.append(fluent)

        return self

    @property
    def clause(self):
        return self._clause

    @property
    def is_single(self):
        return self._single

    @property
    def empty(self):
        return self._clause == []


class PlanningProblemEncoder(object):

    def __init__(self, parser, immutable_predicates = ['adjacent'], length=1, type_container = True):
        self._problem = parser
        self.predicates = {key : list(item.values()) for key, item \
                           in self._problem.predicates.items()}
        if type_container:
            self._set_hierarchy()
        self._length = length
        self.immutable_predicates = immutable_predicates
        self.variables = set()
        self._propositional_formulas = self._encode()
        
        
    def _set_hierarchy(self):
        objs = []
        for _type in self._problem.objects:
            objs += self._problem.objects[_type]
        self._problem.objects['object'] = objs
    
    def _extract_fluent(self, pred):
        fluent = []
        types = self.predicates[pred]
        degree = len(types)
        if degree == 1:
            t = types[0]
            fluent += [(pred, obj) for obj in self._problem.objects[t]]
        else :
            iterables = [self._problem.objects[t] for t in types]
            fluent += [(pred, *objs) for objs in product(*iterables)]
        return fluent
    
    def _extract_fluents(self):
        fluents = []
        for pred in self.predicates:
            fluents += self._extract_fluent(pred)
        return fluents
    
    def _get_ground_operators(self) :
        ground_operators = []
        for action in self._problem.actions:
            action_g = action.groundify(self._problem.objects, {}) #TODO
            ground_operators += list(action_g)
        return ground_operators
                
                
    def _encode(self):
        actions = self._get_ground_operators()
        fluents = self._extract_fluents()

        # 1. encode initial state
        init_state = self._problem.state
        init_state_clauses = []
        for fluent in fluents:
            self.variables.add(fluent + ('0',))
            if fluent not in init_state:
                fluent = ('not',) + fluent + ('0',)
            else :
                fluent = fluent + ('0',)
            init_state_clauses.append(Clause(fluent))

        # 2. encode goal state
        goal_state = list(self._problem.positive_goals)
        goal_state_clauses = []
        for goal in goal_state:
            self.variables.add(goal + (str(self._length),))
            goal_state_clauses.append(Clause(goal + (str(self._length),)))
        
        goal_state = list(self._problem.negative_goals)
        for goal in goal_state:
            self.variables.add(goal + (str(self._length),))
            goal = ('not',) + goal
            goal_state_clauses.append(Clause( goal + (str(self._length),)))

        enc_actions_clauses = []
        explanatory_frame_axioms = []
        complete_exclusion_axiom = []

        for step in range(self._length):
            # 3. encode actions
            for act in actions:
                if act.add_effects.issubset(act.positive_preconditions):
                    continue
                self.variables.add((act.name, *act.parameters, str(step)))
                action_tuple = ('not', act.name, *act.parameters, str(step))
                # preconditions
                for p in act.positive_preconditions:
                    if any(pred in p for pred in self.immutable_predicates) :# maybe predicates that are always true (domain dependant)
                        continue
                    action_clause = Clause(action_tuple)
                    p = p + (str(step),)
                    self.variables.add(p)
                    action_clause.add(p, Operator.OR)
                    enc_actions_clauses.append(action_clause)
                # positive effects
                for e in act.add_effects:
                    e = e + (str(step + 1),)
                    self.variables.add(e)
                    action_clause = Clause(action_tuple)
                    action_clause.add(e, Operator.OR)
                    enc_actions_clauses.append(action_clause)
                # negative effects
                for e in act.del_effects:
                    self.variables.add(e + (str(step + 1),))
                    e = ('not',) + e + (str(step + 1),)
                    action_clause = Clause(action_tuple)
                    action_clause.add(e, Operator.OR)
                    enc_actions_clauses.append(action_clause)

            # 4. explanatory frame axioms
            for fluent in fluents:
                act_with_pos_effect = []
                act_with_neg_effect = []
                for act in actions:
                    if act.add_effects.issubset(act.positive_preconditions):
                        continue
                    if fluent in act.add_effects:
                        act_with_pos_effect.append(act)
                    elif fluent in act.del_effects:
                        act_with_neg_effect.append(act)
                if act_with_pos_effect:
                    a_pos = fluent + (str(step),)
                    self.variables.add(a_pos)
                    self.variables.add(fluent + (str(step + 1),))
                    b_pos = ('not',) + fluent + (str(step + 1),)
                    clause_pos = Clause(a_pos)
                    clause_pos.add(b_pos, Operator.OR)
                    for act in act_with_pos_effect:
                        c_pos = (act.name, *act.parameters,  str(step))
                        clause_pos.add(c_pos, Operator.OR)
                    explanatory_frame_axioms.append(clause_pos)
                if act_with_neg_effect:
                    a_neg = ('not',) + fluent + (str(step),)
                    b_neg = fluent + (str(step + 1),)
                    self.variables.add(b_neg)
                    self.variables.add(fluent + (str(step),))
                    clause_neg = Clause(a_neg)
                    clause_neg.add(b_neg, Operator.OR)
                    for act in act_with_neg_effect:
                        c_neg = (act.name, *act.parameters, str(step))
                        clause_neg.add(c_neg, Operator.OR)
                    explanatory_frame_axioms.append(clause_neg)

            # 5. complete exclusion axiom
            for action_pair in combinations(actions, 2):
                if action_pair[0].add_effects.issubset(
                        action_pair[0].positive_preconditions):
                    continue
                if action_pair[1].add_effects.issubset(
                        action_pair[1].positive_preconditions):
                    continue
                self.variables.add((action_pair[0].name, *action_pair[0].parameters, str(step)))
                self.variables.add((action_pair[1].name, *action_pair[1].parameters, str(step)))
                action0_tuple = ('not', action_pair[0].name, *action_pair[0].parameters, str(step))
                action1_tuple = ('not', action_pair[1].name, *action_pair[1].parameters, str(step))
                action_pair_clause = Clause(action0_tuple)
                action_pair_clause.add(action1_tuple, Operator.OR)
                complete_exclusion_axiom.append(action_pair_clause)

        proposition_formulas = init_state_clauses + goal_state_clauses + \
            enc_actions_clauses + explanatory_frame_axioms + \
            complete_exclusion_axiom

        return proposition_formulas

    def _sat_indexing(self):
        i = 1
        indexing = dict()
        for var in self.variables:
            indexing[var] = i
            i+=1
        return indexing
    
    def formulas_to_sat(self):
        """
        Returns
        -------     
        indexing : Dict
            Keys : Set of variables in boolean SAT problem.
            Values : How every variable is encoded as int type.
        clauses : List
            Clauses to satisfy (respect the CryptoMiniSat format.

        """
        indexing = self._sat_indexing()
        clauses = []
        for clause in self.propositional_formulas:
            v = clause.clause[0::2]
            cl = []
            for literal in v:
                sign = 1
                if literal[0] == 'not' :
                    sign = -1
                    _, *literal = literal
                cl.append(sign * indexing[tuple(literal)])
            clauses.append(cl)
        return indexing, clauses
                    
    
    def build_plan(self, valuation, indexing):
        variables = list(indexing.keys())
        action_names = [act.name for act in self._problem.actions]
        positive_act = list(filter(lambda v: valuation[indexing[v]]\
                                   and v[0] in action_names, variables))
        positive_act = sorted(positive_act, key = lambda x : int(x[-1]))
    
        return positive_act

    @property
    def propositional_formulas(self):
        return self._propositional_formulas
 
if __name__ == "__main__":
    
    parser = PDDL_Parser()
    
    parser.parse_domain('examples/domain_recipies.pddl')
    parser.parse_problem('examples/pb_tartiflette.pddl')

    # change length according to plan estimation
    i=0
    sat = False
    while not sat:
      # change length according to plan estimation
      print('no plan found of length = ',i)
      i+=1
      pb = PlanningProblemEncoder(parser, length = i) 
    
      indexing, clauses = pb.formulas_to_sat()
    
      sat_solver = Solver()
      sat_solver.add_clauses(clauses)
      sat, valuation = sat_solver.solve()
    
    plan = pb.build_plan(valuation, indexing)
    print("Plan found !")
    for act, *objs in plan:
        print(f'{act} --> {objs}')
    
