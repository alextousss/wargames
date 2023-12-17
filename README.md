# wargames

Two agents in a simulation where they shoot at each other, controled by a neural network with a genetic algorithm.
They both learn how to fight during the training process. The agents are learning by playing a lot of games, but never see a human player telling them how to win the game.



### Input
The agent outputs a command based on the distance relative to its opponent, the angle and the number of ticks since its last shot.

### Neural Network
This data is processed by a single hidden layer neural network with 1 bias per layer. The adjustement of this bias value by the algorithm leads to anticipation of the future position of the ennemy AI (overfitting?).

### Genetic Algorithm
At each generation, a tournament assigns a score for each agent.
The probability of an agent to reproduce and give birth to a mutated agent is proportional to the square of its score.

### Results
It works! In the first generations, the agents barely move, and, generation after generation, they try differents moves: they approach or avoid the ennemy, try to scope ...

#### Screenshot :
![screenshot](https://i.imgur.com/86Tvkys.png)


### Dependencies
The game needs : 
- Python 3
- Numpy
- Pygame (Only for the -display part)

### Usage:
To train a new set of agents, type : 

* python3 main.py -simulate 

To continue the training of other agents, type : 

* python3 main.py -simulate <path to agent>

The default output of the save command is located at saves/save_{save_number}/{generation} \

To visualize a tournament with all the agents: 

 * python3 main.py -display <path to agents>
