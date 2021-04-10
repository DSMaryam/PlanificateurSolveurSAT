(define (problem simple-problem)
  (:domain simple)

  (:objects
   rob - robot
   loc1 - location loc2 - location l3 - location)

  (:init
   (adjacent loc1 loc2)
   (adjacent loc2 loc1)
   (adjacent loc2 l3)
   (adjacent loc3 l2)
   (atl rob loc1)
   )

  (:goal
    (atl rob l3)
   )
)