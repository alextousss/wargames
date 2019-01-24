# wargames

Two soldiers shooting at each other, controlled by a neural network with a genetic algorithm.
What is quite interesting here, is that they both learn how to fight during the training process. The AIs are learning by playing a lot of games, but never sees a human player telling her how to kill the other AI.



### Inputs
The only informations the AI gets is the distance relative to the other one, the corresponding angle and the number of updates since both shooted.

### Neural Network
Then, thoses inputs are processed by a single hidden layer neural network with 1 bias per layer. The adjustement of this bias value by the algorithm leads to anticipation of the future position of the ennemy IA, this is over-learning but it is quite interesting

### Genetic Algorithm
The AI's are getting a personnal score, which is the number of kills they made on a tournament with all the other AI's
Their chance to reproduce and give birth to beautifull little mutated AI's is equel to ponderated score power a constant. Actually hard-coded at 2

### Results
It seems that this approach ... works ! On the first generations, the AI's barely moves, and, generation after generation, they start to try differents moves .. They approach or avoid the ennemy, are trying to scope ...

#### Screenshot :
![screenshot](https://i.imgur.com/86Tvkys.png)


### Dependencies
The game needs : 
- Python 3
- Numpy
- Pygame (Only for the -display part)

### Usage:
To train a new set of AI's, type : 

* python3 main.py -simulate 

To continue the training of other AI's, type : 

* python3 main.py -simulate <path to AI's>

The default output of the save command is located at saves/save_{save_number}/{generation} \

To watch what's doing a set of AI's, type : 

 * python3 main.py -display <path to AI's>
