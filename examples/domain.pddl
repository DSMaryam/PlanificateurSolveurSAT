(define (domain solitaire)
  (:requirements :strips :typing)
  (:types card column - object)

  (:predicates  
    (on ?c - card ?o - object)
    (ondeck ?c - card)
    (can_move_on_top ?c - card ?o - object)
    (can_place_on_top ?c - card ?o - object)
    (free ?o - object)
    (placed ?o - object)
    (hidden ?o - object)
    )

		
  (:action from_deck_to_base
             :parameters (?c - card ?o - object )
             :precondition (and (not (placed ?c) ) (ondeck ?c) (free ?o) (can_move_on_top ?c ?o) (not (placed ?o)))
             :effect (and (not (free ?o))
	     	     	  (free ?c)
			          (not (ondeck ?c) )
                      (on ?c ?o))
  )

  (:action from_base_to_base
             :parameters (?c - card ?o1 - object ?o2 - object )
             :precondition (and (not (placed ?c)) (not (placed ?o2)) (can_move_on_top ?c ?o2) (on ?c ?o1) (free ?o2)  (not (hidden ?c)))
             :effect (and (free ?o1)
	     	     	 (not (free ?o2))
                     (on ?c ?o2)
                     (not (on ?c ?o1))
                     (not (hidden ?o1)) )
  )

  (:action place_from_deck
             :parameters (?c - card ?o - object)
             :precondition (and (not (placed ?c) ) (ondeck ?c) (free ?o) (can_place_on_top ?c ?o) (placed ?o))
             :effect (and (free ?c)
	     	     	  (not (free ?o))
	     	     	  (not (ondeck ?c))
                (on ?c ?o)
                (placed ?c))
)
  (:action place_from_base
             :parameters (?c - card ?o1 - object ?o2 - object )
             :precondition (and (not (placed ?c) ) (on ?c ?o1) (free ?c) (free ?o2) (can_place_on_top ?c ?o2) (placed ?o2))
             :effect (and (free ?o1)
             
	     	    (not (free ?o2))
                (on ?c ?o2)
                (not (on ?c ?o1))
                (placed ?c)
                (not (hidden ?o1)))
)

(:action return
             :parameters (?c - card ?o1 - object ?o2 - object )
             :precondition (and (placed ?c) (on ?c ?o1) (free ?c) (free ?o2) (can_move_on_top ?c ?o2))
             :effect (and (free ?o1)
	     	     	  (not (free ?o2))
                (on ?c ?o2)
                (not (placed ?c))
                (not (on ?c ?o1)))
)


)