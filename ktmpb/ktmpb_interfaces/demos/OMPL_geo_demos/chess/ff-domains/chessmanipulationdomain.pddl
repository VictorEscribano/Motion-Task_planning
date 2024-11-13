(define (domain chessmanipulation)

(:types obstacle robot location)

(:predicates
       (handEmpty ?rob)
	     (holding ?rob ?obs)
       (in ?obs ?from))

(:action pick
:parameters (?rob - robot ?obs - obstacle ?from - location)
:precondition (and (handEmpty ?rob) (in ?obs ?from))
:effect (and (holding ?rob ?obs)
   (not (handEmpty ?rob)) ))

(:action place
:parameters (?rob - robot ?obs - obstacle ?from - location)
:precondition (and (holding ?rob ?obs))
:effect (and (handEmpty ?rob) (in ?obs ?from)
   (not (holding ?rob ?obs)) ))
)
