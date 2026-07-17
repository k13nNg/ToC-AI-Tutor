>“Once, humans turned their thinking over to machines in the hope that this would set them free. But that only permitted other humans with machines to enslave them.” 
>
>Frank Herbert (Dune) 

# 12 NP-completeness 

A language B is NP-complete if: 

1. B is in NP, and 

2. every other language A in NP can be reduced[*] to B . 

[∗] math details: Language A is polynomial time mapping reducible to language B , A ≤p B , if there is a polynomial time computable function f : $\Sigma$* -> $\Sigma$* , where for every w $\in$ $\Sigma$* , 

w $\in$ A <-> f ( w ) $\in$ B 


The function f is called the polynomial time reduction from A to B . 

## 12.1 showing that a language is NP-complete 

Suppose we want to show that some new and exiting language, C , is NP-complete. The conventional (easy) way of doing this is to carefully select another language, B , which has been previously proven to be NP-complete. The selection of B should be done in a way that makes it possible to reduce B to C (so that B ≤ C ). Then if C is in NP, it must be NP-complete because another NP-complete language, B , was reduced to it. 

The following is a short list of some languages that have been proven to be NP-complete: 

- SAT = {$\langle$ϕ$\rangle$|ϕ is a satisfiable Boolean formula } 

- VERTEX-COVER = {$\langle$G, k$\rangle$|G is an undirected graph with a k -node vertex cover } 

- HAMPATH = {$\langle$G, s, t$\rangle$|G is a directed graph that has a Hamiltonian path from s to t} 

- SUBSET-SUM = {$\langle$S, t$\rangle$|S = {x 1 , ..., xk} and the sum of some subset of S is t} 

Note that FACTOR is not NP-complete (as far as we know...). 

## 12.2 example of a specific problem reduction 

Consider the following two languages: 

VERTEX-COVER = {$\langle$G, k$\rangle$|G is an undirected graph with a k-node vertex cover } SET-COVER = {$\langle$U, S, k$\rangle$|S is a collection of subsets of U , and the union of k subsets in S equals U } 

A specific problem reduction can be shown with the following graph G = {V, E} : 

[

   Figure: 

   An undirected graph with the following adjacency list

   ad$j_{list}$ = {
    'a': ['b', 'd'],
    'b': ['a', 'c'],
    'c': ['b', 'd'],
    'd': ['a', 'c', 'e'],
    'e': ['d']
   }
]

A 2-node ( k = 2) vertex cover for G is {d, b} . 

Let the set U be the edge set, E , of the graph: U = { ( a, b ) , ( b, c ) , ( c, d ) , ( d, a ) , ( d, e ) } . 

For every v $\in$ V , let Sv contain all edges adjacent to v : 

* Sa = {(d, a), (a, b)}
* Sb = {(a, b), (b, c)}
* Sc = {(b, c), (c, d)}
* Sd = {(c, d), (d, e), (d, a)}
* Se = {(d, e)}

We then have that S is a collection of subsets of the edges in the graph, S = {Sa, Sb, Sc, Sd, Se} , such that the union of the 2 subsets {Sd, Sb} equals U . Then: 

A 2-node ( k = 2) vertex cover for G is {d, b} <-> the union of the 2 subsets {Sd, Sb} equals U . 

We have shown a specific problem reduction (only for this specific graph G ) from VERTEX-COVER to SET-COVER . 

## 12.3 example: show SET-COVER is NP-complete 

- SET-COVER is NP-complete if: 

   1. SET-COVER is in NP, and 

   2. every other language A in NP can be reduced to SET-COVER . 

First show that SET - COVER $\in$ NP. 

A polynomial time verifier for SET - COVER is: 

On input $\langle$U, S, k, c$\rangle$ : 

1. Check that the certificate, c , consists of exactly k subsets from S . If it does not, reject. 

2. Compute the union of all elements in c. If this equals U , accept. Otherwise, reject. 

If S contains m subsets, then part 1. requires at most m × k steps. Part 2. is done once. So this verifier involves at most mk steps which is polynomial, and therefore SET-COVER $\in$ NP. 

To show that every other language A in NP can be reduced to SET-COVER , we can reduce any known NP-complete problem to SET-COVER . 

In this case we will reduce V ERTEX - COV ER to SET-COVER . 

Let F ( $\langle$G, k$\rangle$ ) be the following TM that computes a reduction from VERTEX-COVER to SET-COVER : 

- F = On input $\langle$G, k$\rangle$ : 

   1. Let the set U be the edge set, E , of the graph G = {V, E} . 

   2. For every v $\in$ V , let Sv contain all edges adjacent to v , where Sv $\subseteq$ U . 

   3. Let S = {Sv1 , Sv2 , ..., Svn} , where n is the number of vertices in V . 

   4. Output $\langle$U, S, k$\rangle$ . 

A solution for SET-COVER of k subsets in S that equals U exists if and only if G has a k node vertex cover. In other words: 

- $\langle$G, k$\rangle$$\in$ VERTEX-COVER <->$\langle$U, S, k$\rangle$$\in$ SET-COVER 

We have shown that SET-COVER $\in$ NP, and that VERTEX-COVER ≤ SET-COVER , where VERTEX-COVER is a known NP-complete problem. 

Therefore SET-COVER is NP-complete. 