#!/usr/bin/env python
#
# The Matrix with python and curses
# Howard Gong
# 2013, Shanghai, China

import random, string
import curses

class MatrixLine:
    def __init__(self, maxy, maxx):
        self.len = random.randrange(5, maxy)
        self.str = ''
        for i in range(self.len-1):
            self.str += chr(random.randrange(ord('0'),  ord('z')))
        self.str += ' '
        self.x = random.randrange(0, maxx)
        self.y = 0
        self.speed = random.random()
        if self.speed < 0.3: self.speed = 0.3
        self.blink = False

class MatrixScr:
    def __init__(self, scr):
        self.scr = scr
        self.maxy, self.maxx = scr.getmaxyx()
        self.scr.clear()

        self.lines = []
        for i in range(280):
            self.lines.append(MatrixLine(self.maxy, self.maxx))

        my_bg = curses.COLOR_BLACK
        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
            curses.init_pair(2, curses.COLOR_BLACK, my_bg)
            curses.init_pair(3, curses.COLOR_GREEN, my_bg)
            curses.init_pair(4, curses.COLOR_WHITE, my_bg)

    def redraw(self):
        for i in self.lines:
            i.y += i.speed
            if i.y > (self.maxy + i.len):
                i.y = 0
                i.x = random.randrange(0, self.maxx)
                i.speed = random.random()
                if i.speed < 0.3: i.speed = 0.3
            for n, j in enumerate(i.str):
                tmpy = i.y - n
                if tmpy < self.maxy-1 and tmpy > 0:
                    if n == 0 and i.blink:
                        self.scr.attrset(curses.color_pair(4) | curses.A_BOLD | curses.A_REVERSE)
                        i.blink = False
                    elif n==0:
                        i.blink = True
                        self.scr.attrset(curses.color_pair(4) | curses.A_BOLD)
                    elif n < i.len/2:
                        self.scr.attrset(curses.color_pair(3) | curses.A_BOLD)
                    else:
                        self.scr.attrset(curses.color_pair(3))
                    self.scr.addch(int(tmpy), int(i.x), j)


def main(scr):
    board = MatrixScr(scr)
    scr.nodelay(1)
    while(True):
        c = scr.getch()
        if c == ord('q'):
            break
        board.redraw()
        scr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)

