>“I’ve never been a good estimator of how long things are going to take.” 
>
>Donald Knuth (Programming Guru) 

# 11 Time Complexity 

## 11.1 big-O notation 

Let f, g be functions from the set of non-negative integers to non-negative real numbers. We have that f ( n ) = O ( g ( n )) if integers c and n 0 exist such that for every n ≥ n 0: 

f(x) ≤ c g(n)

## 11.2 polynomial example 

If f1(n) = 2$n^{4}$ + 3$n^{2}$ + 1, show that f1(n) = O($n^{4}$).

Let $n_{0}$ = 2. Then find c $\in$ Z such that for every n ≥ n 0: 

[# Asymptotic Bounds: Solving for Constant $c$ in Big-O Notation

Concept Overview: This mathematical sequence demonstrates how to find the constant multiplier $c$ required to prove that a specific function $f_1(n)$ is bounded above by $c \cdot g(n)$. By substituting the functions with $f_1(n) = 2n^4 + 3n^2 + 1$ and $g(n) = n^4$, and setting a specific value for $n$ (in this case, $n = 2$), the equations algebraically solve for the minimum valid value of $c$.

Mathematical Steps:
$$
\begin{align*}
$f_{1}$(n) &\leq c \cdot g(n) \\
2$n^{4}$ + 3$n^{2}$ + 1 &\leq c \cdot $n^{4}$ \\
2(2)^4 + 3(2)^2 + 1 &\leq c \cdot (2)^4 \\
45 &\leq c \cdot 16 \\
\frac{45}{16} &\leq c \\
2.8125 &\leq c
\end{align*}
$$

Step-by-Step Breakdown:
* General Definition: States the core inequality for an asymptotic upper bound.
* Function Substitution: Replaces $f_1(n)$ and $g(n)$ with their polynomial forms.
* Value Substitution ($n=2$): Plugs in $2$ for $n$ to evaluate the expressions.
* Simplification: Calculates the left side to be $45$ and the right side multiplier to be $16$.
* Isolation of $c$: Divides both sides by $16$ to isolate $c$.
* Final Evaluation: Concludes that for $n=2$, the constant $c$ must be greater than or equal to $2.8125$.]

With c = 3 and n 0 = 2 we have that 2 $n^{4}$ + 3 $n^{2}$ + 1 ≤ c $n^{4}$ for every n ≥ n 0. Therefore f 1( n ) = O ( $n^{4}$ ). 

Alternatively, we could note that when $n \geq 1$: $n^{2}$ ≤ $n^{4}$ , and 1 ≤ $n^{4}$ . Then: 

[# Asymptotic Bounds: Deriving Constant $c$ via Term Replacement (Big-O)

Concept Overview: This mathematical sequence demonstrates a common algebraic technique used in algorithm analysis to prove an asymptotic upper bound (Big-O). Instead of calculating a tight constant for a specific $n$, this method replaces all lower-order terms with the dominant term to easily find a valid constant multiplier $c$ that works for all $n \geq 1$.

Mathematical Steps:
$$
\begin{align*}
2$n^{4}$ + 3$n^{2}$ + 1 &\leq 2$n^{4}$ + 3$n^{4}$ + $n^{4}$ \\
&= 6$n^{4}$
\end{align*}
$$

Step-by-Step Breakdown:
* Original Function: The sequence begins with the polynomial function $f(n) = 2n^4 + 3n^2 + 1$.
* Term Replacement (The Inequality): Assuming $n \geq 1$, it is mathematically guaranteed that $n^2 \leq n^4$ and $1 \leq n^4$. By replacing the $n^2$ and the constant $1$ with the highest-degree term ($n^4$), the right side of the inequality is guaranteed to be greater than or equal to the left side.
* Simplification: Factoring and adding the coefficients together ($2 + 3 + 1$) yields $6n^4$.
* Theoretical Conclusion for RAG: This concise proof demonstrates that $2n^4 + 3n^2 + 1 \in O(n^4)$. It successfully isolates a witness constant of $c = 6$ for $n_0 = 1$.]

With c = 6 and n 0 = 1 we have that 2 $n^{4}$ + 3 $n^{2}$ + 1 ≤ c $n^{4}$ for every n ≥ n 0. Therefore f 1( n ) = O ( $n^{4}$ ). 

## 11.3 logarithm example 

If f 2( n ) = log2( n ) + 8, show that f 2( n ) = O (log n ). 

Let n 0 = 10. Then find c $\in$ Z such that for every n ≥ n 0: 

[
# Asymptotic Bounds: Solving for Constant $c$ with Logarithms (Big-O)

Concept Overview: This mathematical sequence demonstrates how to find the constant multiplier $c$ required to prove an asymptotic upper bound for logarithmic functions. Specifically, it tests the condition where $f_2(n) = \log_2(n) + 8$ and $g(n) = \log(n)$. By substituting a specific value ($n = 10$) and leveraging the property that the common logarithm $\log_{10}(10) = 1$, the equations algebraically solve for the minimum valid value of $c$.

Mathematical Steps:
$$
\begin{align*}
$f_{2}$(n) &\leq c \cdot g(n) \\
\lo$g_{2}$(n) + 8 &\leq c \cdot \log(n) \\
\lo$g_{2}$(10) + 8 &\leq c \cdot \log(10) \\
\lo$g_{2}$(10) + 8 &\leq c \cdot 1 \\
\lo$g_{2}$(10) + 8 &\leq c \\
3.32\dots + 8 &\leq c \\
11.32\dots &\leq c
\end{align*}
$$

Step-by-Step Breakdown:
* General Definition: States the core inequality for an asymptotic upper bound ($O(g(n))$).
* Function Substitution: Replaces $f_2(n)$ and $g(n)$ with their specific logarithmic expressions. The right side uses $\log(n)$, which implies a base of 10 given the later simplification.
* Value Substitution ($n=10$): Plugs in $10$ for $n$ to evaluate the expressions at a specific threshold.
* Logarithmic Simplification: Evaluates $\log(10)$ to $1$, which neatly isolates $c$ on the right side of the inequality.
* Numerical Approximation: Evaluates $\log_2(10)$ to its approximate decimal value, $3.32\dots$
* Final Evaluation: Concludes that for $n=10$, the witness constant $c$ must be greater than or equal to approximately $11.32$.

]

With c = 12 and n0 = 10 we have that log2( n ) + 8 ≤ c log n for every n ≥ n0. Therefore f 2( n ) = O (log n ). 

We could also let n0 = 2. Then: 

[

   # Asymptotic Bounds: Solving for Constant $c$ with Logarithms (Base Case $n=2$)

Concept Overview: This mathematical sequence demonstrates finding the constant multiplier $c$ required to prove an asymptotic upper bound (Big-O) for a logarithmic function. It tests the condition where $f_2(n) = \log_2(n) + 8$ and $g(n) = \log(n)$ (implying base 10). By substituting a lower threshold value of $n = 2$, the equations algebraically solve for the minimum valid value of $c$. 

Mathematical Steps:
$$
\begin{align*}
$f_{2}$(n) &\leq c \cdot g(n) \\
\lo$g_{2}$(n) + 8 &\leq c \cdot \log(n) \\
\lo$g_{2}$(2) + 8 &\leq c \cdot \log(2) \\
1 + 8 &\leq c \cdot \log(2) \\
\frac{9}{\log(2)} &\leq c \\
29.89\dots &\leq c
\end{align*}
$$

Step-by-Step Breakdown:
* General Definition: States the core inequality for establishing an asymptotic upper bound.
* Function Substitution: Replaces $f_2(n)$ and $g(n)$ with their specific logarithmic expressions.
* Value Substitution ($n=2$): Plugs in $2$ for $n$ to evaluate the expressions at a small threshold.
* Logarithmic Simplification: Uses the identity $\log_2(2) = 1$ to simplify the left side of the inequality to $9$.
* Isolation of $c$: Divides both sides by the common logarithm $\log(2)$ to isolate $c$.
* Numerical Approximation: Evaluates $9 / \log_{10}(2)$ to its approximate decimal value. It concludes that if you choose $n_0 = 2$, the witness constant $c$ must be greater than or equal to approximately $29.89$.
]

With c = 30 and n 0 = 2 we have that log2( n ) + 8 ≤ c log n for every n ≥ n 0. Therefore f 2( n ) = O (log n ). 

joshua.schneider@sheridancollege.ca 

page2 

INFO47546 

Theory of Computation 

Week11 

##  11.4 Time complexity of algorithms 

Consider an algorithm that reads an input string w of length n bits. The time complexity, f ( n ), of the algorithm is the maximum number of steps that the algorithm will use on any input w of length n . We typically use big-O notation to estimate f ( n ). Consider the following algorithm, A 1, that determines if a binary string is in the language { $0^{k}$ $1^{k}$ |$k \geq 0$ } : 

[

   # Python Implementation: Algorithm Decider for the Formal Language $L = \{0^n 1^n \mid n \ge 0\}$

Concept Overview: This code provides a high-level implementation (mimicking a Turing Machine's "tape" operations) of a decider, A1, for the classic formal language $L = \{0^n 1^n \mid n \ge 0\}$. It verifies whether an input string consists of a block of 0s followed by an exactly equal-sized block of 1s by scanning and progressively "crossing off" matching symbols.

Algorithm Components (Turing Machine Simulation):
* Format Validation (Step 1): Iterates through the string to ensure that a 0 never sequentially follows a 1. If it finds the sequence 10, the string violates the structural pattern of the language and is immediately rejected.
* Symbol Crossing/Pairing (Step 2): Simulates the back-and-forth movement of a TM head. As long as both a 0 and a 1 remain in the string, it replaces the first occurrence of 0 with an x, and the first occurrence of 1 with an x.
* Final Parity Check (Step 3): Once the pairing loop finishes (meaning either 0s or 1s have run out), the machine checks if any unmatched symbols remain. If stray 0s or 1s exist, the quantities were unequal, and the string is rejected. If the string is entirely xs, it is accepted.

Source Code:
python
def A1(w):

    #1. Scan for 0s after 1s
    for i in range(len(w)-1):
        if w[i]=='1' and w[i+1]=='0':
            return('reject')

    #2. Replace pairs of 0s and 1s with xs
    while '0' in w and '1' in w:
        w=w.replace('0','x',1)
        w=w.replace('1','x',1)
        print(w)

    #3.Check if any 0s or 1s remain
    if '0' in w or '1' in w:
        return('reject')
    
    return('accept')
]

Let $|w| = n$ . Then: 

1. requires n − 1 steps. 

2. requires n 2[steps to find the left most 1 (assuming the scan starts on the left), and must repeat] this n/2 to eliminate all pairs of 0s and 1s (assuming that w is in the language).

3. requires n steps to scan all the remaining elements in the string. 

The total number of steps taken by A1 is given by f ( n ) where: 

[

   # Algorithm Time Complexity: Simplifying an Operation Count Function

Concept Overview: This mathematical sequence demonstrates the formulation and simplification of an exact operation count function, $f(n)$, often used when analyzing the time complexity of an algorithm. The function sums the discrete operations from different phases of an algorithm (e.g., sequential loops and nested loops) to derive a single polynomial representing the total execution time.

Mathematical Steps:
$$
\begin{align*}
f(n) &= (n - 1) + \left(\frac{n}{2} \times \frac{n}{2}\right) + (n) \\
&= \frac{$n^{2}$}{4} + 2n - 1
\end{align*}
$$

Step-by-Step Breakdown:
* Original Function Construction: The top equation sums three distinct components of a hypothetical algorithm:
    * $(n - 1)$: Likely a linear operation, such as a simple `for` loop running $n-1$ times.
    * $\left(\frac{n}{2} \times \frac{n}{2}\right)$: Represents a quadratic operation, likely nested loops that each iterate over half the input size.
    * $(n)$: Another linear operation, such as a final pass over the input array.
* Algebraic Simplification: * The fraction multiplication resolves to the quadratic term: $\frac{n^2}{4}$.
    * The linear terms are combined: $(n - 1) + n = 2n - 1$.
    * Grouping them together yields the simplified polynomial: $\frac{n^2}{4} + 2n - 1$.
* Theoretical Conclusion for RAG: By expressing the exact step count as a simplified polynomial, it becomes mathematically trivial to determine the Big-O asymptotic bound. Because the highest-order term is $\frac{n^2}{4}$, this specific algorithm has a worst-case time complexity of $O(n^2)$.
]

Let n0 = 1. Then find c $\in$ Z such that for every n ≥ n0: 

[

   # Asymptotic Bounds: Solving for Constant $c$ for a Quadratic Function (Big-O)

Concept Overview: Building upon the previous derivation of an algorithm's exact operation count, this sequence demonstrates how to find the constant multiplier $c$ required to prove its asymptotic upper bound. It tests the condition where the exact function $f(n) = \frac{n^2}{4} + 2n - 1$ is bounded by $g(n) = n^2$. By substituting the base case $n = 1$, the equations algebraically solve for the minimum valid value of the witness constant $c$.

Mathematical Steps:
$$
\begin{align*}
f(n) &\leq c \cdot g(n) \\
\frac{$n^{2}$}{4} + 2n - 1 &\leq c \cdot $n^{2}$ \\
\frac{$1^{2}$}{4} + 2 - 1 &\leq c \cdot $1^{2}$ \\
\frac{1}{4} + 1 &\leq c \cdot 1 \\
1.25 &\leq c
\end{align*}
$$

Step-by-Step Breakdown:
* General Definition: States the foundational inequality for proving Big-O notation.
* Function Substitution: Replaces $f(n)$ with the previously derived polynomial and $g(n)$ with the dominant quadratic term $n^2$.
* Value Substitution ($n=1$): Plugs in $1$ for $n$ to evaluate the expression at the lowest possible integer bound ($n_0 = 1$). Note that the term $2n$ simply becomes $2$.
* Simplification: Calculates the left side ($\frac{1}{4} + 1$) and the right side ($c \cdot 1$).
* Final Evaluation: Concludes that for $n_0=1$, the witness constant $c$ must be greater than or equal to $1.25$. This formally proves that $\frac{n^2}{4} + 2n - 1 \in O(n^2)$.
]
With c = 2 and n0 = 1 we have that 

$n^{2}$/4 + 2n - 1 ≤c$n^{2}$

for every n ≥n0

Therefore f ( n ) = O ( $n^{2}$), and  1 has time complexity O ( $n^{2}$ ). 

## 11.5 Time complexity classes 

We have that { $0^{k}$ $1^{k}$ |$k \geq 0$ } $\in$ TIME( $n^{2}$ ) because it can be decided by an algorithm with time complexity O ( $n^{2}$ ). 

The time complexity class TIME( $n^{2}$ ) includes the language { $0^{k}$ $1^{k}$ |$k \geq 0$ } and any other languages that can be decided by an algorithm with time complexity O ( $n^{2}$ ). 

Note that we can do much better (see the exercises) in terms of time complexity for the language { $0^{k}$ $1^{k}$ |$k \geq 0$ } ! 

## 11.6 Time complexity classes P and NP 

Let TIME( t ( n )) = {L|L is a language decided in O ( t ( n )) time } 

## 11.7 the class P 

P is the class of languages that are decidable in polynomial time: 

$$P = \bigcup_k TIME(n^k)$$

Some examples of languages that are decidable in polynomial time are: 

- { $0^{k}$ $1^{k}$ |$k \geq 0$ } 

- {$\langle$f ( x ) $\rangle$|f ( x ) is a linear function with an integer root } 

- {$\langle$G$\rangle$|G is a connected undirected graph } 

- PATH = {$\langle$G, s, t$\rangle$|G is a directed graph that has a path from vertex s to vertex t} 

## 11.8 the class NP 

NP is the class of languages that have polynomial time verifiers. 

A verifier for a language L is an algorithm V , where: 

L = {w|V accepts $\langle$w, c$\rangle$ for some string c}

c is the certificate (or proof) that w $\in$ L . 

Some examples of languages that have polynomial time verifiers are: 

   - FACTOR = {N |N = pq , for integers p, q > 1 } 

   - HAMPATH = {$\langle$G, s, t$\rangle$|G is a directed graph that has a Hamiltonian path from vertex s to vertex t} 

Note: A Hamiltonian path is a path that goes through every vertex in the graph exactly once. 

It can be shown (see Week 12 Exercises...) that a language is a member of NP iff it is decided by a nondeterministic algorithm in polynomial time. 

Let NTIME( t ( n )) = {L|L is a language decided by a nondeterministic algorithm in O ( t ( n )) time } 

$$NP = \bigcup_k NTIME(n^k)$$

## 11.9 P=NP? 

P languages can be decided in polynomial time. 

For example: Given any directed graph, you can check if it has a path between any two vertices in polynomial time. 

So we can directly test if $\langle$G, s, t$\rangle$$\in$ PATH relatively quickly. 

NP languages can be verified in polynomial time. 

For example: Given any directed graph, you can check that a specific path certificate c is a Hamiltonian path in polynomial time using the verifier. 

So we can test if $\langle$$\langle$G, s, t$\rangle$, c$\rangle$ is accepted by the verifier for HAMPATH relatively quickly, and then use this result to establish that $\langle$G, s, t$\rangle$$\in$ HAMPATH . 

But directly testing if $\langle$G, s, t$\rangle$$\in$ HAMPATH relatively quickly without a path certificate c is not possible (as far as we know...). 

In general if L $\in$ NP, it (by definition) has a polynomial time verifier, but we cannot assume that L is also $\in$ P. To establish that L $\in$ P, a polynomial time algorithm that decides the language must be found. 

## 11.10 PATH vs. HAMPATH 

The languages PATH and HAMPATH are similar problems in that they both involve finding paths in a directed graph. They both have exponential time deciders (brute force search algorithms) that are $\in$ EXPTIME where: 

$$EXPTIME = \bigcup_k TIME(2^{n^k})$$

We can show that despite these similarities, algorithms exist that solve PATH in polynomial time... but no such algorithms are know to exist that solve HAMPATH in polynomial time. 

## 11.11 Proof that PATH $\in$ P 

PATH = {$\langle$G, s, t$\rangle$|G is a directed graph that has a path from vertex s to vertex t} 

Let the graph G have m vertices given by: v 1 , v 2 , ..., v{m− 1} , vm . 

In order to prove that PATH $\in$ P, we describe a polynomial time algorithm to solve PATH : 

On input $\langle$G, s, t$\rangle$ : 

1. Mark vertex s . 

2. Repeat until no new vertices are marked: Scan all edges in G . If an edge ( va, vb ) is found where va is marked and vb is not marked, mark vb . 

3. If t is marked accept. Otherwise reject. 

If we let e be the number of edges in G we have part 2. must scan through e edges at most m times. So MPATH uses at most 1+ m × e +1 = 2+ m × e steps which is polynomial, and therefore PATH $\in$ P. 