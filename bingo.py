'''
Created on Oct 20, 2017

@author: david_000
'''

import numpy as np
np.random.seed(0)

u'''
  define class
'''
class Game:

    chart = None
    chart_back = None
    
    def __init__(self, c):
        self.chart = np.copy(c)
        self.chart_back = np.copy(c)
    
    def mark(self, v):
        mul = []
        for i in range(self.chart.shape[0]):
            if self.chart[i]%v == 0:
                mul.append(i)
        
        if len(mul) != 0:
            id = np.random.randint(0, len(mul), 1)
            self.chart[id] = 0.1 # mark as 0.1
        
    
    def isBingo(self):
        c = self.chart
        return c[0] == c[1] == c[2] == 0.1 or\
        c[3] == c[4] == c[5] == 0.1 or\
        c[6] == c[7] == c[8] == 0.1 or\
        c[0] == c[3] == c[6] == 0.1 or\
        c[1] == c[4] == c[7] == 0.1 or\
        c[2] == c[5] == c[8] == 0.1 or\
        c[0] == c[4] == c[8] == 0.1 or\
        c[2] == c[4] == c[6] == 0.1 
    
    '''
    This method returns the average number of dice rolls to reach a Bingo.
    The maximum rolls is 100 for each trial.
    '''
    def play(self, n):
        score = []
        for i in range(n):
            dice1 = np.random.randint(1, 7, 100)
            dice2 = np.random.randint(1, 7, 100)
            sum = dice1 + dice2
            count = 0
            while not self.isBingo():
                if count >= 100:
                    score.append(100)
                    break
                self.mark(sum[count])
                count += 1
            
            self.chart = np.copy(self.chart_back)
            score.append(count)
        
        return np.mean(score), np.sqrt(np.var(score))
    
u'''
  simulate
'''
   
# simulate form random
null_loss = []
for t in range(1000):
    print(t)
    chart = np.array(np.random.randint(1, 21, 9), dtype = float)
    game = Game(chart)
    null_loss.append(game.play(1000))
   
np.mean([i[0] for i in null_loss])
np.min([i[0] for i in null_loss])   

   
# simulate and optimize
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
loss
np.min([i[0] for i in loss])
id = np.argmin([i[0] for i in loss])


game = Game(charts[id])
game.play(10000)

