"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Megan Jung(mj374) and Isabella Wu (iw58)
# 12/12/2019
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute: _direction: whether the Aliens have moved left or right last
    # Invariant: _direction is a boolean

    # Attribute: _key: determines whether or not the player can press the up
    # arrow
    # Invariant: _key is a boolean
    #
    # Attribute: _alienStep: The number of steps the alien wave has taken
    # in between each alien bolt fired
    # Invariant: _alienStep is an int > 0
    #
    # Attribute _gameOver: the state of the wave
    # Invariant: _gameOver is bool(True means Win)
    #
    # Attribute _lastkeys: the number of keys pressed last frame
    # Invariant: _lastkeys is an int>= 0
    #
    # Attribute: _nextBolt: The time of the next laser bolt shot from the alien
    # Invariant: _nextBolt is a random int between 1 and BOLT_RATE
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Returns the ship object or None if ship is shot
        """
        "return self._ship"
        if self._ship == None:
            return True
        return False

    def setNewShip(self):
        """
        Sets the ship attribute as a ship object
        """
        self._ship = Ship()

    def getVelocity(self):
        """
        Returns BOLT_SPEED
        """
        return BOLT_SPEED

    def getAlien(self):
        """
        """
        return self._aliens

    def getLives(self):
        """
        Returns the number of lives left.
        """
        return self._lives

    def setLives(self,life):
        """
        Sets self._lives to the parameter life.
        """
        self._lives = life

    def getLengthAlien(self):
        """
        Returns the length of the self._aliens list.
        """
        return len(self._aliens)

    def getGame(self):
        """Returns: True if the player won the game"""
        return self._gameOver

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the game.
        """
        assert type(ALIEN_ROWS) == int and type(ALIENS_IN_ROW) == int
        self._createAlien()
        self._createShip()
        self._defLine()
        self._gameOver = None
        self._time = 0
        self._lastkeys = 0
        self._direction = False
        self._bolts = []
        self._key = False
        self._alienStep = 0
        self._lives = SHIP_LIVES
        self._nextBolt = random.randint(1,BOLT_RATE)

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Animates a single frame in STATE_ACTIVE.

        Parameter input: The user's input to fire a bolt and move the ship
        Precondition: Either the up, left, or right arrows

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._animateShip(input,dt)
        self._createPlayerBolt(input,dt)
        self._time += dt
        if self._time >= ALIEN_SPEED:
            self._animateRightAlien()
        #if self._time >= ALIEN_SPEED:
            self._animateLeftAlien()

        if (len(self._bolts) > 0):
            for w in range(len(self._bolts)):
                self._bolts[w].y += self._bolts[w].getVelocity()
        self._removeBolt()

        if self._isPlayerBolt() == False:
            if self._alienStep >= self._nextBolt:
                newBolt = self._alienBolt()
                if newBolt:
                    self._alienStep = 0
                    self._nextBolt = random.randint(1,BOLT_RATE)
        self._shipCollide()
        self._alienCollide()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws objects in the STATE_ACTIVE of the game.

        Attribute view: the game view, used in drawing
        Invariant: view is an instance of GView (inherited from GameApp)
        """
        for r in self._aliens:
            for alien in r:
                if alien != None:
                    alien.draw(view)
        if self._ship != None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)

    def _minY(self):
        """
        Returns the minimum y cooridinate of the lowest existing alien in the
        wave.
        """
        pos = GAME_HEIGHT
        for n in range(self.getLengthAlien()):
            for x in range(len(self._aliens[0])):
                if self._aliens[n][x] != None and self._aliens[n][x].y<pos:
                    pos = self._aliens[n][x].y
        return pos

    def _minAlien(self):
        """
        Returns the minimum x cooridinate of an existing alien in the alien
        wave.
        """
        minA = 999999
        for r in self._aliens:
            for y in r:
                if(y != None):
                    minA = min(minA,y.x)
        return minA

    def _drawBolts(self,view):
        """
        Draws both the player and alien bolts.

        Attribute view: the game view, used in drawing
        Invariant: view is an instance of GView (inherited from GameApp)
        """
        if len(self._bolts)>0:
            for n in self._bolts:
                    n.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def _createAlien(self):
        """
        Creates the alien wave.
        """
        alien = ALIENS_IN_ROW
        rows = ALIEN_ROWS
        image = ALIEN_IMAGES
        x = ALIEN_H_SEP + ALIEN_WIDTH
        y = GAME_HEIGHT-ALIEN_CEILING - ((rows - 2)*(ALIEN_HEIGHT))+\
            -((rows-1)*(ALIEN_V_SEP))
        self._aliens = []
        if rows > 6:
            image = ALIEN_IMAGES*(rows//3)
        for i in image:
            rowc = 2
            while rowc > 0 and rows > 0:
                ARow=[]
                while alien > 0:
                    new = Alien(x,y,i)
                    alien -= 1
                    x+=ALIEN_H_SEP+ALIEN_WIDTH
                    new.x = x
                    new.y = y
                    new.source = i
                    ARow.append(new)
                self._aliens.append(ARow)
                rowc -= 1
                alien = ALIENS_IN_ROW
                x=ALIEN_H_SEP+ALIEN_WIDTH
                y += ALIEN_V_SEP + ALIEN_HEIGHT
                rows -= 1

    def getRPos(self):
        """
        Get the right most position of the aliens
        """
        c = ALIENS_IN_ROW-1
        while c >=0:
            i = 0
            for a in range(ALIEN_ROWS):
                if self._aliens[a][c] != None:
                    return self._aliens[a][c].x + ALIEN_WIDTH/2
                else:
                    i +=1
            if i == ALIEN_ROWS:
                c -=1

    def getLPos(self):
        """
        Get the left most position of the aliens
        """
        c = 0
        while c <= ALIENS_IN_ROW-1:
            i = 0
            for a in range(ALIEN_ROWS):
                if self._aliens[a][c] != None:
                    return self._aliens[a][c].x - ALIEN_WIDTH/2
                else:
                    i +=1
            if i == ALIEN_ROWS:
                c +=1

    def _animateRightAlien(self):
        """
        Animates the alien wave to move to the right and move down one step
        when it reaches the right side of the game screen. Then it changes
        self._direction = True.
        """
        incr = self.speedChange()
        max = self._maxAlien()
        min = self._minAlien()
        right = self.getRPos()

        if right <= GAME_WIDTH-ALIEN_H_SEP:
            if self._direction == False:
                for a in self._aliens:
                    for b in a:
                        if b != None:
                            b.x += ALIEN_H_WALK
                self._time = 0
                self._alienStep += 1
            end = ALIENS_IN_ROW - 1
        if right > GAME_WIDTH-ALIEN_H_SEP:
            if self._direction == False:
                for a in self._aliens:
                    for b in a:
                        if b != None:
                            b.y -= ALIEN_V_SEP
                            self._direction = True
                self._time = 0
                self._alienStep += 1

    def _animateLeftAlien(self):
        """
        Animates the alien wave to move to the left and move down one step
        when it reaches the left side of the game screen. Then it changes
        self._direction = False.
        """
        incr = self.speedChange()
        max = self._maxAlien()
        min = self._minAlien()
        left = self.getLPos()

        if left > ALIEN_H_SEP:
            if self._direction == True:
                for a in self._aliens:
                    for b in a:
                        if b != None:
                            b.x -= ALIEN_H_WALK
                self._time = 0
                self._alienStep += 1
            n = 0
        if left <= ALIEN_H_SEP:
            if self._direction == True:
                for a in self._aliens:
                    for b in a:
                        if b != None:
                            b.y -= ALIEN_V_SEP
                            self._direction = False
                self._time = 0
                self._alienStep += 1


    def _createShip(self):
        """
        Creates a new ship object.
        """
        self._ship=Ship()

    def _animateShip(self,input,dt):
        """
        Animates the ship to move left and right on user command.

        Parameter input: The user's input to move the ship
        Precondition: Either the up, left, or right arrows

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        move = 0
        if input.is_key_down('left'):
            move -= SHIP_MOVEMENT
            self._ship.x = max(self._ship.x+move,0)
        if input.is_key_down('right'):
            move += SHIP_MOVEMENT
            self._ship.x = min(self._ship.x+move, GAME_WIDTH)
        #extra feature
        if self._ship != None :
            self._ship.x += move
            self._ship.x = max(self._ship.x, 0+SHIP_WIDTH/2)
            self._ship.x = min(self._ship.x, GAME_WIDTH-SHIP_WIDTH/2)

    def _createPlayerBolt(self,input,dt):
        """
        Creates a bolt fired from the ship on user command.

        Parameter input: The user's input to shoot an arrow
        Precondition: input is the up arrow

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        curr_keys = input.key_count
        change = curr_keys > 0 and self._lastkeys == 0
        if self._key == False and input.is_key_down('up'):
            if self._ship != None:
                self._bolts.append(Bolt(self._ship.x, +\
                (SHIP_HEIGHT+BOLT_HEIGHT),'red',BOLT_SPEED))
                self._key = True

    def _moveBolt(self,input,view,dt):
        """
        Animates the bolt to shoot up on user command.

        Parameter input: The user's input to shoot an arrow
        Precondition: input is the up arrow

        Attribute view: the game view, used in drawing
        Invariant: view is an instance of GView (inherited from GameApp)

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if input.is_key_down('up') and self._isPlayerBolt()==True:
            if self._ship != None:
                self._createPlayerBolt(input,dt)
                velocity = BOLT_SPEED
                self._velocity = velocity

    def _isPlayerBolt(self):
        """
        Determines whether the bolt is from the player or alien.
        """
        for y in self._bolts:
            if y.getVelocity() > 0:
                return True
        return False

    def _removeBolt(self):
        """
        Removes a bolt once it has left the game screen.
        """
        for bolt in self._bolts:
            if (bolt.y-BOLT_HEIGHT/2)>GAME_HEIGHT:
                self._bolts.remove(bolt)
                self._key = False
            elif bolt.y + BOLT_HEIGHT < 0:
                self._bolts.remove(bolt)

    def _alienBolt(self):
        """
        Returns either True of False if the alien selected to shoot the bolt
        exists.
        If it returns True, it creates an alien bolt and is added to the
        self._bolts list.
        """
        exists = False
        temp = 0
        rand = random.randint(0,ALIENS_IN_ROW-1)
        for n in range(ALIEN_ROWS):
            if self._aliens[n][rand] != None:
                exists = True

        if exists == True:
            row = self._findBottom(rand)
            x = self._aliens[row][rand].x
            y = self._aliens[row][rand].y-ALIEN_HEIGHT-BOLT_HEIGHT
            bolt = Bolt(x,y,'green',-BOLT_SPEED)
            self._bolts.append(bolt)
        return exists

    def _findBottom(self,col):
        """
        Returns the y position of the first alien that exists. Its x position
        is less than the game height and is in the column pos.

        Parameter col: The column to search
        Precondition: col is an int >= 0 and <= GAME_HEIGHT
        """
        min = GAME_HEIGHT
        mpos = 0
        for x in range(self.getLengthAlien()):
            if self._aliens[x][col] != None and self._aliens[x][col].y < min:
                min = self._aliens[x][col].y
                mpos = x
        return mpos

    def _defLine(self):
        """
        Creates the defense line
        """
        self._dline=GPath(points = [0,100,GAME_WIDTH,100], linewidth = 1.5,
            linecolor = 'cyan')

    def _shipCollide(self):
        """
        Method to check if a ship bolt collided with an alien in the wave.
        If a collision occurs, the alien that was hit is set to None and the
        bolt is removed, and self._key is also set to False.
        """
        for s in range(self.getLengthAlien()):
            for t in range(len(self._aliens[0])):
                for b in self._bolts:
                    if self._aliens[s][t] != None and + \
                        self._aliens[s][t].collides(b):
                        self._aliens[s][t] = None
                        self._bolts.remove(b)
                        self._key = False

    def _alienCollide(self):
        """
        Method to check if the alien bolt collided with the ship.
        If a collision occurs, self._ship is set to None and self._bolts is
        set to an empty list.
        """
        for b in self._bolts:
            if self._ship != None and self._ship.collides(b):
                self._ship = None
                self._bolts = []
                self._key = False
                self._lives -= 1

    def _maxAlien(self):
        """
        Returns the maximum y cooridinate of an existing alien in the alien
        wave.
        """
        maxA = 0
        for r in self._aliens:
            for y in r:
                if(y != None):
                    maxA = max(maxA,y.x)
        return maxA

    def speedChange(self):
        """
        Changes the speed of aliens after each alien is killed.
        """
        original = ALIENS_IN_ROW *ALIEN_ROWS
        i = 0 #  accumulator
        for x in range(ALIEN_ROWS):
            for y in range(ALIENS_IN_ROW):
                if self._aliens[x][y] != None:
                    i+=1
        return i / original

    def gameOver(self):
        """
        Check if the game is over if there are no more aliens. If the total
        number of aliens that are gone is equal to the orignal wave,
        then set the game over attribute as True
        """
        i = 0 # accumulator for the number of None objects
        for x in range(ALIEN_ROWS):
            for y in range(ALIENS_IN_ROW):
                if self._aliens[x][y] ==None:
                    i +=1
        if i == ALIEN_ROWS * ALIENS_IN_ROW:
            self._gameOver = True

        for x in range(ALIEN_ROWS):
            for y in range(ALIENS_IN_ROW):
                if self._aliens[x][y] !=None:
                    positiony = self._aliens[x][y].getAY() - ALIEN_HEIGHT/2
                    if posy<= self._dline:
                        self._gameOver = False
