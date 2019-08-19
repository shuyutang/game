# PC204 final project, Shuyu Tang

"""
This program uses  MVC (model-view-controller) paradigm.
Model is the game board and rules, implemented in class CorneringGame.  
View is the canvas displayed in the user interface.
Controller is the event handler for mouse clicks in the canvas that place new checkers.
"""
def main():
    """Play cornering game."""

    # Initialize local variables
    size = 5
    side1 = "white"
    side2 = "black"

    ui = CorneringGameUI(CorneringGame(size), side1, side2)
    ui.run()        
    print "Finished"



class CorneringGame:
    """CorneringGame game board."""        # "model"

    def __init__(self, size):
        "Create initial board."
        self.size = size        
        self.player1 = 1
        self.player2 = 2
        self.reset()
            
    def reset(self):
        "Reset the board."
        #self.checkersX denote the position of playerX's checkers on each row

        import numpy as np
        self.checkers1 = np.zeros(self.size,dtype=np.int)
        self.checkers2 = np.zeros(self.size,dtype=np.int)
            
    def stdinit(self):
        "Initialize checkers in a standard way"
        import numpy as np
        for j in range(self.size):
            self.checkers1[j] = 0
            self.checkers2[j] = self.size-1
                    
    def randinit(self):
        "Initialize checkers in a random way"
        import random
        for j in range(self.size):
            pos = random.sample(range(self.size),2)
            #print pos
            self.checkers1[j] = pos[0]
            self.checkers2[j] = pos[1]
                    

    def play(self, i, j, player):
        "Add checker for player at (i, j) and see if game ends."
        if player == self.player1:
                self.checkers1[j] = i
        else:
                self.checkers2[j] = i

        return self._check_win(player)
    
    def _calwinlist(self):
        "calculate all win/lose scenarios for AI references"
        # a scenario is a list consisting of the distance between two checkers of each row
        
        import numpy as np
        import itertools
        import time
       
        self.winlist = set([])  #under these scenarios, first move would win
        self.loselist = set([]) #under these scenarios, first move would lose
        allcase = list(itertools.combinations_with_replacement(range(1,self.size), self.size)) #all possible scenarios listed in ascending order
        
        self.loselist.add(allcase[0]) #the first scenario is alway all ones array, apparently, first move would lose
        start = time.time() #check how long it takes to calculate the list
        
        for case in allcase[1:]:
            caseclassified = False
            """if a scenario with one element modified falls in loselist, then this scenario must belong to winlist, if it doesn't,
            since we check the scenarios in ascending order, meaning any move in this scenario would give opponent a win scenario,
            then this scenario must belong to loselist"""
                
            for i in range(self.size):
                temp = list(case)
                if case[i] > 1:
                    for j in range(1,case[i]):
                        temp[i] = j
                        if tuple(sorted(temp)) in self.loselist:
                            self.winlist.add(case)
                            caseclassified = True
                            break
                if caseclassified:
                        break                        

            else:
                    self.loselist.add(case)

        print "total time of calwinlist: %f s" % (time.time()-start)
        #print self.winlist
        #print self.loselist                              
                    

    def _check_win(self, player):
        "Check for winning run"
        # the victory needs to meet two conditions:
        # a) all the distances between two checkers in the same row should be 1
        # b) all opponents' checkers should be at the first or low column of the board
        if player == self.player1:
            checkercurr = self.checkers1
            checkernext = self.checkers2
        else:
            checkercurr = self.checkers2
            checkernext = self.checkers1
                
        for r in range(self.size):
            if not (checkernext[r] == 0 or checkernext[r] == self.size - 1):
                return False
            if abs(checkernext[r] - checkercurr[r]) > 1:
                return False
        else:
            return True


class CorneringGameUI:
    """CorneringGame game user interface (view and controller)."""

    def __init__(self, game, c1, c2):
        self.game = game
        self._fill = { 1:c1, 2:c2 }

        # Set up widgets for display ("view")
        import Tkinter
        self.app = Tkinter.Tk()
        self.app.title("Cornering Game")
        self.app.protocol("WM_DELETE_WINDOW", self._terminate) # ask before quit

        ## chess board frame
        self.canvas = Tkinter.Canvas(self.app, width=400,height=400, bg="gray")
        self.canvas.grid(row=0, column=0, rowspan = 1, sticky="nsew")

        # turn/win and warning
        self.msg = Tkinter.Label(self.app, text="Message line")
        self.msg.grid(row=1, column=0, columnspan = 1, sticky="ew")
        self.warnmsg = Tkinter.Label(self.app, text="")
        self.warnmsg.grid(row=2, column=0, columnspan = 1, sticky="ew")

        ## buttons frame
        self.f_buttons = Tkinter.Canvas(self.app, width = 80, bg="white")
        self.f_buttons.grid(row=0, column=1,rowspan = 1, sticky="nsew")

        ## new game
        self.l_newgame = Tkinter.Label(self.f_buttons, text="Start New Game", bg = "blue")
        self.l_newgame.grid(row=0, column=0, columnspan = 2, sticky="ew")
        self.b_sg = Tkinter.Button(self.f_buttons, text="New Game", command=self.startgame)
        self.b_sg.grid(row=1, column=1, columnspan = 1, sticky="ew")

        # size options
        self.l_boardsize = Tkinter.Label(self.f_buttons, text="Board Size")
        self.l_boardsize.grid(row=2, column=0, columnspan = 1, sticky="ew")                
        self.bsize = Tkinter.StringVar(self.f_buttons)
        self.bsizeopts = [str(e) for e in range(4,10)]
        self.bsize.set('5')
        self.bsizemenu = apply(Tkinter.OptionMenu, (self.f_buttons, self.bsize) + tuple(self.bsizeopts))
        self.bsizemenu.grid(row=2,column=1, sticky="ew")
        
        # initialization options
        self.l_initgame = Tkinter.Label(self.f_buttons, text="Initialization")
        self.l_initgame.grid(row=3, column=0, columnspan = 1, sticky="ew")                
        self.var = Tkinter.StringVar(self.f_buttons)
        self.var.set("standard")
        self.option = Tkinter.OptionMenu(self.f_buttons,self.var,"standard","random")
        self.option.grid(row=3,column=1,columnspan = 1,sticky="ew")

        # mode options: human or computer
        self.l_mode = Tkinter.Label(self.f_buttons, text="Mode")
        self.l_mode.grid(row=4, column=0, columnspan = 1, sticky="ew")
        self.mode = Tkinter.StringVar(self.f_buttons)
        self.modeopts = ["human vs human","human vs computer", "computer vs human"]
        self.mode.set(self.modeopts[0])
        self.modemenu = apply(Tkinter.OptionMenu, (self.f_buttons, self.mode) + tuple(self.modeopts))
        self.modemenu.grid(row=4,column=1, sticky="ew")

        ## display current game mode
        self.modemsg = Tkinter.Label(self.f_buttons, text="Current Game Mode", bg = "blue")
        self.modemsg.grid(row=5, column=0, columnspan = 2, sticky="ew")                
        self.modedisp = Tkinter.Label(self.f_buttons, text=self.mode.get())
        self.modedisp.grid(row=6, column=0, columnspan = 2, sticky="ew")
        self.colordisp = Tkinter.Label(self.f_buttons, text = '('+self._fill[1]+')   ('+self._fill[2]+')')
        self.colordisp.grid(row=7, column=0, columnspan = 2, sticky="ew")                

        ## save and load button
        self.b_save = Tkinter.Button(self.f_buttons, text="Save", command=self.savegame)
        self.b_save.grid(row=9, column=0, sticky="ew")
        self.b_load = Tkinter.Button(self.f_buttons, text="Load", command=self.loadgame)
        self.b_load.grid(row=10, column=0, sticky="ew")                 


        # make the canvas resizable
        self.app.rowconfigure(0, weight=1)
        self.app.columnconfigure(0, weight=1)
        self.canvas.bind("<Configure>", self._redraw)
        # cellSize is the size of each cell in pixels and is
        # updated by _redraw when we know the size of the canvas

        # record the size of canvas in pixels
        self.canvaswidth = self.canvas.winfo_reqwidth()
        self.canvasheight = self.canvas.winfo_reqheight()


        self._cell_size = 0
        self.currplayer = 1 # player1 always go first
        self.currmode = self.modeopts[0] #record the current mode
        self._nomove = (-1,-1)#(-1,-1) means no play yet
        self._last_played = self._nomove  
        self.handler = None #handler to bind mouse

        self.startgame() #automatically start game

    def run(self):
        "open the mainloop until quit"
        self.app.mainloop()

    def startgame(self):
        "start game"
        print "new game starts"
        # get board size from user selection
        self.game.size = int(self.bsize.get())
        self.game.reset()
        self.game._calwinlist()

        # reset player info
        self._last_played = self._nomove
        self.currplayer = 1                

        # initialize game according to user selection                
        if self.var.get() == "standard":
            self.game.stdinit()
        if self.var.get() == "random":
            self.game.randinit()

        # set mode according to user selection          
        self.currmode = self.mode.get()
        self.modedisp.config(text=self.currmode)
              
        # draw board and checkers       
        sizetemp = min(self.canvaswidth,self.canvasheight)                        
        self._redrawboard(sizetemp)                
        self._redrawchecker()
                        
        # check if initialization is already a dead game
        if self.game._check_win(self.toggle(self.currplayer)):
            self.message("%s wins" % self._fill[self.toggle(self.currplayer)])
            if self.handler != None:
                self.canvas.unbind("<Button-1>", self.handler)
                self.handler = None
        else:
            self.message("%s's turn" % self._fill[self.currplayer])
            self.warnmessage("")
            
            # Set up event handlers for view ("controller")
            self.handler = self.canvas.bind("<Button-1>", self._user_click)
            
            # if computer move first
            if self.currmode == self.modeopts[2]:
                self._AImove(self.currplayer)
                    
    def message(self, msg):
        "Display message in message line."
        self.msg.config(text=msg)
            
    def warnmessage(self, msg):
        "Display message in warning line."
        self.warnmsg.config(text=msg,fg = 'red')
            
    def ask(self, question):
        "Ask yes/no question and return True/False."
        from tkMessageBox import askyesno
        return askyesno("Cornering Game", question)
            

    def _play(self, player):
        "Let one player make a move."
                
        # Get selected location (guaranteed unoccupied/no jump over)
        # Display checker, then add to game
        i, j = self._last_played
        print self._fill[player],i,j

        
        if self.game.play(i, j, player):
            #if wins, redraw checkers, show messages, toggle players, unbind mouse
            self._redrawchecker()
            self.message("%s wins" % self._fill[player])
            self.currplayer = self.toggle(self.currplayer)                       
            self.canvas.unbind("<Button-1>", self.handler)
            self.handler = None
        else:
            #if not win, redraw checkers, show messages, toggle players                   
            self._redrawchecker()
            self.currplayer = self.toggle(self.currplayer)
            self.message("%s's turn" % self._fill[self.currplayer])                        


    def toggle(self,player):
        "toggle players"
        if player == 1:
            return 2
        else:
            return 1
                    
    def _redraw(self, event):
        "Redraw board and checker according to window size."
        size = min(event.width, event.height)
        self.canvaswidth = event.width # record current canvas size
        self.canvasheight = event.height
        self._redrawboard(size)
        self._redrawchecker()
            
    def _redrawboard(self,size):
        "Redraw board according to window size."
        # calculate cell size and edge offset
        cell_size = int(size / (self.game.size+1))
        if cell_size % 2 == 0:
            self._cell_size = cell_size - 1
        else:
            self._cell_size = cell_size
        offset = int(self._cell_size / 2)

        # Redraw the board
        low = offset
        high = self.game.size * self._cell_size + offset
        self.canvas.delete("board")
        for i in range(self.game.size+1):
            where = (i * self._cell_size) + offset
            self.canvas.create_line(where, low, where, high, tags="board")
            self.canvas.create_line(low, where, high, where, tags="board")
            
    def _redrawchecker(self):
        "Redraw checkers according to board"
        self.canvas.delete("checker")
        
        for j in range(self.game.size):
            i = self.game.checkers1[j]
            #print i,j
            self._checker(i, j, 1)
            i = self.game.checkers2[j]
            #print i,j
            self._checker(i, j, 2)

    def _checker(self, i, j, player):
        "Return bounding box for location (i, j)."
        
        #draw a red border for the last move                
        c = 'black'
        if self._last_played != self._nomove:
            tempi,tempj = self._last_played
            if tempi == i and tempj == j:
                c = 'red'
                        
        offset = int(self._cell_size / 2)
        llx = i * self._cell_size + offset
        urx = llx + self._cell_size
        lly = j * self._cell_size + offset
        ury = lly + self._cell_size
      
        return self.canvas.create_rectangle((llx, lly, urx, ury),
                                        tags="checker",
                                        fill=self._fill[player],outline = c)

    def _user_click(self, event):
        "Handle user mouse click in canvas."

        # Find click location indices
        offset = int(self._cell_size / 2)
        low = offset
        high = self.game.size * self._cell_size + offset
        if event.x < low or event.x > high or event.y < low or event.y > high:
                return                
        i = int((event.x - offset) / self._cell_size)
        j = int((event.y - offset) / self._cell_size)
        ij = (i, j)

        # Check if the index is valid
        self.warnmessage("")
        if self.game.checkers1[j] == i or self.game.checkers2[j] == i:
            # cell is already occupied
            self.warnmessage("Cell (%d, %d) occupied" % (i, j))
            return

        if self.currplayer == 1:
            if (self.game.checkers2[j] - i)*(self.game.checkers2[j] - self.game.checkers1[j]) < 0:
                self.warnmessage("Cannot jump over other player's checker")
                return
                
        if self.currplayer == 2:
            if (self.game.checkers1[j] - i)*(self.game.checkers1[j] - self.game.checkers2[j]) < 0:
                self.warnmessage("Cannot jump over other player's checker")
                return

        # if index is valid, set it as last move and make a move       
        self._last_played = ij
        print "human move"
        self._play(self.currplayer)

        # if human win, quit
        if not self.handler:    
            return          
            
        # if against computer, computermove
        if self.currmode != self.modeopts[0]:
            self._AImove(self.currplayer) 
            
    def savegame(self):
        "Save a game"

        from tkFileDialog import asksaveasfile
        name=asksaveasfile(mode='w',defaultextension=".txt")
        if name is not None:
            name.writelines(str(self.game.size)+'\n')
            name.writelines(str(self.currplayer)+'\n')
            name.writelines(self.currmode+'\n')
            for i in range(self.game.size):
                name.writelines(str(self.game.checkers1[i])+'\n')
            for i in range(self.game.size):
                name.writelines(str(self.game.checkers2[i])+'\n')
            i,j = self._last_played
            name.writelines(str(i)+'\n')
            name.writelines(str(j)+'\n')                                
            name.close
            print "game saved"
                    
    def loadgame(self):
        "Load a game"
        
        from tkFileDialog import askopenfile
        name = None
        
        try:
            name = askopenfile(mode = 'r', defaultextension=".txt")
        except IOError:
            self.warnmessage("Unrecognized file!")
                
        if name is not None:
            try:
                # check if loaded values are reasonable
                tempsize = int(name.readline())
                if tempsize < 4 or tempsize > 9:
                    raise ValueError
                
                tempcurrplayer = int(name.readline())
                if tempcurrplayer not in (1,2):
                    raise ValueError
                
                tempcurrmode = name.readline().rstrip()
                if tempcurrmode not in self.modeopts:
                    raise ValueError
                        
                                                                                                               
                import numpy as np
                tempcheckers1 = np.zeros(tempsize,dtype=np.int)
                tempcheckers2 = np.zeros(tempsize,dtype=np.int)
                
                for i in range(tempsize):
                    tempcheckers1[i] = int(name.readline())
                    if tempcheckers1[i] < 0 or tempcheckers1[i] > tempsize - 1:
                        raise ValueError
                        
                for i in range(tempsize):
                    tempcheckers2[i] = int(name.readline())
                    if tempcheckers2[i] < 0 or tempcheckers2[i] > tempsize - 1:
                        raise ValueError

                tempi = int(name.readline())
                tempj = int(name.readline())

                # check if last move is in saved checker positions
                flag = True
                if tempi == -1 and tempj == -1:
                    flag = False
                else:
                    if tempcurrplayer == 1:
                        for j in range(tempsize):
                            if j == tempj and tempcheckers2[j] == tempi:
                                flag = False
                                break
                    if tempcurrplayer == 2:
                        for j in range(tempsize):
                            if j == tempj and tempcheckers1[j] == tempi:
                                flag = False
                                break
                if flag:
                    raise ValueError
                                                   
            except ValueError:
                self.warnmessage("Failed to load values!")
                name.close
            else:
                # if no errors, assign temp values to game
                name.close
                self.game.size = tempsize
                self.game.reset()
                self.game._calwinlist()
                self.game.checkers1 = tempcheckers1
                self.game.checkers2 = tempcheckers2
                
                self._last_played = (tempi,tempj)
                self.currplayer = tempcurrplayer
                
                self.currmode = tempcurrmode
                self.modedisp.config(text=self.currmode)
                
                sizetemp = min(self.canvaswidth,self.canvasheight)
                self._redrawboard(sizetemp)
                self._redrawchecker()
                
                if self.game._check_win(self.toggle(self.currplayer)):
                    self.message("%s wins" % self._fill[self.toggle(self.currplayer)])
                    if self.handler != None:
                        self.canvas.unbind("<Button-1>", self.handler)
                        self.handler = None
                else:
                    self.message("%s's turn" % self._fill[self.currplayer])
                    self.warnmessage("")
                    self.handler = self.canvas.bind("<Button-1>", self._user_click)
                print "game loaded"
                              
    def _AImove(self, player):
        "AI move"
        self.canvas.unbind("<Button-1>", self.handler)
        self.handler = None
        
        import numpy as np
        import heapq
        import time
        import copy

        # calculate sorted distance between two checkers for each row
        self.currcase = tuple(sorted(np.absolute(np.subtract(self.game.checkers2,self.game.checkers1))))

        # if this distance vector is a win scenario
        if self.currcase in self.game.winlist:
#                       start = time.time()

            # calculate unsorted distance
            temp = np.absolute(np.subtract(self.game.checkers2,self.game.checkers1))

            # original index of distance elements if they are ranked in descending order
            midx = heapq.nlargest(self.game.size,range(len(temp)),temp.__getitem__)

            # from the largest to smallest, for each element, reduce its value and check if the modified distance vector is in loselist
            # if it is, such modification is the AI move
            foundAImove = False
            tempcopy = copy.copy(temp)
            for j in midx:
                for d in range(1,tempcopy[j]):
                    temp = copy.copy(tempcopy)
                    temp[j] = d
                    if tuple(sorted(temp)) in self.game.loselist:
                        # two possible positions with the same modified value,
                        # but only the one not on the other side of opponent checker is valid
                        if player == 1:
                            if d*(self.game.checkers1[j]- self.game.checkers2[j]) < 0:
                                i = self.game.checkers2[j]-d
                            else:
                                i = self.game.checkers2[j]+d
                        if player == 2:
                            if d*(self.game.checkers2[j]- self.game.checkers1[j]) < 0:
                                i = self.game.checkers1[j]-d
                            else:
                                i = self.game.checkers1[j]+d
  
                        self._last_played = (i,j)
                        foundAImove = True
                        break
                if foundAImove:
                        break
                                    
#                        print "total time of AIwinmove: %f s" % (time.time()-start)
            print "AI move"
        else:
            # id this distance vector is in the loselist, do a random move
            print "random move"
            self._randmove(player)
            
        self.handler = self.canvas.bind("<Button-1>", self._user_click)
        self._play(self.currplayer)
            
    def _randmove(self,player):
        "computer random move"
        for j in range(self.game.size):
            for i in range(self.game.size):
                if self.game.checkers1[j] == i or self.game.checkers2[j] == i:
                    continue
                if player == 1:
                    if (self.game.checkers2[j] - i)*(self.game.checkers2[j] - self.game.checkers1[j]) < 0:
                        continue
                if player == 2:
                    if (self.game.checkers1[j] - i)*(self.game.checkers1[j] - self.game.checkers2[j]) < 0:
                        continue
                self._last_played = (i,j)
            
            
            
    def _terminate(self):
        "Check if user wants to end game."
        if self.ask("Really quit?"):
            self.app.destroy()

if __name__ == "__main__":
        main()
