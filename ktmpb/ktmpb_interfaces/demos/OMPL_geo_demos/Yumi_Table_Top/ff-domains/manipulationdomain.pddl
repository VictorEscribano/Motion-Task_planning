(define (domain manipulation)

(:types obstacle robot location)

(:predicates
    (handEmpty)
	  (holding ?rob ?obs)
    (in ?obs ?from))

(:action pick
:parameters (?rob - robot ?obs - obstacle ?from - location)
:precondition (and (handEmpty) (in ?obs ?from))
:effect (and (holding ?rob ?obs) (not (handEmpty))
            )
)

(:action place
:parameters (?rob - robot ?obs - obstacle ?to - location)
:precondition (and (holding ?rob ?obs)
                  )
:effect (and (handEmpty) (in ?obs ?to)
   (not (holding ?rob ?obs)) ))

)
