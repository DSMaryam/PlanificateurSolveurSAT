(define (problem solitaire_4_1)
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
   ; tirage inital 
  (on jack base_col_1)
  (on king base_col_2)
  (ondeck king)
  (on queen jack)
  (free queen)
  (free ten)
  (free end_col)

  ; regles de placement
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


