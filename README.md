# wargames

Two soldiers shooting at each other, controlled by a neural network with a genetic algorithm.
They both learn how to fight during the training process. The AIs are learning by playing a lot of games, but never see a human player telling it how to kill the other AI.



### Inputs
The only informations an AI gets is the distance relative to its opponent, the corresponding angle and the number of updates since its last shot.

### Neural Network
This data is processed by a single hidden layer neural network with 1 bias per layer. The adjustement of this bias value by the algorithm leads to anticipation of the future position of the ennemy AI (overfitting?).

### Genetic Algorithm
At each generation, a tournament assigns the score of each AI.
The chance of an AI to reproduce and give birth to a mutated AI is proportional to the square of its score.

### Results
It works! In the first generations, the AIs barely move, and, generation after generation, they try differents moves: they approach or avoid the ennemy, try to scope ...

#### Screenshot :
![screenshot](https://i.imgur.com/86Tvkys.png)


### Dependencies
The game needs : 
- Python 3
- Numpy
- Pygame (Only for the -display part)

### Usage:
To train a new set of AIs, type : 

* python3 main.py -simulate 

To continue the training of other AIs, type : 

* python3 main.py -simulate <path to AIs>

The default output of the save command is located at saves/save_{save_number}/{generation} \

To visualize a tournament with all the AIs: 

 * python3 main.py -display <path to AIs>
