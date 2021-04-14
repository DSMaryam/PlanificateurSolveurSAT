(define (problem solitaire)
 (:domain solitaire)
 (:objects 
     king_red - card
     queen_red - card
     king_black - card
     queen_black - card
     base_col_1 - column
     base_col_2 - column
     base_col_3 - column
     end_col_1 - column
     end_col_2 - column
     jack_black - card
     jack_red - card
     ten_red - card
     
)
 (:init 
  (ondeck jack_black)
  (ondeck jack_red)
  (on king_red queen_black)
  (on king_black queen_red)
  (free king_black)
  (free king_red)
  (free base_col_3)
  (free end_col_1)
  (free end_col_2)
  (on queen_red base_col_1)
  (on queen_black base_col_2)
  
  (can_move_on_top queen_black king_red)
  (can_move_on_top queen_red king_black)
  
  (can_move_on_top jack_black queen_red)
  (can_move_on_top jack_red queen_black)
  
  (can_move_on_top king_red base_col_1)
  (can_move_on_top king_red base_col_2)
  (can_move_on_top king_red base_col_3)
  
  (can_move_on_top king_black base_col_1)
  (can_move_on_top king_black base_col_2)
  (can_move_on_top king_black base_col_3)
  
  (can_place_on_top king_black queen_black)
  (can_place_on_top king_red queen_red)
  (can_place_on_top queen_red jack_red)
  (can_place_on_top queen_black jack_black)
  (can_place_on_top jack_red end_col_1)
  (can_place_on_top jack_black end_col_1)
  (can_place_on_top jack_red end_col_2)
  (can_place_on_top jack_black end_col_2)
  

  (placed end_col_1)
  (placed end_col_2)
  
)
 (:goal
  (and
     (placed king_red)
     (placed king_black)
)))
