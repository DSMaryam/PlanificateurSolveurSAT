import sys, os

# Make sure you have cloned pddl-parser git repo 
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './pddl-parser'))
sys.path.append(module_path)
from PDDL import PDDL_Parser

# TODO : action vs action_id
def check_plan(plan , parser):
    
    current_state  = parser.state
    names = [action.name for action in parser.actions]
    for action_name, *objects in plan:
        action_id = names.index(action_name)
        action = list(parser.actions)[action_id]
        n = len(objects)
                
        #objects_rep = {objects[i] : action.parameters[i][0]\
        #               for i in range(n)}
        
        objects_rep = {action.parameters[i][0] : objects[i] \
                       for i in range(n)}
            
        # assert required predicate degree and correct object types
        assert n == len(action.parameters)
        
        # not working for now because of objects hierarchy 
        
        #assert all(objects[i] in parser.objects[action.parameters[i][1]] for i in range(n))
        
        for cond, *objs  in action.positive_preconditions:
            objs = [objects_rep[obj] for obj in objs]
            if not (cond, *objs) in current_state:
                return False
        
        for cond, *objs  in action.negative_preconditions:
            objs = [objects_rep[obj] for obj in objs]
            if not (cond, *objs) not  in current_state:
                return False
        
        add_effects = []
        for cond, *objs  in action.add_effects:
            objs = [objects_rep[obj] for obj in objs]
            add_effects.append((cond, *objs))
            
        del_effects = []
        for cond, *objs  in action.del_effects:
            objs = [objects_rep[obj] for obj in objs]
            del_effects.append((cond, *objs))
        
        current_state = current_state.union(frozenset(add_effects))
        current_state = current_state.difference(frozenset(del_effects))
        
    if not all(state in current_state for state in parser.positive_goals): 
        return False
    if not all(state not in current_state for state in parser.negative_goals):
        return False
    
    return True
        
if __name__ == "__main__":
    
    parser = PDDL_Parser()
    
    parser.parse_domain('examples/domain.pddl')
    parser.parse_problem('examples/reversed.pddl')
    
    """
    e.g of optimal plans for other problems 
    
    plan = [('place_from_deck', 'jack_black', 'end_col_2'),
            ('place_from_deck', 'jack_red', 'end_col_1'),
            ('from_base_to_base', 'king_red', 'queen_black', 'base_col_3'),
            ('place_from_base', 'queen_black','base_col_2', 'jack_black'),
            ('place_from_base', 'king_black', 'queen_red', 'queen_black'),
            ('place_from_base', 'queen_red', 'base_col_1', 'jack_red'),
            ('place_from_base', 'king_red', 'base_col_3', 'queen_red')]
    
    plan = [('return', 'queen_red', 'end_col_1', 'king_black'),
            ('from_base_to_base', 'jack_black', 'ten_black', 'queen_red'),
            ('place_from_base', 'ten_black', 'base_col_2', 'end_col_2'),
            ('place_from_base', 'jack_black','queen_red', 'ten_black'),
            ('place_from_base', 'queen_red', 'king_black', 'end_col_1'),
            ('place_from_deck', 'king_red', 'queen_red'),
            ('place_from_deck', 'queen_black', 'jack_black'),
            ('place_from_base', 'king_black', 'base_col_1', 'queen_black')]
    """
    plan = [('from_deck_to_base', 'queen_red', 'king_black'),
            ('from_deck_to_base', 'queen_black', 'king_red'),
            ('from_base_to_base', 'king_red', 'jack_red', 'base_col_4'),
            ('from_base_to_base', 'king_black','jack_black', 'base_col_3'),
            ('from_base_to_base', 'jack_black', 'ten_black', 'queen_red'),
            ('from_deck_to_base', 'nine_red', 'ten_black'),
            ('from_base_to_base', 'ten_black', 'eight_black', 'jack_red'),
            ('from_base_to_base', 'eight_black', 'six_black', 'nine_red'),
            ('place_from_base', 'six_black', 'base_col_2', 'end_col_2'),
            ('place_from_deck', 'seven_black', 'six_black'),
            ('place_from_base', 'eight_black', 'nine_red', 'seven_black'),
            ('from_base_to_base', 'jack_red','ten_red', 'queen_black'),
            ('from_deck_to_base', 'nine_black', 'ten_red'),
            ('from_base_to_base', 'ten_red', 'eight_red', 'jack_black'), 
            ('from_base_to_base', 'eight_red','six_red', 'nine_black'),
            ('place_from_base', 'six_red', 'base_col_1', 'end_col_1'),
            ('place_from_deck', 'seven_red', 'six_red'),
            ('place_from_base', 'eight_red', 'nine_black', 'seven_red'),  
            ('place_from_base', 'nine_black', 'ten_red', 'eight_black'),
            ('place_from_base', 'nine_red', 'ten_black', 'eight_red'),
            ('place_from_base', 'ten_black', 'jack_red', 'nine_black'),
            ('place_from_base', 'ten_red','jack_black', 'nine_red'),
            ('place_from_base', 'jack_black', 'queen_red', 'ten_black'),
            ('place_from_base', 'jack_red', 'queen_black', 'ten_red'),
            ('place_from_base', 'queen_black', 'king_red', 'jack_black'),
            ('place_from_base', 'queen_red', 'king_black', 'jack_red'),
            ('place_from_base', 'king_black', 'base_col_3', 'queen_black'),
            ('place_from_base', 'king_red', 'base_col_4', 'queen_red')
            
            ]
    print(check_plan(plan, parser))

