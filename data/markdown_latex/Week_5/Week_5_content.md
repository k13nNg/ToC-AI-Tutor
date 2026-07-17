>“It has no pretensions whatever to originate anything. 
>
>It can do whatever we know how to order it to perform.” 
>
>Ada Lovelace (Original Computer Programmer) 

# 5 Pushdown automata 

A pushdown automaton (PDA) is a 6-tuple ( Q, $\Sigma$ , Γ , $\delta$, q 0 , F ) where: 

1. Q is a finite set of states 

2. $\Sigma$ is the input alphabet 

3. Γ is the stack alphabet 

4. $\delta$ : Q × $\Sigma$$\varepsilon$ × Γ$\varepsilon$ $\to$ P ( Q × Γ$\varepsilon$ ) is the transition function 

5. $q_{0}$ $\in$ Q is the start state 

6. F $\subseteq$ Q is the set of accept states 

Transition functions in PDAs are more complex than DFAs and NFAs because they take a (state, input, stack) triple and return a (state, stack) pair, but they also can be non-deterministic and return sets of (state, stack) pairs. 

A deterministic transition function could be: $\delta$ ( $q_{1}$ , w, a ) = ( $q_{2}$ , b ) 

A non-deterministic transition function could be: $\delta$ ( $q_{1}$ , w, a ) = { ( $q_{2}$ , b ) , ( $q_{3}$ , c ) , ( $q_{3}$ , d ) , ...} 

where: 
* $q_{i}$ $\in$ Q 
* w $\in$ $\Sigma$$\varepsilon$ 
* a, b, c, d $\in$ Γ $\varepsilon$ 

## 5.1 PDA state diagrams 

State diagrams of PDAs require arrow labels that show the input, the element on top of the stack required for the transition to occur, and finally any modifications to the top of the stack. Some general examples follow: 

* w, a $\to$ b : transition happens on input w when a is on top of the stack and a is replaced by b ( a is popped and b is pushed). 

* w, $\varepsilon$ $\to$ b : transition happens on input w when anything is on top of the stack and b is added to the top of the stack. (nothing is popped and b is pushed). 

* w, b $\to$ $\varepsilon$ : transition happens on input w when b is on top of the stack and b is deleted from the top of the stack. ( b is popped and nothing is pushed). 

## 5.2 PDA example 

Here is the state diagram of a PDA, M 1, that recognizes the language A = { $0^{n}$ $1^{n}$ |$n \geq 1$ } : 

[Figure: A state diagram of a pushdown automaton M1 = (Q, $\Sigma$, Γ, $\delta$, $q_{0}$, F) described as follows:

* Q = {$q_{1}$, $q_{2}$, $q_{3}$, $q_{4}$}
* $\Sigma$ = {0, 1}
* Γ = {0, $}
* $q_{0}$ = $q_{1}$
* F = {$q_{4}$}

with transition function $\delta$ described as follows:

* δ($q_{1}$, $\varepsilon$, $\varepsilon$) = {($q_{2}$, $)}
* δ($q_{2}$, 0, $\varepsilon$) = {($q_{2}$, 0)}
* δ($q_{2}$, 1, 0) = {($q_{3}$, $\varepsilon$)}
* δ($q_{3}$, 1, 0) = {($q_{3}$, $\varepsilon$)}
* δ($q_{3}$, $\varepsilon$, $) = {($q_{4}$, $\varepsilon$)}]

We have that Γ = { 0 , \$ } , where \$ is used to mark the start of the stack. 

When $ is popped the PDA has reached the end of the stack. 

In the case of M1, when $ is popped we have met the criteria of 0s followed by the same number of 1s described by A . 

Since $q_{1}$ is not an accept state we have that $\varepsilon$  ̸$\in$ B . 

## 5.3 another PDA example 

Here is the state diagram of a PDA, M2, that recognizes the language B = {w$w^{R}$ |w $\in${ 0 , 1 }^* } : 

[Figure: A state diagram of a pushdown automaton (Q, $\Sigma$, Γ, $\delta$, $q_{0}$, F) described as follows:

* Q = {$q_{1}$, $q_{2}$, $q_{3}$, $q_{4}$}
* $\Sigma$ = {0, 1}
* Γ = {0, 1, $}
* $q_{0}$ = $q_{1}$
* F = {$q_{1}$, $q_{4}$}

with transition function $\delta$ described as follows:

* δ($q_{1}$, $\varepsilon$, $\varepsilon$) = {($q_{2}$, $)}
* δ($q_{2}$, 0, $\varepsilon$) = {($q_{2}$, 0)}
* δ($q_{2}$, 1, $\varepsilon$) = {($q_{2}$, 1)}
* δ($q_{2}$, $\varepsilon$, $\varepsilon$) = {($q_{3}$, $\varepsilon$)}
* δ($q_{3}$, 0, 0) = {($q_{3}$, $\varepsilon$)}
* δ($q_{3}$, 1, 1) = {($q_{3}$, $\varepsilon$)}
* δ($q_{3}$, $\varepsilon$, $) = {($q_{4}$, $\varepsilon$)}]

We have that Γ = { 0 , 1 , \$ } , where \$ is used to mark the start of the stack. 

In the case of M 2, when \$ is popped we have met the criteria writing a string, w , forwards and then in reverse, $w^{R}$ , described by B . 

Since $q_{1}$ is an accept state we have that $\varepsilon$ $\in$ B . 

## 5.4 equivalence of PDAs and CFGs 

A context-free language is any language that can be described by a CFG. 

Theorem: A language is context-free if and only if some PDA recognizes it. 

Using the CFG G = ( V, $\Sigma$ , R, S ) that describes the language, construct a general three state non-deterministic PDA, P that recognizes the language: 

[Figure: A state diagram of a pushdown automaton (Q, $\Sigma$, Γ, $\delta$, $q_{0}$, F) described as follows:

* Q = {$q_{start}$, $q_{loop}$, $q_{end}$}
* $\Sigma$ = {a}
* Γ = {A, S, a, $}
* $q_{0}$ = $q_{start}$
* F = {$q_{end}$}

with transition function $\delta$ described as follows:

* δ($q_{start}$, $\varepsilon$, $\varepsilon$) = {($q_{loop}$, S$)}
* δ($q_{loop}$, $\varepsilon$, A) = {($q_{loop}$, w)}
* δ($q_{loop}$, a, a) = {($q_{loop}$, $\varepsilon$)}
* δ($q_{loop}$, $\varepsilon$, $) = {($q_{end}$, $\varepsilon$)}]

for all production rules A $\to$ w $\in$ R , and for all terminals a $\in$ $\Sigma$. 

- P starts by pushing $, then S to the stack. 

- The non-deterministic loop state contains a transition for all possible production rules. Any terminals are pushed to the stack. 

- This means that P can derive all strings in the language, and there exists a copy of P that has any given string in the language in it’s stack. 

- That copy of P then goes through the input string, and if it matches the elements in the stack, the stack will empty to $. 

- If $ is found on the top of the stack it is popped, and the input is accepted. 

## 5.5 pumping lemma for context-free languages 

If B is a context-free language, then there is a number p (the pumping length) where if s is any string in b of length at least p , then s may be divided into fve pieces, s = uvxyz , such that: 

1. for each $i \geq 0$ , u$v^{i}$ x$y^{i}$ z $\in$ B 

2. $|vy| > 0$ 

3. |vxy| ≤ p 

## 5.6 example 

Show that B = {$a^{n}$ $b^{n}$ $c^{n}$ |$n \geq 0$ } is not context-free. 

Assume, for the purpose of finding a contradiction, that B is context-free. 

Let s = $a^{p}$ $b^{p}$ $c^{p}$ 

Then s $\in$ B and $|s| = 3$ p which is greater than p , the pumping length. 

The pumping lemma guarantees that u$v^{i}$ x$y^{i}$ z $\in$ B for any $i \geq 0$. There are two cases for the substrings v and y which both lead to contradictions: 

- v and y contain only one type of alphabet element (for example v = bbb and y = bb . Then uvvxyyz has more of one type of alphabet element and therefore u$v^{2}$ x$y^{2}$ z $\in$/ B 

- v and y contain different types of alphabet elements (for example v = abbb and y = bc . Then uvvxyyz may have the same number of each type, but the elements will not be in the correct oder. Therefore u$v^{2}$ x$y^{2}$ z $\in$/ B 

Because the assumption that B is context-free always leads to a contradiction, we conclude that B is not context-free. 