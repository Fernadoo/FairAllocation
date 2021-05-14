# Allocating individible items

> A python implementation of all algorithms that allocate indivisible items.

### Usage:

```shell
$ python eval.py -h
usage: eval.py [-h] [--alg {roundRobin,envyGraph,MNW,CSP1,CSPx}]
               [--num_agents NUM_AGENTS] [--num_items NUM_ITEMS] [--round RD]

Allocating indivisible items.

optional arguments:
  -h, --help            show this help message and exit
  --alg {roundRobin,envyGraph,MNW,CSP1,CSPx}
                        Select the allocation algorithm
  --num_agents NUM_AGENTS
                        Specify the number of agents
  --num_items NUM_ITEMS
                        Specify the number of items
  --round RD            Specify the degree of rounding
```



### Implementation so far:

| Algorithm  | Complexity |                    Reference                     |   Support    |
| :--------: | :--------: | :----------------------------------------------: | :----------: |
| roundRobin | Polynomial |    https://dl.acm.org/doi/pdf/10.1145/3355902    |       Y      |
| envyGraph  | Polynomial | https://dl.acm.org/doi/pdf/10.1145/988772.988792 |              |
|    MNW     |  NP-hard   |    https://dl.acm.org/doi/pdf/10.1145/3355902    |              |
|    CSP     |  NP-hard   |                                                  |              |



### As solving CSPs (*<u>new!</u>*)[*<u>onging...</u>*]:

#### Formulation:

* Varialbe: an item: [1, m]

* Value: to which agent the item is allocated: [1, n]

For naive DFS, # of possible solutions = m^n

#### Pruning:

* Rule 1: In any intermediate round, if such a situation exists, for a source agent, this agent (relaxed-ly) envies some other agent even if he gets all the rest goods, then the partial allocation is not feasible.

 

