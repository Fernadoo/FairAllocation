# Allocating individible items

> A python implementation of all algorithms that allocate indivisible items.

### Usage:

```shell
$ python eval.py -h
usage: eval.py [-h]
               [--alg {roundRobin,envyGraph,MUtilW,MNW_opt,MNW_local,CSP1,CSPx}]
               [--num_agents NUM_AGENTS] [--num_items NUM_ITEMS] [--round RD]
               [--seed SEED]

Allocating indivisible items.

optional arguments:
  -h, --help            show this help message and exit
  --alg {roundRobin,envyGraph,MUtilW,MNW_opt,MNW_local,CSP1,CSPx}
                        Select the allocation algorithm
  --num_agents NUM_AGENTS
                        Specify the number of agents
  --num_items NUM_ITEMS
                        Specify the number of items
  --round RD            Specify the degree of rounding
  --seed SEED           Specify the seed
```



### Implementation so far:

|    Algorithm     |  Comp   | EF1  | PO   | EFx(any) | Allow_neg |                          Reference                           | Support |
| :--------------: | :-----: | :--: | ---- | :------: | :-------: | :----------------------------------------------------------: | :-----: |
|    roundRobin    |  Poly   |  Y   | N    |    N     |           |          https://dl.acm.org/doi/pdf/10.1145/3355902          |    Y    |
| doubleRoundRobin |         |      |      |          |     Y     |       https://www.ijcai.org/proceedings/2019/0008.pdf        |         |
|    envyGraph     |  Poly   |  Y   | N    |    N     |           |       https://dl.acm.org/doi/pdf/10.1145/988772.988792       |    Y    |
|   genEnvyGraph   |         |      |      |          |     Y     |       https://www.ijcai.org/proceedings/2019/0008.pdf        |         |
|      MUtilW      |  Poly   |  N   | Y    |    N     |           |                              /                               |    Y    |
|     MNW_opt      | NP-hard |  Y   | Y    |    N     |           |          https://dl.acm.org/doi/pdf/10.1145/3355902          |    Y    |
|    MNW_local     |   DK    |  DK  | DK   |    N     |           | http://www.lifl.fr/SMAC/publications/pdf/paams2009-realistic.pdf |    Y    |
|       CSP        | NP-hard |  Y   | Y    |    Y     |           |                                                              |         |



### As solving CSPs (*<u>new!</u>*)[*<u>onging...</u>*]:

#### Formulation:

* Varialbe: an item: [1, m]

* Value: to which agent the item is allocated: [1, n]

For naive DFS, # of possible solutions = m^n

#### Pruning:

* Rule 1: In any intermediate round, if such a situation exists, for a source agent, this agent (relaxed-ly) envies some other agent even if he gets all the rest goods, then the partial allocation is not feasible.

 

