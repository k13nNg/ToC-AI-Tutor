>“I lost my fighting spirit. I was emptied completely.” 
>
>Garry Kasparov (after losing in 19 moves to Deep Blue) 

# 9 Undecidable problems 

Let’s prove that A TM = {$\langle$M, w$\rangle$|M is a TM that accepts input string w} is an undecidable language. 

Assume, for the purposes of finding a contradiction, that H is a decider for A TM: 

[# Computability Theory: The Hypothetical Decider for the Acceptance Problem ($A_{TM}$)

Concept Overview: This equation defines a hypothetical Turing Machine, $H$, which acts as a decider for the Acceptance Problem. It takes as input an encoded Turing Machine $\langle M \rangle$ and an input string $w$. The machine $H$ attempts to determine whether machine $M$ will eventually accept the string $w$. 

Mathematical Definition:
$$
H(\langle M, w \rangle) = \begin{cases} 
\text{accept} & \text{if } M \text{ accepts } w \\ 
\text{reject} & \text{if } M \text{ does not accept } w 
\end{cases}
$$

Theoretical Implications (The Undecidability Proof):
* The "Does Not Accept" Clause: The critical part of this definition is the phrase "does not accept". For $H$ to be a true decider, it must be able to output "reject" even if machine $M$ enters an infinite loop on input $w$. 
* Proof by Contradiction: In computability theory, this equation is introduced exclusively to prove that machine $H$ cannot exist. Alan Turing proved that it is impossible to construct a general algorithm that can perfectly determine if arbitrary computer programs will halt or loop forever. 
* The Paradox: If a RAG user asks about this equation, the system must know that assuming $H$ exists leads directly to a paradox (usually by constructing a secondary machine, $D$, that does the exact opposite of what $H$ predicts). Therefore, the language $A_{TM}$ is Turing-recognizable, but undecidable.]

Now build a new TM, D , that uses H to determine if any TM M accepts a description of itself, $\langle$M $\rangle$ , and returns the opposite: 

- D = On input $\langle$M $\rangle$ : 

   1. Run H on $\langle$M, $\langle$M $\rangle$$\rangle$ . 

   2. If H accepts then reject. 

   3. If H rejects then accept. 

- If we run D on a description of any TM M , $\langle$M $\rangle$ , we have the following two possible cases: 

   - H ( $\langle$M, $\langle$M $\rangle$$\rangle$ ) = accept. Then M accepts $\langle$M $\rangle$ , and D does not accept $\langle$M $\rangle$ . 

   - H ( $\langle$M, $\langle$M $\rangle$$\rangle$ ) = reject. Then M does not accept $\langle$M $\rangle$ , and D accepts $\langle$M $\rangle$ . 

But D is itself a TM... If we run D on a description of itself, $\langle$D$\rangle$ , we have the following two possible cases; each of which is a contradiction: 

- H ( $\langle$D, $\langle$D$\rangle$$\rangle$ ) = accept. Then D accepts $\langle$D$\rangle$ , and D does not accept $\langle$D$\rangle$ . 

   - (In other words H has “decided” that D accepts w = $\langle$D$\rangle$ , but D actually rejects w = $\langle$D$\rangle$ ) 

- H ( $\langle$D, $\langle$D$\rangle$$\rangle$ ) = reject. Then D does not accept $\langle$D$\rangle$ , and D accepts $\langle$D$\rangle$ . 

(In other words H has “decided” that D rejects w = $\langle$D$\rangle$ , but D actually accepts w = $\langle$D$\rangle$ ) Therefore H , a decider for A TM, cannot exist. 

We have proven that A TM is an undecidable language. 

joshua.schneider@sheridancollege.ca 

page1 

INFO47546 

Theory of Computation 

Week9 

## 9.1 the halting problem 

Let HALT TM = {$\langle$M, w$\rangle$|M is a TM that halts on input string w} . Prove that HALT TM is an undecidable language. 

Assume, for the purposes of finding a contradiction, that R is a decider for HALT TM: 

[# Computability Theory: The Hypothetical Decider for the Halting Problem ($HALT_{TM}$)

Concept Overview: This equation defines a hypothetical Turing Machine, $R$, designed to act as a decider for the Halting Problem. It takes as input an encoded Turing Machine $\langle M \rangle$ and an input string $w$. The machine $R$ attempts to determine whether machine $M$ will eventually stop running (either by accepting or rejecting) when processing $w$, or if it will get stuck in an infinite loop.

Mathematical Definition:
$$
R(\langle M, w \rangle) = \begin{cases} 
\text{accept} & \text{if } M \text{ halts on input } w \\ 
\text{reject} & \text{if } M \text{ does not halt on input } w 
\end{cases}
$$

Theoretical Implications (The Undecidability Proof):
* Halting vs. Accepting: Unlike the Acceptance Problem ($A_{TM}$) which requires the machine to specifically reach an "accept" state, $HALT_{TM}$ only requires the machine to finish its computation. If $M$ halts and rejects $w$, $R$ still outputs "accept" because $M$ successfully halted.
* The "Does Not Halt" Clause: For $R$ to be a valid decider, it must be able to affirmatively output "reject" when $M$ enters an infinite loop. 
* Proof by Contradiction: Similar to the $A_{TM}$ proof, this equation is introduced in computability theory exclusively to prove that machine $R$ cannot exist. Alan Turing famously proved that the Halting Problem is undecidable; there is no general algorithm that can analyze an arbitrary program and perfectly predict if it will run forever.
* RAG Context Guardrail: If a user searches for methods to "detect if a Turing machine loops forever," the RAG system must use this context to correctly explain that while heuristic loop-checkers exist for specific cases, a general-purpose decider $R$ is mathematically impossible.]

Now build a new TM, S , that uses R to decide A TM: 

- S = On input $\langle$M, w$\rangle$ : 

   1. Run R on $\langle$M, w$\rangle$ . 

   2. If R rejects then reject. 

   3. If R accepts then simulate M on w until it halts. 

   4. If M accepts, accept. 

   5. If M rejects, reject. 

Note that if R accepts $\langle$M, w$\rangle$ then M must halt on w ... it cannot go on indefinitely. Therefore S decides the language {$\langle$M, w$\rangle$|M is a TM that accepts input string w} , which is A TM. 

But this is a contradiction because we have proven that A TM is undecidable. 

Therefore R , a decider for HALT TM, cannot exist. 

We have proven that HALT TM is an undecidable language. 


## 9.2 TMs with limited memory 

A linear bounded automaton (LBA) is a TM that can only solve problems requiring memory that can fit within the tape used for input. In other words, an LBA does not have an infinite number of blank symbols, $\sqcup$, to the right of the input; the tape just stops there. An interesting feature of LBAs is that they have a finite number of distinct configurations, C distinct. 

Consider an LBA described by a TM 7-tuple ( Q, $\Sigma$ , Γ , $\delta$, $q_{0}$ , $q_{a}$, $q_{r}$ ) where: 

- Q = {$q_{0}$, $q_{1}$, $q_{2}$, $q_{a}$, $q_{r}$} 

- $\Sigma$ = { 0 , 1 } 

- Γ = $\Sigma$ $\cup${x, $\sqcup$} 

For the 3-bit input w = 110 we can only use 3 locations for memory. The symbols for those locations are { 0 , 1 , x, $\sqcup$} . So we have a total of $4^{3}$ =64 different possible memory strings. For each of these strings, the tape head can be over one of 3 positions, and for each of the string-position pairs, there are 5 states possible. Therefore, this LBA has a total of 5 × 3 × $4^{3}$ distinct configurations. 

Let A LBA = {$\langle$M, w$\rangle$|M is a LBA that accepts input string w} . 

Prove that A LBA is, wait for it..., decidable! 

We can construct a TM, L , that recognizes and decides A LBA: 

On input $\langle$M, w$\rangle$ : 

1. Compute the total number of distinct configurations, C distinct, of M ( M is an LBA; a TM with input tape limited memory). 

2. Simulate M on input string w for a maximum of C distinct steps. 

3. If at any point M enters its accept state, then accept $\langle$M, w$\rangle$ . 

4. If at any point M enters its reject state, then reject $\langle$M, w$\rangle$ . 

5. If M has not halted after C distinct steps, then reject. 

Note that L can determine if M will not halt on input string w ; if it reaches C distinct steps and has not halted, it never will halt because the next step must lead to a previous configuration which creates an infinite loop of configurations. In other words, M may continue indefinitely and not halt on input w , but L knows exactly when this will happen so it can reject at that point. 

We have that L is a decider for A LBA, therefore A LBA is a decidable language. 