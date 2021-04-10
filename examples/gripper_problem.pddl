(define (problem pb1)
    (:domain gripper-strips)
  	(:objects roomA - room roomB - room Ball1 - ball Ball2 - ball left - gripper right - gripper)
	(:init 
		(at-robby roomA) 
		(free left) 
		(free right)  
		(at Ball1 roomA)
		(at Ball2 roomA))
		
	(:goal (and (at Ball1 roomB) 
		(at Ball2 roomB)))
)