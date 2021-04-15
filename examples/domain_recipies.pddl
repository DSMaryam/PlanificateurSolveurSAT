(define (domain recipies)
  (:requirements :strips :typing :negative-preconditions)
  (:types ingredient cooker)
  (:predicates 
    (cooked ?i - ingredient) (is_cut ?i - ingredient)
    (is_clean ?c - cooker)
    (free ?x)
    (in ?i - ingredient ?c - cooker)
  )

  (:action put
    :parameters (?ing - ingredient ?coo - cooker)
    :precondition (and (is_clean ?coo) (free ?coo) (free ?ing))
    :effect (and (in ?ing ?coo) (not(free ?coo)) (not(free ?ing)))
  )

  (:action remove
    :parameters (?ing - ingredient ?coo - cooker)
    :precondition (and (in ?ing ?coo))
    :effect (and (not(in ?ing ?coo)) (free ?coo) (free ?ing))
  )

  (:action cook
    :parameters (?ing - ingredient ?coo - cooker)
    :precondition (and (in ?ing ?coo) (is_cut ?ing))
    :effect (and (cooked ?ing) (not(is_clean ?coo)))
  )

  (:action cut
    :parameters (?ing - ingredient)
    :precondition (and (free ?ing) (not(is_cut ?ing)))
    :effect (and (is_cut ?ing))
  )
  
  (:action clean
    :parameters (?coo - cooker)
    :precondition (and (free ?coo) (not(is_clean ?coo)))
    :effect (and (is_clean ?coo))
  )
)