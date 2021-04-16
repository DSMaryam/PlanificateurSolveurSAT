(define (problem solitaire_7_2_unconstrained)
 (:domain solitaire)
 (:objects 
    king_club - card
    king_diamond - card
    queen_club - card
    queen_diamond - card
    jack_club - card
    jack_diamond - card
    ten_club - card
    ten_diamond - card
    nine_club - card
    nine_diamond - card
    eight_club - card
    eight_diamond - card 
    seven_club - card
    seven_diamond - card 
    
    base_col_1 - column
    base_col_2 - column
    base_col_3 - column
    end_col_1 - column
    end_col_2 - column
)
(:init 
    ; initial placement
  (on nine_diamond base_col_1)

  (on king_diamond base_col_2)
  (on seven_club king_diamond)

  (on jack_diamond base_col_3)
  (on ten_diamond jack_diamond)
  (on queen_club ten_diamond)
  
  (hidden king_diamond)
  (hidden jack_diamond)
  (hidden ten_diamond)

  (free nine_diamond)
  (free seven_club)
  (free queen_club)

  (ondeck seven_diamond)
  (ondeck eight_club)
  (ondeck eight_diamond)
  (ondeck nine_club)
  (ondeck ten_club)
  (ondeck jack_club)
  (ondeck queen_diamond)
  (ondeck king_club)
  
  (free end_col_1)
  (free end_col_2)

  ; rules 
  (can_place_on_top seven_diamond end_col_2)
  (can_place_on_top seven_club end_col_1)
  (can_place_on_top eight_club seven_club)
  (can_place_on_top eight_diamond seven_diamond)
  (can_place_on_top nine_club eight_club)
  (can_place_on_top nine_diamond eight_diamond)
  (can_place_on_top ten_club nine_club)
  (can_place_on_top ten_diamond nine_diamond)
  (can_place_on_top jack_club ten_club)
  (can_place_on_top jack_diamond ten_diamond)
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
  (can_move_on_top ten_diamond jack_club)
  (can_move_on_top nine_club ten_diamond)
  (can_move_on_top eight_diamond nine_club)
  (can_move_on_top seven_club eight_diamond)

  (can_move_on_top queen_club king_diamond)
  (can_move_on_top jack_diamond queen_club)
  (can_move_on_top ten_club jack_diamond)
  (can_move_on_top nine_diamond ten_club)
  (can_move_on_top eight_club nine_diamond)
  (can_move_on_top seven_diamond eight_club)
  
  (can_move_on_top queen_club king_club)
  (can_move_on_top jack_club queen_club)
  (can_move_on_top ten_club jack_club)
  (can_move_on_top nine_club ten_club)
  (can_move_on_top eight_club nine_club)
  (can_move_on_top seven_club eight_club)
  
  (can_move_on_top queen_diamond king_diamond)
  (can_move_on_top jack_diamond queen_diamond)
  (can_move_on_top ten_diamond jack_diamond)
  (can_move_on_top nine_diamond ten_diamond)
  (can_move_on_top eight_diamond nine_diamond)
  (can_move_on_top seven_diamond eight_diamond)

  (placed end_col_1)  
  (placed end_col_2)
)
 
  (:goal
    (and (placed king_diamond) (placed king_club))
)
)