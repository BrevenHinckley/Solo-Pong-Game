'''
Author: Breven G. Hinckley
File Name: Hinckley_Breven_HW5.py

'''
from tkinter import *
import tkinter.font as font
from tkinter import messagebox

class Pong(Frame):
    ''' Class that will run the Pong Game.
        When the ball is heading south and contacts the paddle, your life will remain and the speed of the ball will increase (+ .25 to dy and dx).
        The speed will continue to increase until you can no longer keep up with it and it instead contacts the south wall.
        When the ball contacts the south wall, you lose a life and the speed is reset to its default 2 dy and dx.
        You begin the game with 5 lives, when you reach 0 then game ends. At which point you can either choose to play again or not.
        You can control the paddle at the bottom of the screen using the Right and Left arrow keys or alternatively the a and d keys. '''
    
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Pong Game")
        self.grid()

        ''' First row containing two labels in seperate columns. Fonts and spacing attributes used to get desired look.
            First label is for displaying the remaining lives, second label is for displaying current speed of the ball. '''
        font1 = font.Font(size = 20, family = "Verdana", weight = "bold")
        self._scoreLabel = Label(self, text = "Lives Left: 5", font = font1, bg = "#F9EEBC", fg = "black")
        self._scoreLabel.grid(row = 0, column = 0, sticky = N+S+W+E, ipadx = 270)
        self._speedLabel = Label(self, text = "Speed: 2", bg = "#F9EEBC")
        self._speedLabel.grid(row = 0, column = 1, sticky = N+S+W+E)

        ''' Second row the Canvas that the game will be played on. '''
        canvas_width = 800
        canvas_height = 400 
        self.canvas = Canvas(self, width = canvas_width, height = canvas_height , bg = "#E6FDFF")
        self.canvas.grid(row = 1, column = 0, columnspan = 2) # Columnspan of 2 to match the first row.

        ''' paddle creation along with later used variables '''
        self._paddleTopX = 360
        self.paddle_width = 80
        self.paddle_height = 20
        self.canvas.create_rectangle(360, 380, 440, 400, fill = "black", tags = "paddle")

        ''' Binding keys to move the paddle with their event method. I included a and d with the arrow keys incase someone
            was used to that button layout. I got the idea for this from when I first started testing and kept trying to use
            a and d because I was used to the w,a,s,d layout from other games. '''
        self.canvas.bind("<Left>", self.movePaddleLeft) and self.canvas.bind("<a>", self.movePaddleLeft)
        self.canvas.bind("<Right>", self.movePaddleRight) and self.canvas.bind("<d>", self.movePaddleRight)

        ''' Draws the ball near the top left corner of the canvas; top-left corner of surrounding box is at (2,2) '''
        self._ball_diameter = 20
        self._top_left_x = 2 # top-left coordinate of circle's rectangular outline 
        self._top_left_y = 2
        self.canvas.create_oval(self._top_left_x, self._top_left_y, self._top_left_x + self._ball_diameter,
                                self._top_left_y + self._ball_diameter, fill = "#FCE6B3", tags = "ball")

        ''' Various variables used in the main loop only. '''
        horizontal_direction = "east" # ball's horizontal direction
        vertical_direction = "south" # ball's vertical direction
        dy = 2 # dy and dx will determine the speed of the ball. As the ball hits the paddle the speed will increase
        dx = 2 # the speed will reset to these numbers if the ball hits the south wall
        livesLeft = 5 # Starting amount of lives, counts down in main loop.
        counter = 2 # Counter used soley for displaying the speed of the ball.

        self.canvas.focus_set()

        ''' main loop '''
        while True:
            try:
                if horizontal_direction == "east":
                    ''' Moves the ball horizontally to the right dx pixels every 16 milliseconds. '''
                    self.canvas.move("ball", dx, 0)
                    self._top_left_x += dx
                    ''' When the ball hits the east wall, switch to left horizontal direction. '''
                    if self._top_left_x >= canvas_width - self._ball_diameter:
                        self._top_left_x = canvas_width - self._ball_diameter
                        horizontal_direction = "west"
                        
                else: # When horizontal direction is west.
                    ''' Moves the ball horizontally to the left dx pixels every 16 milliseconds. '''
                    self.canvas.move("ball", -dx, 0)
                    self._top_left_x -= dx
                    ''' When the ball hits the west wall, switch to right horizontal direction. '''
                    if self._top_left_x <= 0:
                        self._top_left_x = 0
                        horizontal_direction = "east"
                
                if vertical_direction == "south":
                    ''' Moves the ball vertically down dy pixels every 16 milliseconds. '''
                    self.canvas.move("ball", 0, dy)
                    self._top_left_y += dy
                    ''' While moving south, the ball will first vertically check if it is in the paddle's range. When it is, it will then
                        horizontally check if the ball is within the paddle's domain (isCollision method). If True, increase speed and change
                        vertical direction to north. Also, update speed label. '''
                    if self._top_left_y + self._ball_diameter >= canvas_height - self.paddle_height:
                        if self.isCollision() == True:
                            self._top_left_y = canvas_height - self.paddle_height - self._ball_diameter
                            ''' Every time the ball is hit by the paddle, the old ball is deleted and a new one is created at the correct location.
                                This was added as bug fix. In testing, whenever I would move the paddle over the ball's location late but before it
                                contacted the south wall, it would mess up the ball's alignment because it could not correctly calculate the paddle's
                                height. This would basically mess up the entire game. With this fix, the ball is correctly moved to the top of the paddle
                                at the same x location that it was hit. Thus, eliminating the problem. In the rare case that this bug occurs, the animation
                                can look slightly less normal, but it is still quite a smooth transition. '''
                            self.canvas.delete("ball")
                            self.canvas.create_oval(self._top_left_x, self._top_left_y, self._top_left_x + self._ball_diameter,
                                                    self._top_left_y + self._ball_diameter, fill = "#FCE6B3", tags = "ball")
                            counter += .25
                            self._speedLabel["text"] = "Speed: " + str(counter)
                            dy += .25
                            dx += .25
                            vertical_direction = "north"
                        elif self._top_left_y >= canvas_height - self._ball_diameter:
                            ''' If the ball hits the south wall, switch to up vertical direction, reset speed to 2 (dy and dx default 2 values),
                                lose a life, and update score/speed labels. If livesLeft falls to 1, change the foreground color to red as a warning
                                to the user that this is their last life. If livesLeft falls to 0, the game is over and the user is prompted with a
                                message box asking them if they want to play again. If True, delete the previous iteration of the program and create a new
                                one. If False, the ball is placed in the top left corner and the main loop is broken out of. '''
                            dy = 2
                            dx = 2
                            counter = 2
                            vertical_direction = "north"
                            self._top_left_y = canvas_height - self._ball_diameter
                            livesLeft -= 1
                            self._scoreLabel["text"] = "Lives Left: " + str(livesLeft)
                            self._speedLabel["text"] = "Speed: " + str(counter)
                            if livesLeft == 1:
                                self._scoreLabel["fg"] = "red"
                            if livesLeft == 0:
                                self.canvas.delete("ball")
                                self._top_left_x, self._top_left_y = 2, 2
                                self.canvas.create_oval(self._top_left_x, self._top_left_y, self._top_left_x + self._ball_diameter,
                                                        self._top_left_y + self._ball_diameter, fill = "#FCE6B3", tags = "ball")
                                if messagebox.askyesno(title = "Game Over", message = "Play again?", parent = self) == True:
                                    self.destroy()
                                    Pong().mainloop()
                                else:
                                    break
                            
                        
                else: # Direction is north
                    ''' Moves the ball vertically up dy pixels every 16 milliseconds. '''
                    self.canvas.move("ball", 0, -dy)
                    self._top_left_y -= dy
                    if self._top_left_y <= 0: # When the ball hits the north wall switch
                        vertical_direction = "south"

                ''' After testing, I found that waiting 16 milliseconds made the game run the smoothest on my system.
                    If necessary you can either increase or decrease it to better fit your system. '''
                self.canvas.after(16)
                self.canvas.update()

            except:
                break
                

    def movePaddleRight(self, event):
        ''' Event handler for the Right arrow and d keypress event.
            If the top left x coordinate of the paddle plus the width of the entire paddle are less than 800 pixels (canvas width),
            then move the paddle 5 pixels to the right or east. '''
        if self._paddleTopX + self.paddle_width < 800:
            self.canvas.move("paddle", 5, 0)
            self._paddleTopX += 5

    def movePaddleLeft(self, event):
        ''' Event handler for the Left arrow and a keypress event.
            If the top left x coordinate of the paddle is greater than 0,
            move the paddle 5 pixels to the left or west. '''
        if self._paddleTopX > 0:
            ''' Note: Because the paddle moves in multiples of 5 and in combination with these two methods,
                it can never be lower or higher than 0 and 800 pixels (for its entire width). '''
            self.canvas.move("paddle", -5, 0)
            self._paddleTopX -= 5

    def isCollision(self):
        ''' Collision check for the paddle making contact with the ball's rectangle outline from either side or both. '''
        if self._paddleTopX <= self._top_left_x <= self._paddleTopX + self.paddle_width or self._paddleTopX <= self._top_left_x + self._ball_diameter <= self._paddleTopX + self.paddle_width:
            return True
        else:
            return False


def main():
    Pong().mainloop()

main()
