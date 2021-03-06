import numpy as np
import Queue
import hashTable
from copy import copy
from math import *

action = ["up","down","left","right"]        
        

class Tree():

    def __init__(self,env,agent,tableSize = 60):
        self.env = env
        self.agent = agent
        self.discount = agent.discount
        self.table = hashTable.Table(tableSize,self.hashFunc)
        self.root = None
    
    def reset(self):
        self.table.reset()
    
    def addNewRoot(self,state = None, done = None, root = None):
        self.table.reset()
        
        if type(root) == type(None):
            self.root = self.table.addNode(key = state,done = done,Qs = self.agent.Q,getIdx = self.agent.getIdx)
        
        else:
            self.root = root
        
        
        
    def changeRoot(self,state,done):
        self.root = self.table.newRoot(key = state,done = done,Qs = self.agent.Q,getIdx = self.agent.getIdx)
            
            
        
    def hashFunc(self,state,size):
        return (state[0]*state[1]) % size
        


    def play(self,s,done):
        discount = 1
        R = 0
        while discount > 0.01 and not done:
            a = self.agent.epsPickAction(s)
            s_,r,done = self.env.step(action[a])
            s_ = copy(s_)
            R += discount * r 
            discount *= self.discount
            s = s_
        if not done:
            idx = self.agent.getIdx(s)
            Q = np.amax(self.agent.Q[idx])
            Q *= discount
            return Q+R
        else:
            return R


        
    def MonteCarloTreeSearch(self,num_paths):
        while self.root.values[0]<num_paths:
            self.findBestWay()
        return self.root.getChoice(pFlag = 1,getAFlag = 1)
            
            
        
    def findBestWay(self):
        Que = Queue.Queue()
        self.env.setPosition(self.root.state)
        s,_,done = self.root.findBest(Que,self.env,self.discount)
        s = copy(s)
        ret = self.play(s,done)
        self.backPropagate(Que,ret)
            
    def backPropagate(self,Que,ret):
        num = 0
        while not Que.isEmpty():
            node = Que.pop()
            node.value.values[0] += 1
            node.value.values[1] += (self.discount**num) * ret
            num += 1
            
             
                                         
