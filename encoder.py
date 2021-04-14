from itertools import *
from clause import Operator, Clause
from copy import deepcopy


class PlanningProblemEncoder(object):

    def __init__(self, parser, length=1, type_container = True, immutable_predicates = []):
        """
        

        Parameters
        ----------
        parser : parser instance that retrieved information from a PDDL problem
                and its domain
        length : length at which a plan is desired
             The default is 1.
        type_container : infer world objects global hierarchy
            The default is True.
        immutable_predicates : optional
           Set of predicates that can't be changed during plan execution
            The default is [].

        """
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
        """
        Add 'object' type as a global type , since the parser can't infer the global type
        of objects

        """
        objs = []
        for _type in self._problem.objects:
            objs += self._problem.objects[_type]
        self._problem.objects['object'] = list(set(objs))
    
    def _extract_fluent(self, pred):
        """
    
        Parameters
        ----------
        pred : predicate name

        Extract all combinations of possible predicates with the given predicate name 
        for all world objects

        """
        fluent = []
        types = self.predicates[pred]
        degree = len(types)
        if degree == 1:
            t = types[0]
            fluent += [(pred, obj) for obj in self._problem.objects[t]]
        else :
            iterables = [self._problem.objects[t] for t in types]
            fluent += [(pred, *objs) for objs in product(*iterables) if len(objs) == len(set(objs)) ]
        return fluent
    
    def _extract_fluents(self):
        fluents = []
        for pred in self.predicates:
            fluents += self._extract_fluent(pred)
        return fluents
    
    def _get_ground_operators(self) :
        """
        Extracts ground actions : all possible combinations of actions for all objects 
        in the world

        """
        ground_operators = []
        for action in self._problem.actions:
            action_g = action.groundify(self._problem.objects, \
                                        {}) #TODO
            ground_operators += list(action_g)
        return ground_operators
                
    def _encode(self):
        """
        Generates the set of clauses for the SAT problem

        """
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
                
                # pos preconditions
                for p in act.positive_preconditions:
                    action_clause = Clause(action_tuple)
                    p = p + (str(step),)
                    self.variables.add(p)
                    action_clause.add(p, Operator.OR)
                    enc_actions_clauses.append(action_clause)
                    
                # neg preconditions
                for p in act.negative_preconditions:
                    action_clause = Clause(action_tuple)
                    p = ('not', ) + p + (str(step),)
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
                
                if fluent[0] in self.immutable_predicates and fluent in init_state:
                    self.variables.add(fluent + (str(step),))
                    clause = Clause(fluent + (str(step),))
                    explanatory_frame_axioms.append(clause)
                    continue
                elif fluent[0] in self.immutable_predicates and fluent not in init_state:
                    self.variables.add(fluent + (str(step),))
                    clause = Clause(('not', ) + fluent + (str(step),))
                    explanatory_frame_axioms.append(clause)
                    continue
                
                pos_clause = Clause(fluent + (str(step), ))
                self.variables.add(fluent + (str(step), ))
                pos_clause.add(('not', ) + fluent + (str(step +1), ), Operator.OR)
                self.variables.add( fluent + (str(step +1), ))
                neg_clause = Clause(('not', ) + fluent + (str(step), ))
                neg_clause.add(fluent + (str(step +1), ), Operator.OR)
                
                act_with_pos_effect = []
                act_with_neg_effect = []
                for act in actions:
                    if fluent in act.add_effects:
                        act_with_pos_effect.append(act)
                    elif fluent in act.del_effects:
                        act_with_neg_effect.append(act)
                        
                        
                if act_with_pos_effect:
                    
                    pos_clause_ = deepcopy(pos_clause)
                    for act in act_with_pos_effect:
                        act_pos = (act.name, *act.parameters,  str(step))
                        pos_clause_.add(act_pos, Operator.OR)
                    explanatory_frame_axioms.append(pos_clause_)
                    
                else :
                    explanatory_frame_axioms.append(pos_clause)
                    
                if act_with_neg_effect:
                    
                    neg_clause_ = deepcopy(neg_clause)
                    for act in act_with_neg_effect:
                        act_neg = (act.name, *act.parameters, str(step))
                        neg_clause_.add(act_neg, Operator.OR)
                    explanatory_frame_axioms.append(neg_clause_)
                
                else:
                    explanatory_frame_axioms.append(neg_clause)

            # 5. complete exclusion axiom
            for action_pair in combinations(actions, 2):

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
            Values : Int type index for every variable.
        clauses : List
            Clauses to satisfy (with respect the CryptoMiniSat format).

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
 



