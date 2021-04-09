from enum import Enum
from itertools import *

import sys, os
# Make sure you have cloned pddl-parser git repo 
module_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), './pddl-parser'))
sys.path.append(module_path)
from PDDL import PDDL_Parser

""" 
 'actions',
 'domain_name',
 'objects',
 'predicates',
 'requirements',
 'scan_tokens',
 'split_predicates',
 'types'
 
 parser.positive_goals
 parser.negative_goals
 parser.state
"""



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

    def __init__(self, parser, length=1):
        self._problem = parser
        self.predicates = {key : list(item.values()) for key, item \
                           in self._problem.predicates.items()}
        self._set_hierarchy()
        self._length = length
        self.action_encoding = {act.name : act \
                                for act in self._problem.actions}
        self._propositional_formulas = self._encode()
        
    
    def _set_actions(self):
        action_variables = dict()
        for action in self._problem.actions:
            action_variables[action.name] = dict()
            for params in action.parameters:
                var, t = params
                action_variables[action.name][var] = t
        self.action_variables = actions
        
    def _set_hierarchy(self):
        objs = []
        for _type in self._problem.objects:
            objs += self._problem.objects[_type]
        self._problem.objects['object'] = objs
    
    def _extract_fluents(self):
        fluents = []
        for pred, types in self.predicates.items():
            degree = len(types)
            if degree == 1:
                t = types[0]
                fluents += [(pred, obj) for obj in self._problem.objects[t]]
            else :
                iterables = [self._problem.objects[t] for t in types]
                fluents += [(pred, *objs) for objs in product(*iterables)]
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
        init_state = list(self._problem.state)
        init_state_clauses = []
        for fluent in fluents:
            if fluent not in init_state:
                fluent = ('not',) + fluent
            fluent = fluent + ('0',)
            init_state_clauses.append(Clause(fluent))

        # 2. encode goal state
        goal_state = list(self._problem.positive_goals)
        goal_state_clauses = []
        for goal in goal_state:
            goal_state_clauses.append(Clause(goal + (str(self._length),)))
        
        goal_state = list(self._problem.negative_goals)
        for goal in goal_state:
            goal_state_clauses.append(Clause(('not', goal + (str(self._length),))))

        enc_actions_clauses = []
        explanatory_frame_axioms = []
        complete_exclusion_axiom = []

        for step in range(self._length):
            # 3. encode actions
            for act in actions:
                if act.add_effects.issubset(act.positive_preconditions):
                    continue
                action_tuple = ('not', act.name, str(step))
                # preconditions
                for p in act.positive_preconditions:
                    if 'adjacent' in p: # maybe predicates that are always true (domain dependant)
                        continue
                    action_clause = Clause(action_tuple)
                    p = p + (str(step),)
                    action_clause.add(p, Operator.OR)
                    enc_actions_clauses.append(action_clause)
                # positive effects
                for e in act.add_effects:
                    e = e + (str(step + 1),)
                    action_clause = Clause(action_tuple)
                    action_clause.add(e, Operator.OR)
                    enc_actions_clauses.append(action_clause)
                # negative effects
                for e in act.del_effects:
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
                    b_pos = ('not',) + fluent + (str(step + 1),)
                    clause_pos = Clause(a_pos)
                    clause_pos.add(b_pos, Operator.OR)
                    for act in act_with_pos_effect:
                        c_pos = (act, str(step))
                        clause_pos.add(c_pos, Operator.OR)
                    explanatory_frame_axioms.append(clause_pos)
                if act_with_neg_effect:
                    a_neg = ('not',) + fluent + (str(step),)
                    b_neg = fluent + (str(step + 1),)
                    clause_neg = Clause(a_neg)
                    clause_neg.add(b_neg, Operator.OR)
                    for act in act_with_neg_effect:
                        c_neg = (act, str(step))
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
                action0_tuple = ('not', action_pair[0], str(step))
                action1_tuple = ('not', action_pair[1], str(step))
                action_pair_clause = Clause(action0_tuple)
                action_pair_clause.add(action1_tuple, Operator.OR)
                complete_exclusion_axiom.append(action_pair_clause)

        proposition_formulas = init_state_clauses + goal_state_clauses + \
            enc_actions_clauses + explanatory_frame_axioms + \
            complete_exclusion_axiom

        return proposition_formulas

    @property
    def propositional_formulas(self):
        return self._propositional_formulas
 
if __name__ == "__main__":
    
    parser = PDDL_Parser()
    
    parser.parse_domain('examples/domain.pddl')
    parser.parse_problem('examples/problem.pddl')