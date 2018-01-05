from Tkinter import *
import math
import time
import random

root = Tk()

class Vector():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def len(self):
        return math.sqrt((self.x)**2+(self.y)**2)

    def normalize_to(self, c):
        self.x = (c/(self.len()))*self.x
        self.y = (c/(self.len()))*self.y

    def limit(self, max):
        if self.len() > max:
            self.normalize_to(max)

w1 = 900
h1 = 700

canvas1 = Canvas(root, width=w1, height=h1, bg='white')
canvas1.pack()

r2=10

vmax1 = 0.04
amax1 = 0.000022

class Ball():
    def __init__(self, startx, starty, vmax):
        self.r = Vector(startx, starty)
        self.v = Vector(0.05,0.05)
        self.a = Vector(0,0)
        self.vmax = vmax
        self.ballfig = canvas1.create_oval(self.r.x-r2,self.r.y-r2,self.r.x+r2,self.r.y+r2, fill='red')

ball1 = Ball(w1/2,h1/2,vmax1)

goalwd = 5
goalh = 5

goals = {}

for j in range(6):
    goals['goal %d' % j] = []
    goals['goal %d' % j].append(Vector(int(4 * goalwd + (random.random()) * (w1 - 8 * goalwd)), int(4 * goalh + (random.random()) * (h1 - 8 * goalh))))
    goals['goal %d' % j].append(canvas1.create_rectangle(goals['goal %d' % j][0].x - goalwd, goals['goal %d' % j][0].y - goalh, goals['goal %d' % j][0].x + goalwd, goals['goal %d' % j][0].y + goalh, fill='green'))

def new_goal(last):
    canvas1.delete(goals[last][1])
    goals[last][0] = Vector(int(4*goalwd+ (random.random())*(w1-4*goalwd)),int(4*goalh + (random.random())*(h1-4*goalh)))
    goals[last][1] = canvas1.create_rectangle(goals[last][0].x - goalwd, goals[last][0].y - goalh, goals[last][0].x + goalwd, goals[last][0].y + goalh, fill='green')

def follow_mouse():
    diff_to_goals = {}
    for key in goals:
        diff_new = Vector(goals[key][0].x-ball1.r.x,goals[key][0].y-ball1.r.y)
        diff_to_goals[key] = [diff_new, diff_new.len()]
    dir1_var = min(diff_to_goals, key=lambda k: diff_to_goals[k][1])
    dir1 = diff_to_goals[dir1_var][0]
    if dir1.len() < 3*goalwd:
        new_goal(dir1_var)
    dir1.normalize_to(amax1)
    ball1.a = dir1
    ball1.v.x += ball1.a.x
    ball1.v.y += ball1.a.y
    ball1.v.limit(ball1.vmax)


while True:
    if (ball1.r.x + r2 >= w1) or (ball1.r.x <= 0):
        ball1.v.x = ball1.v.x*-1
    if (ball1.r.y + r2 >= h1) or (ball1.r.y <= 0):
        ball1.v.y = ball1.v.y*-1
    follow_mouse()
    canvas1.move(ball1.ballfig, ball1.v.x, ball1.v.y)
    ball1.r.x += ball1.v.x
    ball1.r.y += ball1.v.y
    root.update()