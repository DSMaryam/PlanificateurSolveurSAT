(define (problem solitaire_5_1)
 (:domain solitaire)
 (:objects 
     king - card
     queen - card
     jack - card
     ten - card
     nine - card
     eight - card
     seven - card

     base_col_1 - column
     base_col_2 - column
     end_col - column

     
)
 (:init 
; placements initiaux
  (on eight base_col_1)
  (on jack base_col_2)
  (on king jack)
  (hidden jack)
  (ondeck queen)
  (ondeck ten)
  (ondeck seven)
  (ondeck nine)
  (free king)
  (free eight)
  (free end_col)

; regles 
  (can_move_on_top king base_col_1)
  (can_move_on_top king base_col_2)

  (can_move_on_top queen king)
  (can_move_on_top jack queen)
  (can_move_on_top ten jack)
  (can_move_on_top nine ten)
  (can_move_on_top eight nine)
  (can_move_on_top seven eight)

  (can_place_on_top king queen)
  (can_place_on_top queen jack)
  (can_place_on_top jack ten)
  (can_place_on_top ten nine)
  (can_place_on_top nine eight)
  (can_place_on_top eight seven)
  (can_place_on_top seven end_col)
  

  (placed end_col)
)
 (:goal
     (placed king)
))