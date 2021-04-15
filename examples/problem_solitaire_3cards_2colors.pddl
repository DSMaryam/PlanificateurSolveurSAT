; relaxed problem : to card of the same color can be stacked 
(define (problem solitaire_3_1)
 (:domain solitaire)
 (:objects 
    king_club - card
    king_diamond - card
    queen_club - card
    queen_diamond - card
    jack_club - card
    jack_diamond - card
    
    base_col_1 - column
    base_col_2 - column
    base_col_3 - column
    end_col_1 - column
    end_col_2 - column
)
 (:init 
    ; initial placement
  (on queen_club base_col_1)
  (on jack_diamond base_col_2)
  (on king_club base_col_3)
  (on king_diamond jack_diamond)
  (on queen_diamond king_club)
  (on jack_club queen_diamond)

  (free jack_club)
  (free queen_club)
  (free king_diamond)
  (free end_col_2)
  (free end_col_1)

  ; rules 
  (can_place_on_top jack_club end_col_1)
  (can_place_on_top jack_diamond end_col_2)
  (can_place_on_top queen_club jack_club)
  (can_place_on_top king_club queen_club)
  (can_place_on_top queen_diamond jack_diamond)
  (can_place_on_top king_diamond queen_diamond)

  (can_move_on_top king_diamond base_col_2)
  (can_move_on_top king_club base_col_1)
  (can_move_on_top king_diamond base_col_1)
  (can_move_on_top king_club base_col_2)

  (can_move_on_top queen_diamond king_club)
  (can_move_on_top jack_club queen_diamond)
  (can_move_on_top queen_club king_diamond)
  (can_move_on_top jack_diamond queen_club)

  (can_move_on_top queen_diamond king_diamond)
  (can_move_on_top jack_diamond queen_diamond)
  (can_move_on_top queen_club king_club)
  (can_move_on_top jack_club queen_club)

  (placed end_col_1)  
  (placed end_col_2)
)
 
(:goal
     (placed king_diamond)
     (placed king_club)
))