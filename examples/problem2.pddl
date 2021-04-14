(define (problem solitaire)
 (:domain solitaire)
 (:objects
     king_red - card 
     queen_red - card
     king_black - card 
     base_col_1 - column 
     base_col_2 - column
     end_col_1 - column
     end_col_2 - column
     jack_black - card
     ten_black - card
     queen_black - card 
     
)
 (:init 

  (ondeck queen_black)
  (ondeck king_red)
  (on king_black base_col_1)
  (free king_black)
  (free queen_red)
  (free end_col_2)
  (free jack_black)
  (hidden ten_black)
  (on jack_black ten_black)
  (on ten_black base_col_2)
  (on queen_red end_col_1)
  (placed queen_red)
  
  (can_move_on_top king_black base_col_1)
  (can_move_on_top king_black base_col_2)
  (can_move_on_top king_red base_col_1)
  (can_move_on_top king_red base_col_2)
  (can_move_on_top queen_red king_black)
  (can_move_on_top jack_black queen_red)
  
  (can_place_on_top queen_red end_col_1)
  (can_place_on_top ten_black end_col_1)
  (can_place_on_top queen_red end_col_2)
  (can_place_on_top ten_black end_col_2)
  (can_place_on_top king_black queen_black)
  (can_place_on_top king_red queen_red)
  (can_place_on_top queen_red end_col_1)
  (can_place_on_top queen_red end_col_2)
  (can_place_on_top queen_black jack_black)
  (can_place_on_top jack_black ten_black)
  (can_place_on_top queen_black jack_black)
  (can_place_on_top ten_black end_col_2)
  (can_place_on_top ten_black end_col_1)
  
  
  (placed end_col_1)
  (placed end_col_2)
  
)
 (:goal
  (and
     (placed king_red)
     (placed king_black)
)))
