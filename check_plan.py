import sys, os
# Make sure you have cloned pddl-parser git repo 
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './pddl-parser'))
sys.path.append(module_path)
from PDDL import PDDL_Parser

# TODO : action vs action_id
def check_plan(plan , parser):
    
    current_state  = parser.state
    
    for action_id, *objects in plan:
        action = parser.actions[action_id]
        print(action)
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
            assert (cond, *objs) in current_state
        
        for cond, *objs  in action.negative_preconditions:
            objs = [objects_rep[obj] for obj in objs]
            assert (cond, *objs) not  in current_state
        
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
        
    assert all(state in current_state for state in parser.positive_goals)
    assert all(state not in current_state for state in parser.negative_goals)
    
    return True
        
if __name__ == "__main__":
    
    parser = PDDL_Parser()
    
    parser.parse_domain('examples/domain.pddl')
    parser.parse_problem('examples/reversed.pddl')
    
    """
    e.g of optimal plans for other problems 
    
    plan = [(2, 'jack_black', 'end_col_2'),
            (2, 'jack_red', 'end_col_1'),
            (1, 'king_red', 'queen_black', 'base_col_3'),
            (3, 'queen_black','base_col_2', 'jack_black'),
            (3, 'king_black', 'queen_red', 'queen_black'),
            (3, 'queen_red', 'base_col_1', 'jack_red'),
            (3, 'king_red', 'base_col_3', 'queen_red')]
    
    plan = [(4, 'queen_red', 'end_col_1', 'king_black'),
            (1, 'jack_black', 'ten_black', 'queen_red'),
            (3, 'ten_black', 'base_col_2', 'end_col_2'),
            (3, 'jack_black','queen_red', 'ten_black'),
            (3, 'queen_red', 'king_black', 'end_col_1'),
            (2, 'king_red', 'queen_red'),
            (2, 'queen_black', 'jack_black'),
            (3, 'king_black', 'base_col_1', 'queen_black')]
    """
    plan = [(0, 'queen_red', 'king_black'),
            (0, 'queen_black', 'king_red'),
            (1, 'king_red', 'jack_red', 'base_col_4'),
            (1, 'king_black','jack_black', 'base_col_3'),
            (1, 'jack_black', 'ten_black', 'queen_red'),
            (0, 'nine_red', 'ten_black'),
            (1, 'ten_black', 'eight_black', 'jack_red'),
            (1, 'eight_black', 'six_black', 'nine_red'),
            (3, 'six_black', 'base_col_2', 'end_col_2'),
            (2, 'seven_black', 'six_black'),
            (3, 'eight_black', 'nine_red', 'seven_black'),
            (1, 'jack_red','ten_red', 'queen_black'),
            (0, 'nine_black', 'ten_red'),
            (1, 'ten_red', 'eight_red', 'jack_black'), 
            (1, 'eight_red','six_red', 'nine_black'),
            (3, 'six_red', 'base_col_1', 'end_col_1'),
            (2, 'seven_red', 'six_red'),
            (3, 'eight_red', 'nine_black', 'seven_red'),  
            (3, 'nine_black', 'ten_red', 'eight_black'),
            (3, 'nine_red', 'ten_black', 'eight_red'),
            (3, 'ten_black', 'jack_red', 'nine_black'),
            (3, 'ten_red','jack_black', 'nine_red'),
            (3, 'jack_black', 'queen_red', 'ten_black'),
            (3, 'jack_red', 'queen_black', 'ten_red'),
            (3, 'queen_black', 'king_red', 'jack_black'),
            (3, 'queen_red', 'king_black', 'jack_red'),
            (3, 'king_black', 'base_col_3', 'queen_black'),
            (3, 'king_red', 'base_col_4', 'queen_red')
            
            ]
    print(check_plan(plan, parser))

