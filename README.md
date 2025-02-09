# TP3

## Instructions

- Exercise 1 : Louvain
    - ✅ a function f(n, p, q) that generate a graph g where
        - $V = \bigsqcup_{1 \leq i \leq 4} V_i$ 
        - $\forall a, b \in V_i:$ $(a,b) \in E$ with proba $p$
        - $\forall a, b \in V_i, V_j$ s.t $i \neq j :$ $(a, b) \in E$ with proba $q$
    - ✅ a function to draw the graph
    - Use Louvain algorithm with $p/q$ ratio.
        - Which structures of community emerges ?
            - Use multiple tests
            - Use Images
            - Comment them
- Exercise 2 : Benchmarks
    - List explicitely 3 algorithms
    - Compare them
        - Execution time and space
        - Use different scales
        - Use different values of n,p,q
