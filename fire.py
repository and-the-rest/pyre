#!/usr/bin/python
import random
import signal
import sys
import curses
import time

def signal_handler(signal, frame):
  curses.endwin()
  sys.exit(0)

class Fire(object):
  def __init__(self, speed):
    self.speed = speed
    self.screen = curses.initscr()
    curses.curs_set(0)
    self.screen.clear()
    self.resize()

  def resize(self):
    self.height, self.width = self.screen.getmaxyx()[:2]
    self.redraw()

  def redraw(self):
    b_prev = ['X' for i in range(self.width - 0)]
    for i in range(self.height - 1, 0, -1):
      b = ['X' if (
            ((self.height - i) < random.randint(0, self.height))
            or
            (j < self.width - 2 and j > 0 and b_prev[j] == 'X' and b_prev[j + 1] == 'X' and b_prev[j - 1] == 'X' and (self.height - i) < random.randint(self.height//4, self.height))
          )
          else ' ' for j in range(self.width - 1)]
      self.screen.addstr(i, 0, ''.join(b))
      b_prev = b
    self.screen.refresh()
    self.screen.timeout(50)
    time.sleep(1 / self.speed)

def main():
  signal.signal(signal.SIGINT, signal_handler)
  speed = 20
  if len(sys.argv) >= 2:
    speed = int(sys.argv[1])
  f = Fire(speed)
  while 1: f.redraw()

main()
