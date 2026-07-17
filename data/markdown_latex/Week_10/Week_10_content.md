>“There are things machines will never do: 
>
>they cannot possess faith, they cannot appreciate beauty, they cannot create art. If they ever learn these things, they won’t have to destroy us, they’ll be us.” 
>
>Sarah Connor (Iconic Sci-Fi warrior) 

# 10 Reducibility 

## 10.1 mapping reducibility 

Language A is mapping reducible to language B if there is a computable function f : $\Sigma$^* -> $\Sigma$^* , where for every w $\in$ $\Sigma$^* , 

w $\in$ A <-> f ( w ) $\in$ B 

The function f is called the reduction from A to B . 

A function f : $\Sigma$^* −> $\Sigma$^* , is a computable function if some TM, on every input w , halts with just f ( w ) on its tape. 

We use the notation “ A ≤m B ” to state that language A is mapping reducible to language B . 

## 10.2 a simple A ≤ m B example 

Let A = { 1 , 10 , 11 } and B = { 101 , 111 , 1001 } with the function f : { 0 , 1 ^* -> { 0 , 1 ^* defined as: 

On input w : 

   1. Convert w from binary to a decimal number x and compute f ( x ) = 2 x + 3. 

   2. Convert f ( x ) from decimal to a binary number f ( w ) and return f (w ). 

f ( w ) is a reduction from A to B because for every binary string w $\in${ 0 , 1} ^*: 

w $\in$ A <-> f ( w ) $\in$ B 

Note that f ( w ) is computable because arithmetic operations on integers are computable. Therefore A ≤m B . 

## 10.3 decidability 

If we have that B = { 101 , 111 , 1001 } is decidable (and it is!), then A = { 1 , 10 , 11 } must also be decidable. The idea here is that if A reduces to a language that is less than or equal to the “computational difficulty” of B , then A’s “computational difficulty” must be contained within B’s “computational difficulty”. 

Construct a decider, N , for A : 

N = On input w : 

   1. Compute the reduction (in this case it’s just f ( w ) = 2 × w + 3 converted to binary). 

   2. Run M on f ( w ). 

   3. If M accepts f ( w ), then N accepts w . 

   4. If M rejects f ( w ), then N rejects w . 

We have that N is a decider for A . Therefore A is decidable. 

## 10.4 decidability using A ≤ m B 

If A ≤m B , and B is any decidable language, then A is decidable. 

The idea is that if B is decidable, and A reduces to a language that is less than or equal to the “computational difficulty” of B , then A must also be decidable. 

PROOF: 

Let M be the decider for B and f be the reduction from A to B . 

Construct a decider, N , for A : 

- N = On input w : 

   1. Compute the reduction f ( w ) (note that a reduction must exist because A ≤ m B ). 

   2. Run M on f ( w ). 

   3. If M accepts, then accept w . 

   4. If M rejects, then reject w . 

We have that N is a decider for A . Therefore A is decidable. 

## 10.5 undecidability using A ≤m B

We also have that if A ≤ m B and A is any undecidable language, then B is undecidable. 

The idea is that if A is undecidable, and A reduces to a language that is less than or equal to the “computational difficulty” of B , then B must also be undecidable. If B was decidable, then we could use the decider for B , along with the reduction from A to B , to decide A (which would be a contradiction because A is undecidable!) 

PROOF: Just show a reduction f from A to B such that for every w $\in$ $\Sigma$^* , 

w $\in$ A <-> f ( w ) $\in$ B 

## 10.6 a practical A ≤ m B example 

Let A = A_{TM}. 

We have proven previously that A_{TM} is undecidable. 

Let B = HALT_{TM}. 

Find a reduction from A to B to prove that HALT_{TM} is undecidable. 

Let F ( $\langle$M, w$\rangle$ ) be the following TM that computes a reduction from A = A_{TM} to B = HALT_{TM}: 

- F = On input $\langle$M, w$\rangle$ : 

   1. Construct a new TM, M' : 

      - M' = On input x : 

         1. Simulate M on x . 

         2. If M accepts, then accept (and halt) 

         3. If M rejects, then enter an infinite loop (and never halt). 

   2. Output $\langle$M' , w$\rangle$ 

We have that if M accepts w , then M' halts on w . We also have that if M' halts on w , then M must accept w (because M' cannot reject). 

- F computes a reduction from A = A_{TM} to B = HALT_{TM} such that for every $\langle$M, w$\rangle$ , 

$\langle$M, w$\rangle$$\in$ A <-> F ( $\langle$M, w$\rangle$ ) $\in$ B 

where: 

- F ( $\langle$M, w$\rangle$ ) = $\langle$M' , w$\rangle$ . 

- M' halts on input w if and only if M accepts w . 

We have shown that A_{TM} ≤m HALT_{TM}, and we have proven previously that A_{TM} is undecidable. 

Therefore, HALT_{TM} is undecidable. 