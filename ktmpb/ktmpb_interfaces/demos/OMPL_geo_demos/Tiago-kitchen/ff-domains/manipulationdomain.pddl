(define (domain manipulation)

(:types obstacle robot location)  

(:predicates    
         (at ?rob ?from)          ; The robot is at a location
         (handEmpty)              ; The robot is not holding anything
         (holding ?rob ?obs)      ; The robot is holding an object
         (in ?obs ?from)          ; The object is at a location
         (isclean ?obs)           ; The object is clean
         (isempty ?obs)           ; The object is empty
         (served ?obs)            ; The object has been served
)

(:action move
   :parameters    (?rob - robot ?from - location ?to - location)
   :precondition  (and (at ?rob ?from))           
   :effect        (and   (at ?rob ?to) 
                  (not   (at ?rob ?from))
                  )
)

(:action pick
   :parameters    (?rob - robot ?obs - obstacle ?from - location)
   :precondition  (and  (handEmpty) (in ?obs ?from) 
                        (at ?rob ?from))          
   :effect        (and  (holding ?rob ?obs) 
                  (not  (handEmpty)) )
)

(:action place
   :parameters    (?rob - robot ?obs - obstacle ?from - location)
   :precondition  (and  (holding ?rob ?obs) 
                        (at ?rob ?from)
                        (holding ?rob ?obs))          
   :effect        (and  (handEmpty) (in ?obs ?from) 
                        (not (holding ?rob ?obs)) 
                        (handEmpty))
)

(:action fill
   :parameters    (?rob - robot ?obs - obstacle)
   :precondition  (and (isclean ?obs) (isempty ?obs) (in ?obs coffeemachine) (at ?rob coffeemachine))          
   :effect        (and (not (isempty ?obs)))
)

(:action serve
   :parameters    (?rob - robot ?obs - obstacle ?to - location)
   :precondition  (and  (not (isempty ?obs)) (isclean ?obs) (at ?rob coffeemachine) (in ?obs coffeemachine) (not (served ?obs)))
   :effect        (and  (in ?obs ?to) (at ?rob ?to) (served ?obs) (not (holding ?rob ?obs)))
)
)
