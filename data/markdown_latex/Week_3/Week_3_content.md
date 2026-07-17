>“The real question is not whether machines think but whether humans do.” 
>
>B.F. Skinner (Behaviorist and author) 

# 3 Regular Expressions 

The regular operations ( $\cup$, $\circ$, * ) can be used to build regular expressions that describe languages. 

## 3.1 examples of regular expressions 

Consider the regular expression ( a $\cup$ b ) $\circ$ a* . This regular expression describes the language, L1, of all strings that begin with a single a or a single b and are followed by any number of a ’s (including zero a ’s). It can be simplified using the shorthand: ( a $\cup$ b ) a* . Therefore: 

L1 = ( a $\cup$ b ) a* = { w | w begins with a or b and ends with any number of a’s } 

## 3.2 equivalence with finite automata 

Note that we can also describe the language L1 using the NFA N1 with a state diagram: 

[
    Figure: A state diagram of a finite automata (Q, $\Sigma$, $\delta$, $q_{0}$, F) described as follows:

    * Q = {$q_{1}$, $q_{2}$}
    * $\Sigma$ = {a, b}
    * $q_{0}$ = $q_{1}$
    * F = {$q_{2}$}

    with transition function $\delta$ described as follows:

    * δ($q_{1}$, a) = {$q_{2}$}
    * δ($q_{1}$, b) = {$q_{2}$}
    * δ($q_{2}$, a) = {$q_{2}$}
    * δ($q_{2}$, b) = $\emptyset$
]

Or formally by the 5-tuple N 1 = ( Q, $\Sigma$ , $\delta$, $q_{0}$ , F ) where: 

1. Q = {$q_{1}$ , $q_{2}$ } 

2. $\Sigma$ = {a, b} 

3. $\delta$ is given by: 
    * ($q_{1}$, a) -> $q_{2}$
    * ($q_{1}$, b) -> $q_{2}$
    * ($q_{1}$, $\varepsilon$) -> $\emptyset$
    * ($q_{2}$, a) -> $q_{2}$
    * ($q_{2}$, b) -> $\emptyset$
    * ($q_{2}$, $\varepsilon$) -> $\emptyset$

4. $q_{0}$ = $q_{1}$ 

5. F = $q_{2}$ 

We have that $L(N1)$ = ( a $\cup$ b ) a* . 

## 3.3 more shorthand 

If $\Sigma$ = { 0 , 1 } then the regular expressions $\Sigma$* and (0 $\cup$ 1)* both describe the same language; the language of all strings consisting of 0s and 1s. 

## 3.4 formal definition of a regular expression 

R is a regular expression if R is: 

1. a for some a $\in$ $\Sigma$ 

2. $\varepsilon$ (the language of a single empty string) 

3. $\emptyset$ (the language that does not contain any strings) 

4. R1 $\cup$ R2, where R1 and R2 are regular expressions 

5. R1 $\circ$ R2, where R1 and R2 are regular expressions 

6. R1*, where  R1 is a regular expression

## 3.5 the difference between $\varepsilon$ and $\emptyset$ 

Let R be a regular expression. 

If we add the language that does not contain any strings to R then R is not changed. Therefore: R $\cup$$\emptyset$ = R 

If we concatenate a single empty string to R then R is not changed. Therefore: R $\circ$ $\varepsilon$ = R 

For example: 0 $\cup$$\emptyset$ = 0, but 0 $\cup$ $\varepsilon$ = { 0 , $\varepsilon$}  ̸= 0 

For example: 0 $\circ$ $\varepsilon$ = 0, but 0 $\circ$$\emptyset$ = $\emptyset$̸ = 0 

## 3.6 order of precedence 

Just like arithmetic expressions (BEDMAS), there is an order of precedence for regular expressions: parentheses, then star, then concatenation, then union. 


## 3.7 The pumping lemma for regular languages 

If A is a regular language, then there is a number p (the pumping length) where if s is any string in A of length at least p , then s may be divided into three pieces, s = xyz , such that: 

1. for each $i \geq 0$ , x$y^{i}$ z $\in$ A 

2. $|y| > 0$ 

3. |xy| ≤ p 

PROOF: 

Let M = ( Q, $\Sigma$ , $\delta$, $q_{0}$ , F ) be a DFA with p states that recognizes A . 

Let s = s1s2...sn be a string in A of length n where n ≥ p . 

Let r = r1 , r2 , ..., rn, rn +1 be the sequence of states for s such that r{i +1} = $\delta$ ( ri, si ) for all 1 ≤ i ≤ n . This sequence has length n + 1 which is at least p + 1. 

Two of the first p+1 states in the sequence r must be the same by the pigeonhole principle because there are only p states in M. Let the first of these be rj and the other rl . Then l ≤ p + 1. 

Let x = s1 ...s{j− 1} Let y = sj...s{l− 1}. Let z = sl...sn 

We have that M must accept x$y^{i}$ z for $i \geq 0$ (condition 1. is true) We have that j = l , so $|y| > 0$ (condition 2. is true) We have that l ≤ p + 1, and $|xy| = l$ − 1. Therefore |xy| ≤ p (condition 3. is true) 

## 3.8 nonregular languages 

Let B = { $0^{n}$ $1^{n}$ |$n \geq 0$ } , the language of all strings of 0s then 1s with the same number of 0s and 1s. 

Assume, for the purpose of finding a contradiction, that B is regular. 

Let s = $0^{p}$ $1^{p}$ 

Then s $\in$ B and $|s| = 2p$ which is greater than p . 

The pumping lemma guarantees that x$y^{i}$ z $\in$ B for any $i \geq 0$. There are three cases for the string y which all lead to contradictions: 

- y consists of only 0s. Then xyyz has more 0s than 1s and therefore xy[2] z $\in$/ B 

- y consists of only 1s. Then xyyz has more 1s than 0s and therefore xy[2] z $\in$/ B 

- y consists of 1s and 0s. Then xyyz has a 0 after a 1 and therefore xy[2] z $\in$/ B 

Because the assumption that B is regular always leads to a contradiction, we conclude that B must be a nonregular language. 

Note that we can also use the third condition of the pumping lemma, |xy| ≤ p , to show that B is not regular: 

Assume, for the purpose of finding a contradiction, that B is regular. 

Let s = 0 [p] 1 [p] 

Then s $\in$ B and $|s| = 2$ p which is greater than p . 

[Figure: 
* The string $s$ is composed of $p$ zeros followed by $p$ ones (often written as $s = 0^p 1^p$).
* The string is partitioned into three consecutive substrings: $x$, $y$, and $z$ (such that $s = xyz$).
* The visual alignment indicates that the substrings $x$ and $y$ are located entirely within the first block of $p$ zeros.
* The substring $z$ aligns with the remainder of the string, which includes the block of $p$ ones.]

By the pumping lemma, xy[i] z $\in$ B for all $i \geq 0$. 

Because |xy| ≤ p , we have that y must only contain 0s. 

But then s cannot be pumped because xy[0] z has less than p 0s, and xy[2] z has more than p 0s. 

This contradicts the assumption that B is regular. 

Therefore B is not regular. 