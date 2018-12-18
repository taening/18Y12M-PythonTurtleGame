# -*- coding: utf-8 -*-
from turtle import *
import random as rd

"""
    Title: Game
    Name: Turtle.io
    Author: SeoPaul
    E-mail: m9472757c@gmail.com
"""


class TurtleGame:
    def __init__(self, width, height):
        self.screen = Screen()
        self.user = Turtle()
        self.com = Turtle()
        self.ball = Turtle()

        self.__color_list = ['red', 'green', 'yellow', 'pink', 'white']
        self.__ball_list = list()

        self.__screen_info = {'width': width,
                              'height': height,
                              'num': int(),
                              'mouse': {'coordinate': tuple()},
                              'user': {'coordinate': tuple()},
                              'com': {'coordinate': tuple()}}
        self.__user_info = {'name': str(),
                            'color': 'red',
                            'size': 1.2,
                            'score': 0}
        self.__com_info = {'name': 'Com1',
                           'color': 'blue',
                           'size': 1.2,
                           'score': 0}

        self.__screen_setting()
        self.__marker_setting()

    def __screen_setting(self):
        """
            < Screen Setting >
            a. Width, Height Setting
            b. Screen Title Setting
            c. Screen Background Color Setting
        """
        self.screen.setup(self.__screen_info['width'], self.__screen_info['height'], 0, 0)
        self.screen.title('turtle.io')
        self.screen.bgcolor('black')
        self.__screen_info['num'] = int(self.screen.numinput('< Setting Board >', '공의 갯수', 10, minval=10, maxval=50))

    def __marker_setting(self):
        self.__user_info['name'] = self.screen.textinput('< Setting Board >', '유저 이름')
        self.__user_info['color'] = self.screen.textinput('< Setting Board >', '색 선택')

        if self.__user_info['color'].lower() not in self.__color_list:
            self.screen.textinput('< Warning >', '유저에게 제공하지 않는 색(자동 빨강 설정)')
            self.__user_info['color'] = 'red'

        self.user.shape('turtle')
        self.user.color(self.__user_info['color'])
        self.user.penup()
        self.user.turtlesize(self.__user_info['size'])

        self.com.shape('turtle')
        self.com.color('blue')
        self.com.penup()
        self.com.turtlesize(self.__com_info['size'])

        self.ball.shape('circle')
        self.ball.color('green')
        self.ball.penup()

        w, h, mg = self.__screen_info['width'], self.__screen_info['height'], 20
        self.user.setpos(rd.randint(-(w // 2) + mg, w // 2 - mg), rd.randint(-(h // 2) + mg, h // 2 - mg))
        self.com.setpos(rd.randint(-(w // 2) + mg, w // 2 - mg), rd.randint(-(h // 2) + mg, h // 2 - mg))

        for i in range(self.__screen_info['num']):
            num = rd.randint(0, len(self.__color_list) - 1)
            b = self.ball.clone()
            b.color(self.__color_list[num])
            b.setpos(rd.randint(-(w // 2) + mg, w // 2 - mg), rd.randint(-(h // 2) + mg, h // 2 - mg))
            self.__ball_list.append(b)
        self.ball.hideturtle()

    def play(self):
        self.__screen_info['user']['coordinate'] = self.user.pos()
        self.__screen_info['com']['coordinate'] = self.com.pos()

        w, h, mg = self.__screen_info['width'], self.__screen_info['height'], 20
        coor_user = self.__screen_info['user']['coordinate']
        coor_com = self.__screen_info['com']['coordinate']

        if coor_user[0] < -(w // 2) + mg:
            self.user.setpos(-(w // 2) + mg, coor_user[1])
        if coor_user[0] > w // 2 - mg:
            self.user.setpos(w // 2 - mg, coor_user[1])
        if coor_user[1] < -(h // 2) + mg:
            self.user.setpos(coor_user[0], -(h // 2) + mg)
        if coor_user[1] > h // 2 - mg:
            self.user.setpos(coor_user[0], h // 2 - mg)

        if coor_com[0] < -(w // 2) + mg:
            self.com.setpos(-(w // 2 + mg), coor_com[1])
        if coor_com[0] > w // 2 - mg:
            self.com.setpos(w // 2 - mg, coor_com[1])
        if coor_com[1] < -(h // 2) + mg:
            self.com.setpos(coor_com[0], -(h // 2) + mg)
        if coor_com[1] > h // 2 - mg:
            self.com.setpos(coor_com[0], h // 2 - mg)

        if self.__screen_info['num'] != 0:
            # User & Ball Distance Check
            for b in self.__ball_list:
                if self.user.distance(b) < 12:
                    b.hideturtle()
                    self.__ball_list.remove(b)
                    self.__screen_info['num'] -= 1
                    self.__user_info['size'] += 0.2
                    self.__user_info['score'] += 10
                    self.user.turtlesize(self.__user_info['size'])

            # Computer Target Search
            distance = list()
            if self.__ball_list:
                for b in self.__ball_list:
                    b_x, b_y = b.position()
                    distance.append(abs(b_x - coor_com[0]) + abs(b_y - coor_com[1]))
                idx = distance.index(min(distance))
                self.com.setheading(self.com.towards(self.__ball_list[idx].pos()))

                # Com & Ball Distance Check
                if self.com.distance(self.__ball_list[idx]) < 12:
                    self.__ball_list[idx].hideturtle()
                    self.__ball_list.pop(idx)
                    self.__screen_info['num'] -= 1
                    self.__com_info['size'] += 0.2
                    self.__com_info['score'] += 10
                    self.com.turtlesize(self.__com_info['size'])

            # User & Computer Moving
            self.user.forward(10)
            self.com.forward(6)
        else:
            if self.__user_info['size'] > self.__com_info['size']:
                if self.com.distance(self.user) < 12:
                    self.com.hideturtle()
                    self.screen.textinput('<Result>', self.__user_info['name'] + ' WIN!!!')
                    self.screen.exitonclick()
                self.user.forward(10)
                self.com.forward(0)
            elif self.__user_info['size'] == self.__com_info['size']:
                self.user.forward(0)
                self.com.forward(0)
                self.screen.textinput('<Result>', 'Draw')
                self.screen.exitonclick()
            else:
                self.com.setheading(self.com.towards(self.user.pos()))
                if self.com.distance(self.user) < 12:
                    self.user.hideturtle()
                    self.screen.textinput('<Result>', self.__com_info['name'] + ' WIN!!!')
                    self.screen.exitonclick()
                self.user.forward(0)
                self.com.forward(10)
        self.screen.ontimer(self.play, 100)

    def turn_right(self):
        self.user.setheading(0)

    def turn_up(self):
        self.user.setheading(90)

    def turn_left(self):
        self.user.setheading(180)

    def turn_down(self):
        self.user.setheading(270)

    def run(self):
        self.screen.onkeypress(self.turn_right, 'Right')
        self.screen.onkeypress(self.turn_left, 'Left')
        self.screen.onkeypress(self.turn_up, 'Up')
        self.screen.onkeypress(self.turn_down, 'Down')
        self.screen.listen()
        self.play()
        self.screen.mainloop()


if __name__ == '__main__':
    t = TurtleGame(width=500, height=500)
    t.run()
