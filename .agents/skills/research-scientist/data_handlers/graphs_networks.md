# Data Handler 6: Graphs, Complex Networks & Relational Systems

Format Scope: Edge lists (`.edgelist`, `.csv`), GraphML (`.graphml`), GEXF (`.gexf`), Pajek (`.net`).

---

## 1. Network Topology & Macro Properties

- **Degree Distribution**: Test power-law / scale-free fit vs. exponential or log-normal.
- **Small-Worldness**: Average shortest path length ($L$) and clustering coefficient ($C$) compared against Erdős–Rényi random graphs.
- **Community Detection**: Louvain modularity optimization, Leiden algorithm, Infomap.

---

## 2. Node-Level Centrality Metrics
- **Degree Centrality**: Immediate connectivity.
- **Betweenness Centrality**: Information brokerage and bottleneck identification.
- **Closeness / Harmonic Centrality**: Efficiency of reaching all other nodes.
- **Eigenvector / PageRank**: Influence derived from connections to other influential nodes.
- Tools: Python (`networkx`, `igraph`, `graph-tool`), R (`igraph`, `tidygraph`).
