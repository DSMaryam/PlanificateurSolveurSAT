(define (problem reversed)
 (:domain solitaire)
 (:objects 
     king_red - card
     queen_red - card
     king_black - card
     queen_black - card
     jack_black - card
     jack_red - card
     ten_red - card
     ten_black - card
     nine_red - card
     nine_black - card
     eight_red - card
     eight_black - card
     seven_red - card
     seven_black - card
     six_red - card
     six_black - card
     base_col_1 - column
     base_col_2 - column
     base_col_3 - column
     base_col_4 - column
     end_col_1 - column
     end_col_2 - column
     
     
)
 (:init 
  (ondeck nine_black)
  (ondeck nine_red)
  (ondeck queen_red)
  (ondeck queen_black)
  (ondeck seven_red)
  (ondeck seven_black)
  
  (hidden queen_red)
  (hidden queen_black)
  (hidden jack_red)
  (hidden jack_black)
  (hidden ten_red)
  (hidden ten_black)
  (hidden eight_red)
  (hidden eight_black)
  (hidden six_red)
  (hidden six_black)
  
  (on king_red jack_red)
  (on king_black jack_black)
  (on jack_red ten_red)
  (on jack_black ten_black)
  (on ten_red eight_red)
  (on ten_black eight_black)
  (on eight_red six_red)
  (on eight_black six_black)
  (on six_red base_col_1)
  (on six_black base_col_2)
  
  (free king_black)
  (free king_red)
  (free base_col_3)
  (free base_col_4)
  (free end_col_1)
  (free end_col_2)
  
  
  (can_move_on_top queen_black king_red)
  (can_move_on_top queen_red king_black)
  (can_move_on_top jack_black queen_red)
  (can_move_on_top jack_red queen_black)
  (can_move_on_top ten_black jack_red)
  (can_move_on_top ten_red jack_black)
  (can_move_on_top nine_black ten_red)
  (can_move_on_top nine_red ten_black)
  (can_move_on_top eight_black nine_red)
  (can_move_on_top eight_red nine_black)
  (can_move_on_top seven_black eight_red)
  (can_move_on_top seven_red eight_black)
  (can_move_on_top six_black seven_red)
  (can_move_on_top six_red seven_black)
  
  (can_move_on_top king_red base_col_1)
  (can_move_on_top king_red base_col_2)
  (can_move_on_top king_red base_col_3)
  (can_move_on_top king_red base_col_4)
  
  (can_move_on_top king_black base_col_1)
  (can_move_on_top king_black base_col_2)
  (can_move_on_top king_black base_col_3)
  (can_move_on_top king_black base_col_4)
  
  (can_place_on_top king_black queen_black)
  (can_place_on_top king_red queen_red)
  (can_place_on_top queen_red jack_red)
  (can_place_on_top queen_black jack_black)
  (can_place_on_top jack_red ten_red)
  (can_place_on_top jack_black ten_black)
  (can_place_on_top ten_red nine_red)
  (can_place_on_top ten_black nine_black)
  (can_place_on_top nine_red eight_red)
  (can_place_on_top nine_black eight_black)
  (can_place_on_top eight_red seven_red)
  (can_place_on_top eight_black seven_black)
  (can_place_on_top seven_red six_red)
  (can_place_on_top seven_black six_black)
  
  (can_place_on_top six_red end_col_1)
  (can_place_on_top six_black end_col_1)
  (can_place_on_top six_red end_col_2)
  (can_place_on_top six_black end_col_2)
  
  (placed end_col_1)
  (placed end_col_2)
  
)
 (:goal
  (and
     (placed king_red)
     (placed king_black)
)))
