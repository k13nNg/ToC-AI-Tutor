>“A TM is a 7-tuple that can do everything a real computer can do.” 
>
>Michael Sipser (Theory of Computation Guru) 

# 6 Turing machines 

Turing machines are models of computers with unrestricted access to unlimited memory. They are more powerful than DFAs, NFAs, and PDAs; in other words they are more powerful than any finite automaton. 

- A Turing machine (TM) is a 7-tuple ( Q, $\Sigma$ , Γ , $\delta$, q 0 , $q_{\text{accept}}$, $q_{\text{reject}}$ ) where: 

   1. Q is a finite set of states 

   2. $\Sigma$ is the input alphabet where $\sqcup$  ̸$\in$ $\Sigma$ 

   3. Γ is the tape alphabet, where $\sqcup$ $\in$ Γ and $\Sigma$ $\subset$ Γ 

   4. $\delta$ : Q × Γ $\to$ Q × Γ × {L, R} is the transition function 

   5. $q_{0}$ $\in$ Q is the start state 

   6. $q_{\text{accept}}$ is the accept state 

   7. $q_{\text{reject}}$ is the reject state, where $q_{\text{accept}}$ = $q_{\text{reject}}$ 

## 6.1 the tape of a TM 

- starts on left side and then extends infinitely long to the right 

- initially contains the input string and an infinite number of blank symbols, $\sqcup$, to the right. 

- read and write head 

- head starts on the left side of the tape; which is the first input symbol 

## 6.2 the configuration of a TM 

During computations changes occur to the state, tape contents, and head position. These three items form the configuration, C , of the machine. 

The critical configurations are the: 

   - C1: start configuration with state q 0 

   - Caccept : accept configuration with state $q_{\text{accept}}$ 

   - Creject : reject configuration with state $q_{\text{reject}}$ 

- Caccept and Creject are halting configurations and do not yield further configurations. 

A TM accepts input w = w1w2...wn $\in$ $\Sigma$ [∗] if a sequence of configurations, {C1 , C2 , ..., Caccept} , exists. 

## 6.3 the transition function of a TM 

The transition function, $\delta$ : Q × Γ $\to$ Q × Γ × {L, R} , takes a (state, current tape element) pair and returns a (state, new tape element, direction) triple. Some examples of this are: 

- $\delta$ ( $q_{1}$ , a ) = ( $q_{2}$ , b, R ). “transition from $q_{1}$ to $q_{2}$ when the head reads a on the tape, write b on the tape (re-writing the a), and then move the head one symbol to the right on the tape” . The state diagram label for this would be: a $\to$ b, R . 

- $\delta$ ( $q_{3}$ , c ) = ( $q_{4}$ , c, L ). “transition from $q_{3}$ to $q_{4}$ when the head reads c on the tape, write c on the tape (c is not changed), and then move the head one symbol to the left on the tape” . The state diagram label for this would be: c $\to$ L . 

## 6.4 TM example: is thing1 the same as thing2? 

Suppose we want a machine that compares two things to see if they are identical. As input the machine is given thing1, then a single delimiter, then thing2. If thing1=thing2 the machine accepts the input, otherwise it rejects. 

Let thing1 and thing2 be represented by by binary strings and the delimiter by #. 

Then a possible input string for this machine is: w = 01101....101 # 01101....101. 

Let M1 be a TM that tests if an input string belongs to {a # a|a $\in${ 0 , 1 }^* } . An informal description of M 1 is: 

On input string w : 

1. Check corresponding symbols on either side of #. If corresponding symbols are not the same, reject. Re-write each checked symbol with “x”. If no # is found, or if more that one occurrence of # is found in the input, reject. 

2. When all symbols on left of # have been re-written, check for any remaining (non re-written symbols) on right of #. If any symbols remain on right, reject, otherwise accept. 

A formal description of M1 is given by M1 = ( Q, $\Sigma$ , Γ , $\delta$, $q_{1}$ , $q_{\text{accept}}$, $q_{\text{reject}}$ ) where: 

- Q = {$q_{1}$ , $q_{2}$ , $q_{3}$ , $q_{4}$ , $q_{5}$ , $q_{6}$ , $q_{7}$ , $q_{8}$ , $q_{\text{accept}}$, $q_{\text{reject}}$} 

- $\Sigma$ = { 0 , 1 , # } 

- Γ = { 0 , 1 , # , x, } 

- $\delta$ is given by the following state diagram : 

[Figure: A state diagram of a Turing Machine (Q, $\Sigma$, Γ, $\delta$, $q_{0}$, $q_{accept}$, $q_{reject}$) described as follows:

* Q = {$q_{1}$, $q_{2}$, $q_{3}$, $q_{4}$, $q_{5}$, $q_{6}$, $q_{7}$, $q_{8}$, $q_{accept}$}
* $\Sigma$ = {0, 1, #}
* Γ = {0, 1, #, x, $\sqcup$}  *(where $\sqcup$ represents the blank symbol)*
* $q_{0}$ = $q_{1}$
* $q_{accept}$ = $q_{accept}$
* $q_{reject}$ = implicit for any undefined transitions

with transition function $\delta$ described as follows (format: δ(state, read) = (nex$t_{state}$, write, direction)):

* δ($q_{1}$, 0) = ($q_{2}$, x, R)
* δ($q_{1}$, 1) = ($q_{3}$, x, R)
* δ($q_{1}$, #) = ($q_{8}$, #, R)
* δ($q_{2}$, 0) = ($q_{2}$, 0, R)
* δ($q_{2}$, 1) = ($q_{2}$, 1, R)
* δ($q_{2}$, #) = ($q_{4}$, #, R)
* δ($q_{3}$, 0) = ($q_{3}$, 0, R)
* δ($q_{3}$, 1) = ($q_{3}$, 1, R)
* δ($q_{3}$, #) = ($q_{5}$, #, R)
* δ($q_{4}$, 0) = ($q_{6}$, x, L)
* δ($q_{4}$, x) = ($q_{4}$, x, R)
* δ($q_{5}$, 1) = ($q_{6}$, x, L)
* δ($q_{5}$, x) = ($q_{5}$, x, R)
* δ($q_{6}$, 0) = ($q_{6}$, 0, L)
* δ($q_{6}$, 1) = ($q_{6}$, 1, L)
* δ($q_{6}$, #) = ($q_{7}$, #, L)
* δ($q_{6}$, x) = ($q_{6}$, x, L)
* δ($q_{7}$, 0) = ($q_{7}$, 0, L)
* δ($q_{7}$, 1) = ($q_{7}$, 1, L)
* δ($q_{7}$, x) = ($q_{1}$, x, R)
* δ($q_{8}$, x) = ($q_{8}$, x, R)
* δ($q_{8}$, $\sqcup$) = ($q_{accept}$, $\sqcup$, R)]

The following shows the sequence of configurations for M 1 on input w = 01#01. 

Note that 01#01 $\in${a # a|a $\in${ 0 , 1 }[∗] } so we expect Caccept . 

Comments appear on the right for all state transitions: 
* Step 1: Configuration $\sqcup$$q_{101}$#01$\sqcup$ $\rightarrow$ found 0. Apply $\delta(q1, 0) = (q2, x, R)$
* Step 2: Configuration $\sqcup$xq21#01$\sqcup$
* Step 3: Configuration $\sqcup$x1q2#01$\sqcup$ $\rightarrow$ found #. Apply $\delta(q2, \#) = (q4, \#, R)$
* Step 4: Configuration $\sqcup$x1#$q_{401}$$\sqcup$ $\rightarrow$ found 0. Apply $\delta(q4, 0) = (q6, x, L)$
* Step 5: Configuration $\sqcup$x1q6#x1$\sqcup$ $\rightarrow$ found #. Apply $\delta(q6, \#) = (q7, \#, L)$
* Step 6: Configuration $\sqcup$xq71#x1$\sqcup$
* Step 7: Configuration $\sqcup$q7x1#x1$\sqcup$ $\rightarrow$ found x. Apply $\delta(q7, x) = (q1, x, R)$
* Step 8: Configuration $\sqcup$xq11#x1$\sqcup$ $\rightarrow$ found 1. Apply $\delta(q1, 1) = (q3, x, R)$
* Step 9: Configuration $\sqcup$xxq3#x1$\sqcup$ $\rightarrow$ found #. Apply $\delta(q3, \#) = (q5, \#, R)$
* Step 10: Configuration $\sqcup$xx#q5x1$\sqcup$
* Step 11: Configuration $\sqcup$xx#xq51$\sqcup$ $\rightarrow$ found 1. Apply $\delta(q5, 1) = (q6, x, L)$
* Step 12: Configuration $\sqcup$xx#q6xx$\sqcup$
* Step 13: Configuration $\sqcup$xxq6#xx$\sqcup$ $\rightarrow$ found #. Apply $\delta(q6, \#) = (q7, \#, L)$
* Step 14: Configuration $\sqcup$xq7x#xx$\sqcup$ $\rightarrow$ found x. Apply $\delta(q7, x) = (q1, x, R)$
* Step 15: Configuration $\sqcup$xxq1#xx$\sqcup$ $\rightarrow$ found #. Apply $\delta(q1, \#) = (q8, \#, R)$
* Step 16: Configuration $\sqcup$xx#q8xx$\sqcup$
* Step 17: Configuration $\sqcup$xx#xq8x$\sqcup$
* Step 18: Configuration $\sqcup$xx#xxq8$\sqcup$ $\rightarrow$ found end of input. Apply $\delta(q8, ⊔) = (qaccept, ⊔, R)$
* Step 19: Configuration $\sqcup$xx#xx$\sqcup$$q_{\text{accept}}$$\sqcup$

We have reached Caccept = xx # xx $q_{\text{accept}}$ . Therefore the input w = 01#01 is accepted. 

The following shows the sequence of configurations for M 1 on input w = 0##01. 

Note that 0##01 ̸$\in${a # a|a $\in${ 0 , 1 }[∗] } so we expect Creject . 

Comments appear on the right for all state transitions: 

* Step 1: Configuration $q_{10}$##01$\sqcup$ $\rightarrow$ found 0. Apply $\delta(q1, 0) = (q2, x, R)$
* Step 2: Configuration xq2##01$\sqcup$ $\rightarrow$ found #. Apply $\delta(q2, \#) = (q4, \#, R)$
* Step 3: Configuration x#$q_{4}$#01$\sqcup$ $\rightarrow$ found another #. Apply $\delta(q4, \#) = (qreject)$
* Step 4: Configuration x#$q_{\text{reject}}$#01$\sqcup$

We have reached Creject = x#$q_{\text{reject}}$#01. Therefore the input w = 0##01 is not accepted. 


## 6.5 multi-tape TMs 

A multi-tape TM has k tapes, where the input w appears initially on tape k = 1, with all other tapes blank. 

The general transition function for a k tape TM is $\delta$ : Q × Γ^k $\to$ Q × Γ^k × {L, R, S}^k . 

- {L, R, S}^k allows for some tape heads to “stay” while others move left or right. 

For example, a k = 3 tape TM could have $\delta$ ( $q_{1}$ , a1 , a2 , a3) = ( $q_{6}$ , b1 , b2 , b3 , L, R, S ) 

If this TM was in state $q_{1}$ with tape head 1 over a1, tape head 2 over a2, and tape head 3 over a3 it would: 

- transition to state $q_{6}$ 

- write b1 to tape 1 and move the head of tape 1 left 

- write b2 to tape 2 and move the head of tape 2 right 

- write b3 to tape 3 and not move the head of tape 3 

## 6.6 non-deterministic TMs 

A non-deterministic TM allows for different sequences of configurations to be computed in parallel. 

The general transition function for non-deterministic TM is $\delta$ : Q × Γ $\to$ P ( Q × Γ × {L, R} ). 

For example, a non-deterministic TM could have $\delta$ ( $q_{1}$ , a ) = { ( $q_{2}$ , b, R ) , ( $q_{5}$ , c, L ) , ( $q_{8}$ , d, R ) } . 

Such a transition would allow the TM to split into three possible configuration sequences. For example if the current configuration in a sequence was yzq 1 ay , then $\delta$ ( q 1 , a ) would split this sequence into three parallel configuration sequences: 

$$
\begin{matrix}
 & \vdots & \\
 & yz$q_{1ay}$ & \\
yzb$q_{2y}$ & y$q_{5zcy}$ & yzd$q_{8y}$ \\
\vdots & \vdots & \vdots
\end{matrix}
$$