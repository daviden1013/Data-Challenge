# Data-Challenge
My code and explanations on the challenge. 
The complete code is available in bingo.py

## Evaluation
We first develop the class "Game" based on the rules to evaluate the Bingo charts. For a given chart, when Game.play() is called, it returns the average number of dice rolls it takes a reach a Bingo out of n trials. For example:

```
chart = np.array(np.random.randint(1, 21, 9), dtype = float)
game = Game(chart)
game.play(1000)

>> 52.3, 15.3
```
this code generates a random chart and computes the average number of rolls (52.3) it takes to reach a Bingo out of 1000 trials. It also returns the standard deviation (15.3).
The less rolls it takes, the faster it gets a Bingo. So we want to find a chart that has the minimum score (loss).

## Find some candidate charts
Now we can find out some candidate charts and evaluation them.
A simple computation tells exhaustive method won't work. Trying ALL possible combinition will take (20^9)/4 = 128000000000 trials. There's no way we can brute force this! 
Then how about setting all 9 elements to the same value-- the most probable one to be chosen? According to the distribution of sum of two dice, 7 has the biggest probability 0.17. But considering the rule which multiples of a smaller number will also be chosen, we have 20 with probability 0.47. 
```
chart = np.repeat(20.0,9)
game = Game(chart)
game.play(1000)

>> 21.6, 12.6
```
The loss does improved from 52.3 to 21.6. But still, is this the optimal solution?
### Wide ranged search
We launch a simulation of 1000 to find the average loss. 
```
null_loss = []
for t in range(1000):
    print(t)
    chart = np.array(np.random.randint(1, 21, 9), dtype = float)
    game = Game(chart)
    null_loss.append(game.play(1000))
   
np.mean([i[0] for i in null_loss])
np.min([i[0] for i in null_loss])   

>> 50.8
>> 10.959
```
We found the average loss is 50.8 with the minimum loss 10.959. This tells that setting all values to the same is not the best approach.

### modified searching algorithm
Now we introduce a modified searching algorithm. It starts with a random given chart. We fix all other 8 elements and change only 1 at a time. Find the best value (minimize loss) then move on to the next element. This algorithm sacrificed some info of interaction of elements and does not guarantee to find the global minimum. But it finds a relative good result out of the random chart and is efficient enough to compute.

```
loss = []
charts = []
for t in range(1000):
    print(t)
    chart = np.array(np.random.randint(1, 21, 9), dtype = float)
    
    for i in range(9):
        min_chart = np.copy(chart)
        min = 100
        for j in range(1,21):
            chart[i] = j
            game = Game(chart)
            cur = game.play(100)[0]
            if cur < min:
                min_chart = np.copy(chart)
                min = cur
        
        chart = np.copy(min_chart)       
    
    charts.append(chart)
    game = Game(chart)
    loss.append(game.play(1000))

np.mean([i[0] for i in loss])
np.min([i[0] for i in loss])

>> 13.2
>> 8.4
```
The average loss is 13.2 with minimum 8.4. 
This means rolling 8 to 9 times can give a Bingo!
