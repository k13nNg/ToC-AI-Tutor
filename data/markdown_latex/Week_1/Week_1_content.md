>“Theory of Computation shows you a new, simpler, more elegant side of computers... it can heighten your aesthetic sense and help you build more beautiful systems.” 
>
>Michael Sipser (Theory of Computation Guru) 

# 1 Finite Automata 

Deterministic Finite Automata (DFA) are models for computers with limited memory. They are formally described by a 5-tuple ( Q, $\Sigma$ , $\delta$, q 0 , F ) where: 

1. Q is a finite set of states 

2. $\Sigma$ is the alphabet (a finite set of symbols) 

3. $\delta$ : Q × $\Sigma$ $\to$ Q is the transition function 

4. $q_{0}$ $\in$ Q is the start state 

5. F $\subseteq$ Q is the set of accept states 

They can also be described informally by using a state diagram. 

## 1.1 finite automaton for checking a string for equality 

Suppose we have a machine that checks if a binary string represents 5. A finite automaton, M 1, that models this machine can be represented using the following state diagram: 

[Figure: A state diagram of a finite automata (Q, $\Sigma$, $\delta$, $q_{0}$, F) described as follows:
- Q = {$q_{1}$, $q_{2}$, $q_{3}$, $q_{4}$, $q_{5}$}
- $\Sigma$ = {0, 1}
- $q_{0}$ = $q_{1}$
- F = {$q_{4}$}

with transition function $\delta$ described as follows:
* δ($q_{1}$, 0) = $q_{5}$
* δ($q_{1}$, 1) = $q_{2}$
* δ($q_{2}$, 0) = $q_{3}$
* δ($q_{2}$, 1) = $q_{5}$
* δ($q_{3}$, 0) = $q_{5}$
* δ($q_{3}$, 1) = $q_{4}$
* δ($q_{4}$, 0) = $q_{5}$
* δ($q_{4}$, 1) = $q_{5}$
* δ($q_{5}$, 0) = $q_{5}$
* δ($q_{5}$, 1) = $q_{5}$
]

## 1.2 finite automaton for finding a word in a file 

Suppose we have a machine that searches a file for the existence of a binary string that represents 5. A finite automaton, M 2, that models this machine can be represented using the following state diagram: 

[Figure: A state diagram of a finite automata (Q, $\Sigma$, $\delta$, $q_{0}$, F) described as follows:

* Q = {$q_{1}$, $q_{2}$, $q_{3}$, $q_{4}$}
* $\Sigma$ = {0, 1}
* $q_{0}$ = $q_{1}$
* F = {$q_{4}$}

with transition function $\delta$ described as follows:

* δ($q_{1}$, 0) = $q_{1}$
* δ($q_{1}$, 1) = $q_{2}$
* δ($q_{2}$, 0) = $q_{3}$
* δ($q_{2}$, 1) = $q_{2}$
* δ($q_{3}$, 0) = $q_{1}$
* δ($q_{3}$, 1) = $q_{4}$
* δ($q_{4}$, 0) = $q_{4}$
* δ($q_{4}$, 1) = $q_{4}$]

The formal description of M2 is the 5-tuple ({$q_{1}$, $q_{2}$, $q_{3}$, $q_{4}$ }, {0, 1 }, $\delta$, $q_{1}$ , {$q_{4}$}),where $\delta$ is given by: 

* δ($q_{1}$, 0) = $q_{1}$
* δ($q_{1}$, 1) = $q_{2}$
* δ($q_{2}$, 0) = $q_{3}$
* δ($q_{2}$, 1) = $q_{2}$
* δ($q_{3}$, 0) = $q_{1}$
* δ($q_{3}$, 1) = $q_{4}$
* δ($q_{4}$, 0) = $q_{4}$
* δ($q_{4}$, 1) = $q_{4}$]



## 1.3 the language of a finite automaton 

If A is the set of all strings that machine M accepts, then A is the language of M , and hence $L(M)$ = A . 

In the case of M 2, we have that $L(M_2)$ = {w | w contains the substring 101 } 

In the case of M1, we have that $L(M_1)$ = { 101 }. In other words, the language of M1 is the binary string 101. 

## 1.4 the empty string, $\varepsilon$ 

The $\varepsilon$ symbol is used to represent the empty string; an input consisting of zero elements from the alphabet. 

For example, in a real language (like python) we would use: 

`x=""` 

to define a string, x, of length zero. 

## 1.5 definition of computation 

Let M = ( Q, $\Sigma$ , $\delta$, $q_0$ , F ) be a finite automaton and $w = w_1w_2w_3 ...w_n$ be a string of length $n$ over the alphabet $\Sigma$. Then M accepts w if a sequence of states $r_0 , r_1 , r_2 , \ldots, r_n$ exists in Q such that: 

1. r0 = $q_{0}$ 

2. $\delta$ (ri, w{i+1}) = r{i +1} for i = 0 , 1 , ..., n − 1 

3. rn $\in$ F 

We have that M recognizes a language A if A = {w|M accepts w} . 

## 1.6 regular languages 

A language is a regular language if some finite automaton recognizes it. 

In the case of M 2 given by: 

[Figure: A state diagram of a finite automata (Q, $\Sigma$, $\delta$, $q_{0}$, F) described as follows:

* Q = {$q_{1}$, $q_{2}$, $q_{3}$, $q_{4}$}
* $\Sigma$ = {0, 1}
* $q_{0}$ = $q_{1}$
* F = {$q_{4}$}

with transition function $\delta$ described as follows:

* δ($q_{1}$, 0) = $q_{1}$
* δ($q_{1}$, 1) = $q_{2}$
* δ($q_{2}$, 0) = $q_{3}$
* δ($q_{2}$, 1) = $q_{2}$
* δ($q_{3}$, 0) = $q_{1}$
* δ($q_{3}$, 1) = $q_{4}$
* δ($q_{4}$, 0) = $q_{4}$
* δ($q_{4}$, 1) = $q_{4}$]

We have that $L(M_2)$ = { w | w contains the substring 101 } . Therefore $L(M_2)$ is a regular language. 

## 1.7 regular operations 

Let A and B be languages. The regular operations are: 

- Union: A $\cup$ B = {x|x $\in$ A or x $\in$ B} 

- Concatenation: A $\circ$ B = {xy|x $\in$ A and y $\in$ B} 

- Star: $A^*$ = {x_1x_2x_3...x_k | $k \geq 0$ and each xi $\in$ A} 

For example if A = { 3p0, r2 } and B = { bb8 } then: 

A $\cup$ B = { 3p0, r2, bb8 } 

A $\circ$ B = { 3p0bb8, r2bb8 } 

$A^*$ = {$\varepsilon$ , 3po, r2, 3por2, r23p0, 3p03p03p0, ... } , where $\varepsilon$ is the empty string. 