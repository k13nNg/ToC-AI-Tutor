>“The 9000 series is the most reliable computer ever made. No 9000 computer has ever made a mistake or distorted information. We are all, by any practical definition of the words, foolproof and incapable of error.” 
>
>HAL 9000 (Iconic Sci-Fi AI) 

# 2 Nondeterminism 

A finite automaton that has exactly one possible transition arrow for every symbol in the alphabet for each of its states is deterministic and called a deterministic finite automaton (DFA). 

A finite automaton that does not have exactly one possible transition arrow for every symbol is nondeterministic and called a nondeterministic finite automaton (NFA). 

## 2.1 NFA: computing in parallel 

Let A be the language of all strings with $\Sigma$ = {0, 1} that contain a 1 in the third position from the end. A DFA that recognizes A is tricky to build... but a NFA is fairly straightforward: 

[Figure: A state diagram of a finite automata (Q, $\Sigma$, $\delta$, $q_{0}$, F) described as follows:

* Q = {$q_{1}$, $q_{2}$, $q_{3}$, $q_{4}$}
* $\Sigma$ = {0, 1}
* $q_{0}$ = $q_{1}$
* F = {$q_{4}$}

with transition function $\delta$ described as follows:

* δ($q_{1}$, 0) = {$q_{1}$}
* δ($q_{1}$, 1) = {$q_{1}$, $q_{2}$}
* δ($q_{2}$, 0) = {$q_{3}$}
* δ($q_{2}$, 1) = {$q_{3}$}
* δ($q_{3}$, 0) = {$q_{4}$}
* δ($q_{3}$, 1) = {$q_{4}$}
* δ($q_{4}$, 0) = $\emptyset$
* δ($q_{4}$, 1) = $\emptyset$]

Adding the empty string $\varepsilon$ to the last two arrows results in a different NFA that recognizes a different language: 

[Figure: A state diagram of a finite automata (Q, $\Sigma$, $\delta$, $q_{0}$, F) described as follows:

* Q = {$q_{1}$, $q_{2}$, $q_{3}$, $q_{4}$}
* $\Sigma$ = {0, 1}
* $q_{0}$ = $q_{1}$
* F = {$q_{4}$}

with transition function $\delta$ described as follows:

* δ($q_{1}$, 0) = {$q_{1}$}
* δ($q_{1}$, 1) = {$q_{1}$, $q_{2}$}
* δ($q_{2}$, 0) = {$q_{3}$}
* δ($q_{2}$, 1) = {$q_{3}$}
* δ($q_{2}$, $\varepsilon$) = {$q_{3}$}
* δ($q_{3}$, 0) = {$q_{4}$}
* δ($q_{3}$, 1) = {$q_{4}$}
* δ($q_{3}$, $\varepsilon$) = {$q_{4}$}
* δ($q_{4}$, 0) = $\emptyset$
* δ($q_{4}$, 1) = $\emptyset$]

## 2.2 formal description of an NFA 

NFAs are formally described by a 5-tuple ( Q, $\Sigma$ , $\delta$, $q_{0}$ , F ) where: 

1. Q is a finite set of states 

2. $\Sigma$ is the alphabet (a finite set of symbols) 

3. $\delta$ : Q × $\Sigma$ $\varepsilon$ $\to$ P ( Q ) is the transition function 

4. $q_{0}$ $\in$ Q is the start state 

5. F $\subseteq$ Q is the set of accept states 

Where: 

$\Sigma$$\varepsilon$ = $\Sigma$ $\cup${$\varepsilon$} 

P ( Q ) is the collection of all subsets of Q ; called the power set of Q . 

For the NFA N2 given by: 

[Figure: A state diagram of a finite automata (Q, $\Sigma$, $\delta$, $q_{0}$, F) described as follows:

* Q = {$q_{1}$, $q_{2}$, $q_{3}$, $q_{4}$}
* $\Sigma$ = {0, 1}
* $q_{0}$ = $q_{1}$
* F = {$q_{4}$}

with transition function $\delta$ described as follows:

* δ($q_{1}$, 0) = {$q_{1}$}
* δ($q_{1}$, 1) = {$q_{1}$, $q_{2}$}
* δ($q_{1}$, $\varepsilon$) = $\emptyset$
* δ($q_{2}$, 0) = {$q_{3}$}
* δ($q_{2}$, 1) = {$q_{3}$}
* δ($q_{2}$, $\varepsilon$) = {$q_{3}$}
* δ($q_{3}$, 0) = {$q_{4}$}
* δ($q_{3}$, 1) = {$q_{4}$}
* δ($q_{3}$, $\varepsilon$) = {$q_{4}$}
* δ($q_{4}$, 0) = $\emptyset$
* δ($q_{4}$, 1) = $\emptyset$
* δ($q_{4}$, $\varepsilon$) = $\emptyset$]

A formal description of N 2 would involve a transition function $\delta$ as follows: 

* ($q_{1}$, 0) -> $q_{1}$
* ($q_{1}$, 1) -> {$q_{1}$, $q_{2}$}
* ($q_{1}$, $\varepsilon$) -> $\emptyset$
* ($q_{2}$, 0) -> $q_{3}$
* ($q_{2}$, 1) -> $q_{3}$
* ($q_{2}$, $\varepsilon$) -> $q_{3}$
* ($q_{3}$, 0) -> $q_{4}$
* ($q_{3}$, 1) -> $q_{4}$
* ($q_{3}$, $\varepsilon$) -> $q_{4}$
* ($q_{4}$, 0) -> $\emptyset$
* ($q_{4}$, 1) -> $\emptyset$
* ($q_{4}$, $\varepsilon$) -> $\emptyset$

## 2.3 converting NFAs to DFAs 

Two machines are equivalent if they recognize the same language. Any NFA can be converted into a DFA by building a DFA that has, as its set of states, the power set, P ( Q ), of the states in the NFA, Q . 

Consider the three state NFA N 3 with Q = { 1 , 2 , 3 } : 

[Figure: A state diagram of a finite automata (Q, $\Sigma$, $\delta$, $q_{0}$, F) described as follows:

* Q = {1, 2, 3}
* $\Sigma$ = {a, b}
* $q_{0}$ = 1
* F = {1}

with transition function $\delta$ described as follows:

* δ(1, a) = $\emptyset$
* δ(1, b) = {2}
* δ(1, $\varepsilon$) = {3}
* δ(2, a) = {2, 3}
* δ(2, b) = {3}
* δ(2, $\varepsilon$) = $\emptyset$
* δ(3, a) = {1}
* δ(3, b) = $\emptyset$
* δ(3, $\varepsilon$) = $\emptyset$]

Conversion into a DFA is done using the following steps: 

- draw the vertices for states P ( Q ) = {$\emptyset$, { 1 }, { 2 }, { 3 }, { 1 , 2 }, { 2 , 3 }, { 1 , 3 }, { 1 , 2 , 3 }} 

- change the start state to {{ 1,3 }} due to the $\varepsilon$ edge 

- change any states containing { 1 } to accept states 

- draw edges from Q = { 1 , 2 , 3 } that can be seen in N3 (black) 

- draw edges going to the state $\emptyset$ that cannot be seen in N3 (red) 

- draw the remaining edges from the remaining states {{ 1 , 2 }, { 2 , 3 }, { 1 , 3 }, { 1 , 2 , 3 }} (blue) 

[Figure: A state diagram of a finite automata (Q, $\Sigma$, $\delta$, $q_{0}$, F) described as follows:

* Q = {{1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}, {$\emptyset$}}
* $\Sigma$ = {a, b}
* $q_{0}$ = {1,3}
* F = {{1}, {1,2}, {1,3}, {1,2,3}}

with transition function $\delta$ described as follows:

* δ({1}, a) = {$\emptyset$} (red)
* δ({1}, b) = {2} (black)
* δ({2}, a) = {2,3} (black)
* δ({2}, b) = {3} (black)
* δ({3}, a) = {1,3} (black)
* δ({3}, b) = {$\emptyset$} (red)
* δ({1,2}, a) = {2,3} (blue)
* δ({1,2}, b) = {2,3} (blue)
* δ({1,3}, a) = {1,3} (blue)
* δ({1,3}, b) = {2} (blue)
* δ({2,3}, a) = {1,2,3} (blue)
* δ({2,3}, b) = {3} (blue)
* δ({1,2,3}, a) = {1,2,3} (blue)
* δ({1,2,3}, b) = {2,3} (blue)
* δ({$\emptyset$}, a) = {$\emptyset$} (red)
* δ({$\emptyset$}, b) = {$\emptyset$} (red)]

Because states {{ 1 }} and {{ 1,2 }} cannot be reached, they may be removed to simplify the machine: 

[Figure: A state diagram of a finite automata (Q, $\Sigma$, $\delta$, $q_{0}$, F) described as follows:

* Q = {{1,3}, {2}, {3}, {2,3}, {1,2,3}, {$\emptyset$}}
* $\Sigma$ = {a, b}
* $q_{0}$ = {1,3}
* F = {{1,3}, {1,2,3}}

with transition function $\delta$ described as follows:

* δ({1,3}, a) = {1,3} (blue)
* δ({1,3}, b) = {2} (blue)
* δ({2}, a) = {2,3} (black)
* δ({2}, b) = {3} (black)
* δ({3}, a) = {1,3} (black)
* δ({3}, b) = {$\emptyset$} (red)
* δ({2,3}, a) = {1,2,3} (blue)
* δ({2,3}, b) = {3} (blue)
* δ({1,2,3}, a) = {1,2,3} (blue)
* δ({1,2,3}, b) = {2,3} (blue)
* δ({$\emptyset$}, a) = {$\emptyset$} (red)
* δ({$\emptyset$}, b) = {$\emptyset$} (red)]

We can see some of the power of the NFA over that of the DFA by comparing with the original machine N3: 

[Figure: A state diagram of a finite automata (Q, $\Sigma$, $\delta$, $q_{0}$, F) described as follows:

* Q = {1, 2, 3}
* $\Sigma$ = {a, b}
* $q_{0}$ = 1
* F = {1}

with transition function $\delta$ described as follows:

* δ(1, a) = $\emptyset$
* δ(1, b) = {2}
* δ(1, $\varepsilon$) = {3}
* δ(2, a) = {2, 3}
* δ(2, b) = {3}
* δ(2, $\varepsilon$) = $\emptyset$
* δ(3, a) = {1}
* δ(3, b) = $\emptyset$
* δ(3, $\varepsilon$) = $\emptyset$]

## 2.4 closure under the regular operations 

A set L is closed under some operation if applying the operation to elements of L returns elements from L . The set of regular languages is closed under the regular operations (union, concatenation, and star). 

## 2.5 If languages A1 and A2 are regular, then A1 $\cup$ A2 is regular 

PROOF 1: 

Let M1 = ( Q1 , $\Sigma$ , $\delta$1 , $q_{1}$ , F1) recognize A1. 

Let M2 = ( Q2 , $\Sigma$ , $\delta$2 , $q_{2}$ , F2) recognize A2. 

Construct a finite automaton M = ( Q, $\Sigma$ , $\delta$, $q_{0}$ , F ) that recognizes A1 $\cup$ A2 

Let Q = Q1 × Q2 (the set of pairs of states). Then Q = { ( r1 , r2) |r1 $\in$ Q1 and r2 $\in$ Q2 } 

Let $\delta$ (( r1 , r2) , a ) = ( $\delta$1( r1 , a ) , $\delta$2( r2 , a )) for all a $\in$ $\Sigma$. Then M goes from a pair of states to another pair of states. 

Let $q_{0}$ = ( $q_{1}$ , $q_{2}$) be the starting pair of states 

Let F = { ( r1 , r2) |r1 $\in$ F1 or r2 $\in$ F2 } be the accepting pairs of states. 

PROOF 2: 

Let N1 = ( Q1 , $\Sigma$ , $\delta$1 , $q_{1}$ , F1) recognize A1. 

Let N2 = ( Q2 , $\Sigma$ , $\delta$2 , $q_{2}$ , F2) recognize A2. 

Construct N = ( Q, $\Sigma$ , $\delta$, $q_{0}$ , F ) that recognizes A1 $\cup$ A2 

Let Q = Q1 $\cup$ Q2 $\cup${$q_{0}$ } (combine all states and add a new start state $q_{0}$) 

Let F = F1 $\cup$ F2 (combine all accept states) 

Let the transition function $\delta(q, a)$ for any state $q \in Q$ and any symbol $a \in \Sigma$ be defined by the following conditions:

* If $q \in Q_1$, then $\delta(q, a) = \delta_1(q, a)$
* If $q \in Q_2$, then $\delta(q, a) = \delta_2(q, a)$
* If $q = q_0$ and $a = \varepsilon$, then $\delta(q, a) = \{q_1, q_2\}$
* If $q = q_0$ and $a \neq \varepsilon$, then $\delta(q, a) = \emptyset$