(define (problem solitaire)
 (:domain solitaire)
 (:objects 
     king - card
     queen - card
     jack - card
     ten - card
     base_col_1 - column
     base_col_2 - column
     end_col - column

     
)
 (:init 
  (on ten base_col_1)
  (ondeck jack)
  (on king ten)
  (on queen king)
  (free queen)
  (free base_col_2)
  (free end_col)
  (can_place_on_top jack ten)
  (can_place_on_top queen jack)
  (can_place_on_top king queen)
  (can_place_on_top ten end_col)
  (can_move_on_top king base_col_2)
  (placed end_col)
  
)
 (:goal
     (placed king)

))


