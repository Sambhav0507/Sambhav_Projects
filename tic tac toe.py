import numpy as np
import pickle

board_rows=3
board_columns=3

#this is the class for the state of the board
class State:
    def __init__(self,p1,p2):
        self.board=np.zeros((board_rows,board_columns))
        self.p1=p1
        self.p2 = p2
        #boolean flag that tells whether the game has ended or not
        self.isEnd = False
        self.boardHash= None
        #init p1 plays first
        self.playerSymbol = 1
    
    #get unique hash of a current board state
    def getHash(self):
        self.boardHash= str(self.board.reshape(board_rows * board_columns))
        return self.boardHash
    
    #define available positions
    
    def availablePositions(self):
        positions = []
        for i in range(board_rows):
            for j in range(board_columns):
                if self.board[i , j] == 0:
                    positions.append((i,j))
        return positions
        
    def updateState(self, position):
        self.board[position]=self.playerSymbol
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1
        
    def checkWinner(self):
        # row
        for i in range(board_rows):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1
        # col
        for i in range(board_columns):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
        # diagonal
        diag_sum1 = sum([self.board[i, i] for i in range(board_columns)])
        diag_sum2 = sum([self.board[i, board_columns - i - 1] for i in range(board_columns)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        # tie
        # no available positions
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # not end
        self.isEnd = False
        return None
   
    #feed reward to the winner
    
    def giveReward(self):
        result= self.checkWinner()
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        if result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)        
        if result == 1:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)
            
    # board reset
    def reset(self):
        self.board=np.zeros((board_rows,board_columns))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1
        
    #play the game between two computers(training)
    
    def play(self, rounds=1000):
        for i in range(rounds):
            if i%100 == 0:
                print("Round {}".format(i))
            
            while not self.isEnd:
                # player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(self.board ,positions, self.playerSymbol)
                #take action and update board state
                self.updateState(p1_action)
                board_hash= self.getHash()
                self.p1.addState(board_hash)
                
                #check board status if it is end
                
                win = self.checkWinner()
                if win is not None:
                    #self.showboard()
                    # ended with p1 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                    
                else:
                    #Player 2
                    positions= self.availablePositions()
                    p2_action= self.p2.chooseAction(self.board , positions, self.playerSymbol)
                    
                    #take action and update board and player state
                    
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)
                    
                    #check board status if ti is end
                    
                    win= self.checkWinner()
                    if win is not None:
                        #self.showboard()
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break
        #play with human
        
    def play2(self):
            while not self.isEnd:
                #player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(self.board , positions, self.playerSymbol)
                # update state of board and player
                self.updateState(p1_action)
                self.showBoard()
                #chech board status if it is end
                win = self.checkWinner()
                if win is not None:
                    if win == 1:
                        print(self.p1.name, "wins!")
                    else:
                        print("tie!")
                            
                    self.reset()
                    break
                else:
                    #Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions)
                    
                    #take action and update the board state
                    
                    self.updateState(p2_action)
                    self.showBoard()
                    
                    #check board staus if it is end
                    win = self.checkWinner()
                    if win is not None:
                        if win == -1:
                            print(self.p2.name, "wins!")
                        else:
                            print("tie!")
                        self.reset()
                        break
        
        #showing the board
        
    def showBoard(self):
            #player1 : x ,player 2 : o
            for i in range(board_rows):
                for j in range(board_columns):
                    if j!= board_columns - 1:
                        if self.board[i,j]== 1:
                            print("x",end=" ")
                        elif self.board[i,j]== -1:
                            print("o",end=" ")
                        else:
                            print(" ",end=" ")
                        print("|",end=" ")
                    else:
                        if self.board[i,j]== 1:
                            print("x")
                        elif self.board[i,j]== -1:
                            print("o")
                        else:
                            print(" ")

                if i!= board_rows-1:
                    print("---------")
class player:
    def __init__(self,name,exp_rate=0.3):
        self.name= name
        self.exp_rate = exp_rate #ϵ-greedy method to balance between exploration and exploitation. Here we set exp_rate=0.3 , which means ϵ=0.3 , 
        #so 70% of the time our agent will take greedy action, which is choosing action based on current 
        #estimation of states-value, and 30% of the time our agent will take random action.
        self.lr = 0.2 #learning rate
        self.states = [] #record all positions taken
        self.states_value = {} #state -> value
        self.decay_gamma= 0.9
        '''decay_gamma is a hyperparameter that controls the discount factor in the agent's learning process. 
        In reinforcement learning, the agent's goal is to maximize the cumulative reward it receives over time. 
        However, future rewards are typically worth less than immediate rewards, because there is more uncertainty 
        associated with them. Therefore, to account for this, the agent discounts future rewards by multiplying them
        by a factor between 0 and 1, called the discount factor.

        The decay_gamma parameter is a value between 0 and 1 that determines the degree of discounting. 
        A higher value of decay_gamma means that the agent places more emphasis on future rewards and less on 
        immediate rewards, while a lower value means the opposite. In general, a decay_gamma value close to 1 
        indicates that the agent is more far-sighted and willing to invest in long-term strategies, while a value
        closer to 0 indicates that the agent is more myopic and focused on short-term gains.'''
     
    
    def getHash(self, board):
        boardHash = str(board.reshape(board_columns * board_rows))
        return boardHash
    
    #choose action
    def chooseAction(self, current_board, positions, symbol):
        if np.random.uniform(0,1)<= self.exp_rate:
            # player will make a random choice
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            max_value= -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p]= symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                if value>=max_value:
                    max_value=value
                    action = p
        return action
    
    #append a hashed state
    def addState(self , state):
        self.states.append(state)
     
    #at the end of the game, backpropagate and update states value
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st]=0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]
            
    #reset states
    def reset(self):
        self.states = []
        
    #saving the policy
    def savePolicy(self):
       file_name = "policy_" + self.name
       with open(file_name, 'wb') as fw:
        pickle.dump(self.states_value, fw)
       fw.close()
        
    #loading the policy
    def loadPolicy(self, file):
       with open(file, 'rb') as f:
        data = pickle.load(f)
       f.close()


class humanPlayer:
    def __init__ (self , name):
        self.name = name
        
    #choose action
    def chooseAction(self , Positions):
        while True:
            row = int(input("Enter the row number: "))
            column = int(input("Enter the column number:"))
            action = (row,column)
            if action in Positions:
                return action
        
if  __name__ == "__main__":
    #training
    p1=player("p1")
    p2=player("p2")
    st=State(p1,p2)
    print("training...")
    st.play(50000)
    
    #play with human 
    
    p1=player("computer",exp_rate=0)
    
    p2=humanPlayer("Human")
    
    st=State(p1,p2)
    st.play2()   