# Homework - Large Network of Interactions

Work in progress, Deadline: 6th March

## Installation

TODO

## Execution

```bash
# demonstrations
make demo_distribution
make demo_generation
make demo_community_identification

# unit tests
make tests
make tests_verbose
```

## Instructions a

- Exercise 1 :
    - $\epsilon \in ]0, 1[$
    - 1:
        - Can we have Erdös-Reyni $G(n, p)$ or $G(n, M)$ such that $\Delta$ (max degree) $\in O(n^{1 - \epsilon})$ 
        - In this case, what are the clustering coefficients?
    - 2:
        - ✅ a function f(n, k, p, q) that generate a graph g where
            - $V = \bigsqcup_{1 \leq i \leq 4} V_i$ 
            - Each are sub graph $V_i$ is an Erdös-Rényi graph $G(n_i, p)$.
            - Edges between two different communities should have a probability $q$.
            - Eventually shuffle the nodes 
- Exercise 2 :
    - List explicitely 2 algorithms
        - ✅ Louvain
        - Other?
    - Compare them
        - Execution time and space
        - Use different scales
        - Use different values of n,p,q
        
## Instructions b (optional)

- Exercise 1 : Louvain
    - ✅ a function f(n, p, q) that generate a graph g where
        - $V = \bigsqcup_{1 \leq i \leq 4} V_i$ 
        - $\forall a, b \in V_i:$ $(a,b) \in E$ with proba $p$
        - $\forall a, b \in V_i, V_j$ s.t $i \neq j :$ $(a, b) \in E$ with proba $q$
    - ✅ a function to draw the graph
    - ✅ Use Louvain algorithm with $p/q$ ratio.
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
