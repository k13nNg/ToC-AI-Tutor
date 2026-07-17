>“The biggest issue I see with AI is that the so-called experts think they know more than they do, and they think they are smarter than they actually are.” 
>
>Elon Musk (speaking about the dangers of AI) 

# 8 Recognizers and Deciders 

## 8.1 Recognizers 

A language is Turing-recognizable if and only if some TM recognizes it. 

For a TM to be a recognizer for a language, the set of all strings that the TM accepts must be the language. 

## 8.2 example of a recognizer 

Consider the language L = {p ( x ) |p ( x ) is a polynomial with an integer root } 

We can construct a TM, M 1, to recognize L using the following informal description: 

On input p ( x ): 

1. Evaluate p ( x ) for the integers x = 0 , 1 , − 1 , 2 , − 2 , 3 , − 3 , ... 

2. If at any point p ( x ) = 0 then accept p ( x ). 

If p ( x ) has an integer root then M1 will eventually find it. 

Note that if p ( x ) doesn’t have an integer root, then M 1 will never accept; it will just keep searching. 

## 8.3 specific example of a recognizer (using python) 

Let L = {p ( x ) |p ( x ) is a 3rd degree polynomial with an integer root } 

Let M1 be a TM that recognizes L . Then a “High-level” description of M1 (using commented python code) is: 

[# Python Implementation: Turing Machine Recognizer for 3rd-Degree Polynomial Integer Roots

Concept Overview: This code implements a Turing Machine ($M_1$) that acts as a recognizer for a formal language $L$ (3rd-degree polynomials with integer roots). Unlike a decider, it uses an unbounded while loop to search incrementally outward from zero ($0, 1, -1, 2, -2 \dots$). If an integer root exists, the machine halts and accepts. If no integer root exists, the machine never halts (loops infinitely), demonstrating the classic behavior of a recognizable but non-decidable execution path.

Mathematical & Theoretical Components:
* Polynomial Evaluation ($p_{x}$): Evaluates a cubic polynomial $p(x) = c_1 x^3 + c_2 x^2 + c_3 x + c_4$ for a given $x$ using a list of coefficients c.
* Turing Machine Recognizer ($M_{1}$): Iterates through integers starting at $x=0$. Inside the loop, it checks both positive $x$ and negative $-x$ simultaneously. It lacks a mathematical bound (unlike a decider), meaning it cannot affirmatively output 'reject'.
* Execution State (Halting vs. Looping): * $M_{1}$([2, -9, 8, 3]) successfully finds a root and halts with 'accept'.
   * $M_{1}$([1, -2, 0, 2]) encounters a polynomial with no integer roots. Because $M_1$ is only a recognizer, it enters an infinite loop (denoted by the hanging In [*] state in Jupyter/IPython) and fails to halt.

Source Code:
python
#3rd degree polynomial: p(x) = c1*$x^{3}$ + c2*$x^{2}$ + c3*x + c4
#coefficient list: c = [c1,c2,c3,c4]
def $p_{x}$(x,c):
    value = c[0]*x3 + c[1]*x2 + c[2]*x1 + c[3]
    return(value)

#Turing Machine $M_{1}$ that recognizes L
#$M_{1}$ uses input [c1,c2,c3,c4] as the encoding of p(x)
def $M_{1}$(c):
    x=0
    while $p_{x}$(x,c)!=0 and $p_{x}$(-x,c)!=0:
        x+=1
    return('accept')

# Example Executions
# Halts and accepts:
# $M_{1}$([2, -9, 8, 3]) 
# Out: 'accept'

# Infinite loop (fails to halt):
# $M_{1}$([1, -2, 0, 2])

]

Here we see that M 1 accepts the input of the encoding of p ( x ) = 2 $x^{3}$ − 9 $x^{2}$ + 8 x + 3, because of the integer root found at x = 3. But M 1 goes into an infinite loop on the input of the encoding of p ( x ) = 1 $x^{3}$ − 2 $x^{2}$ + 0 x + 2 because no integer root exists for this 3rd degree polynomial: 

[Figure: Graph of the function p(x) = 2$x^{3}$ - 9$x^{2}$ + 8x + 3, with 3 roots highlighted: (1.781, 0), (-0.281, 0) and (3,0)]

[Figure: Graph of the function p(x) = 1$x^{3}$ - 2$x^{2}$+0x + 2, with 1 root (-0.839, 0)]


## 8.4 Deciders 

A language is Turing-decidable if and only if some TM decides it. 

For a TM to be a decider for a language it must: 

- be a recognizer for the language 

- reject all strings that are not part of the language 

In other words, a decider for some language L must be able to accept any string w $\in$ L and also reject any string w $\in$/ L . 

Deciders can be used to recognize the complement of a language, L = {w|w $\in$/ L} . A consequence of this is that a decider must halt (eventually reach a Caccept or Creject configuration) on all inputs. It cannot go into an infinite loop. 

## 8.5 example of a decider 

To convert M1 into a decider, we need to give it some way of halting. This is done by using a bound for x given by: 

$|x| < k$ (c{max}. $c_{1}$)>

Where k is the number of terms in p ( x ), c max is the coefficient with the largest absolute value, and c1 is the coefficient of the highest order term. 

We can construct a TM, M2, that decides L using the following informal description: 

On input p ( x ): 

1. While $|x| < k$ (c_{max}/ c1) : Evaluate p ( x ) for the integers x = 0 , 1 , − 1 , 2 , − 2 , 3 , − 3 , ... c1 

2. If at any point p ( x ) = 0 then accept p ( x ). 

3. Otherwise; reject p ( x ). 

If p ( x ) has an integer root then M2 will eventually find it and accept p ( x ). If p ( x ) doesn’t have an integer root within the bound for x , then M2 will reject p ( x ). So M2 decides L . 


## 8.6 specific example of a decider (using python) 

Let L = {p ( x ) |p ( x ) is a 3rd degree polynomial with an integer root } 

Let M3 be a TM that decides L . Then a “High-level” description of M3 (using commented python code) would be: 

[Python Implementation: Turing Machine Decider for 3rd-Degree Polynomial Integer Roots

Concept Overview: This code implements a Turing Machine ($M_3$) that acts as a decider for a specific formal language $L$. It determines if a given 3rd-degree polynomial has an integer root. It solves this by calculating a finite mathematical bound for potential roots and checking all integers within that range. 

Mathematical Components:
* Polynomial Evaluation ($p_{x}$): Evaluates a cubic polynomial of the form $p(x) = c_1 x^3 + c_2 x^2 + c_3 x + c_4$ given a specific $x$ and a list of coefficients.
* Root Bounding (bound): Calculates the maximum absolute value a root could take using the formula $k \cdot \frac{c_{max}}{|c_1|}$, where $k$ is the number of coefficients, $c_{max}$ is the maximum absolute coefficient, and $c_1$ is the leading coefficient.
* Turing Machine Decider ($M_{3}$): Uses the calculated bounds to iterate through a finite range of integers. If a root is found ($p_{x}$ == 0), the TM halts and accepts. If the loop finishes without finding a root, the TM halts and rejects.

Source Code:
python
#3rd degree polynomial: p(x) = c1*$x^{3}$ + c2*$x^{2}$ + c3*x + c4
#coefficient list: c = [c1,c2,c3,c4]
def $p_{x}$(x,c):
    value = c[0]*$x^{3}$ + c[1]*$x^{2}$ + c[2]*$x^{1}$ + c[3]
    return(value)

#bound for x:
def bound(c):
    $c_{max}$=max([abs(i) for i in c])
    $c_{1}$=c[0]
    k=len(c)
    return(k*($c_{max}$ / abs($c_{1}$)))

#Turing Machine $M_{3}$ that decides L
#$M_{3}$ uses input [c1,c2,c3,c4] as the encoding of p(x)
def $M_{3}$(c):
    for x in range(int(-bound(c)),int(+bound(c))):
        if $p_{x}$(x,c)==0:
            return('accept')
    #otherwise reject
    return('reject')]

M3 accepts the input of the encoding of p ( x ) = 2 $x^{3}$ − 9 $x^{2}$ + 8 x + 3, because of the integer root found at x = 3. 

M3 rejects the encoding of p ( x ) = 1 $x^{3}$ − 2 $x^{2}$ + 0 x + 2 because no integer root was found for this 3rd degree polynomial within the bounds of $|x| < k$(c{max} c1) = 4*{2/1}=8 or -8 < x < 8. 

## 8.7 TMs as descriptions of algorithms 

The Church-Turing thesis gives a connection between algorithms and TMs; any TM that decides a language can be used as a description of an algorithm for that language. We have the following levels of detail to describe TMs, each of which represents a description of an equivalent algorithm: 

- Formal: A complete description (using math) of the 7-tuple ( Q, $\Sigma$ , Γ , $\delta$, q 0 , $q_{\text{accept}}$, $q_{\text{reject}}$ ) including all states and transitions within $\delta$ . 

- Implementation: A description (using English) of how the head moves and writes data to the tape on an input string. 

- High-level: A description (using code, math, English, etc...) of the algorithm used to describe the language. 

For obvious reasons we are going to use “High-level” descriptions, using commented python code or math. 

## 8.8 Encodings 

Let the encoding an object, “object”, into it’s representation as a string be $\langle$ “object” $\rangle$ . 

For example, the polynomial p ( x ) = 2 $x^{3}$ − 9 $x^{2}$ + 8 x + 3 has encoding: $\langle$p ( x ) $\rangle$ = [2 , − 9 , 8 , 3]. 

When testing if an object is an element of a language we can modify the description of the language to involve the encoding of the object, instead of the actual object. 

For example, the language L = {$\langle$p ( x ) $\rangle$|p ( x ) is a 3rd degree polynomial with an integer root } is the set of all encodings, $\langle$p ( x ) $\rangle$ , of 3rd degree polynomials with an integer root. 

We can then using the encodings as inputs for the TM that either recognize or decide L . 

Recall that p ( x ) = 2 $x^{3}$ − 9 $x^{2}$ +8 x +3 has an integer root ( x = 3) so the encoding: $\langle$p ( x ) $\rangle$ = [2 , −9 , 8 , 3] is accepted by M3. 

But p ( x ) = 1 $x^{3}$ + 2 $x^{2}$ + 3 x + 4 does not have an integer root, so the encoding: $\langle$p ( x ) $\rangle$ = [1 , 2 , 3 , 4] is rejected by M3. 

## 8.9 decidable languages 

Languages that have deciders are called decidable languages. Here are some examples of decidable languages involving the acceptance problem for regular and context-free languages: 

- A DFA = {$\langle$B, w$\rangle$|B is a DFA that accepts input string w} 

- A NFA = {$\langle$B, w$\rangle$|B is a NFA that accepts input string w} 

- A RegEx = {$\langle$R, w$\rangle$|R is a Regular Expression that generates string w} 

- A PDA = {$\langle$B, w$\rangle$|B is a PDA that accepts input string w} 

- A CFG = {$\langle$G, w$\rangle$|G is a CFG that generates string w} 

## 8.10 undecidable languages and the halting problem 

Let A TM = {$\langle$M, w$\rangle$|M is a TM that accepts input string w} . 

We can construct a TM, U , that recognizes A TM: 

- U = On input $\langle$M, w$\rangle$ : 

   1. Simulate M on input string w . 

   2. If at any point M enters its accept state, then accept $\langle$M, w$\rangle$ . 

   3. If at any point M enters its reject state, then reject $\langle$M, w$\rangle$ . 

Note that U has no way of determining if M will not halt on input string w . In other words, M may continue indefinitely and not halt on input w . This is called the halting problem . 

Because no decider can be constructed for A TM we conclude that it’s an undecidable language. 