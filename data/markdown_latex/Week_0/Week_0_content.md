> “A powerful aspect of abstraction is that many different situations become the same when you forget some details.”
>
> — Eugenia Cheng

## 0 Key mathematical objects, tools, and notation 

The methods that we use to compute things can be very complex: Programs involving lines and lines of code, complicated algorithms, and programming languages that each have their own unique syntax and structures. The complexity often makes it difficult to see patterns in the computations. Our goal (in this course anyway...) is to take away some details involved in certain types of computations so that what’s left can be described completely using sets and functions. 

## 0.1 Sets 

A set is a collection of distinct objects. For example, let A= {I,N,F,O} and B= {1,π,42} in a universe of elements {m,a,t,h,I,N,F,O,1, π ,42, α} (the universal set). 

The set operators ( $\cup$, $\cap$, × ) are some of the “tools” used to manipulate sets: 

A $\cup$ B= { I,N,F,O,1, π ,42 } 

A $\cap$ B= {} 

A= { m,a,t,h,1, π ,42, α} 

B= { m,a,t,h,I,N,F,O, α} 

A × B= { { I, 1 } , { I, π} , { I, 42 } , { N, 1 } , { N, π} , { N, 42 } , { F, 1 } , { F, π} , { F, 42 } , { O, 1 } , { O, π} , { O, 42 } } 

One way of describing A × B is that it consists of all 2-tuples ( a, b ) where a is a member of { I,N,F,O } and b is a member of { 1, π ,42 } . More compactly: 

A×B={(a, b)|a $\in$A, b $\in$B}

## 0.2 Functions

A function f is a mapping from a domain set A to a range set B.

[Figure: diagram illustrating a function mapping elements from A to B is omitted]

Let:
A = {I, N, F, O}
B = {1, π, 42}

We define a function f: A $\to$ B.

[Figure: function assignment diagram is omitted]

Function definition:

f(I) = 1  
f(N) = 42  
f(F) = 42  
f(O) = π  

This function can also be represented as a mapping table:

Mappings:
(I $\to$ 1)  
(N $\to$ 42)  
(F $\to$ 42)  
(O $\to$ π)

## 0.3 Graphs 

Graphs are a collection of vertices and edges. When the vertices represent elements of sets, and the edges represent the relationship between those elements then graphs can be used to visually describe functions. For example the previous function can be represented using the following graph: 

[Figure: graph showing the function mapping a set of letter inputs to number outputs]

This graph can be represented using a set of vertices, V , and directed edges, E , where: 

V = { I,N,F,O,1, π ,42 } 

E={ (I,1), (N,42), (F,42) , (O,π) }

## 0.4 Transition functions 

Let a transition function f be a mapping from some set A × B (the state and input pairs) to the set A (the next states): 

f : A × B $\to$ A

If we let A= { I,N,F,O } and B= { 1, π ,42 } then we can (arbitrarily...) construct a transition function and describe it using a table: 
[Figure: 
This table defines a transition function $\delta$: A × B $\to$ A.

States:
A = {I, N, F, O}

Inputs:
B = {1, 42, π}

Transition rules:

(I, 1) $\to$ N  
(I, 42) $\to$ O  
(I, π) $\to$ N  

(N, 1) $\to$ O  
(N, 42) $\to$ N  
(N, π) $\to$ O  

(F, 1) $\to$ I  
(F, 42) $\to$ I  
(F, π) $\to$ I  

(O, 1) $\to$ F  
(O, 42) $\to$ F  
(O, π) $\to$ N  ]

In the same way that a graph can represent a function, a “state diagram” gives a visual description of a transition function f : 

[Figure: A graph of a state diagram representing the transitions shown in the above table]

Each “edge” in the state diagram is an element of the form (( a, b ) , a ) where a $\in$ A, b $\in$ B . Each vertex a is a state, and for each state there is an input b that “transitions” to a next state. 

For example, starting at the state I, the input 1,1,1 would result in a final state F. Starting at the state I, the input π , π , 42 would result in a final state N. 