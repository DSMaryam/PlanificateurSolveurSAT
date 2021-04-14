(define (problem solitaire)
 (:domain solitaire)
 (:objects 
     king - card
     queen - card
     base_col - column
     end_col - column

     
)
 (:init 
  (on king base_col)
  (on queen king)
  (free queen)
  (free end_col)
  (can_place_on_top queen end_col)
  (can_place_on_top king queen)
  (placed end_col)
  
)
 (:goal
     (placed king)

))


