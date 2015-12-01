#!/usr/bin/python
import random
import signal
import sys
import curses
import time

# Audio support
pyaudio_available = False
try:
  import pyaudio
  import wave
  import threading
  pyaudio_available = True
except ImportError:
  pyaudio_available = False

class Fire(object):
  def __init__(self, speed):
    self.speed = speed
    self.screen = curses.initscr()
    self.screen.clear()

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1,curses.COLOR_YELLOW,0)
    curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_RED)
    curses.init_pair(3,curses.COLOR_RED,curses.COLOR_RED)
    curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_RED)

    self.resize()
    if pyaudio_available:
      self.loop = True
      self.lock = threading.Lock()
      t = threading.Thread(target=self.play_fire)
      t.start()

  def play_fire(self):
    CHUNK = 1024
    p = pyaudio.PyAudio()
    wf = wave.open('fire.wav', 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
              channels=wf.getnchannels(),
              rate=wf.getframerate(),
              output=True)
    loop = True
    while loop:
      self.lock.acquire()
      loop = self.loop
      self.lock.release()
      data = wf.readframes(CHUNK)
      if (len(data) == 0): wf.rewind()
      if (len(data) < 0): break
      stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

  def shutdown(self):
    if pyaudio_available:
      self.lock.acquire()
      self.loop = False
      self.lock.release()

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
      b_color = [(((j < self.width - 2) and (b_prev[j+1] == 'X') and random.randint(0,1)) + 
                  ((j > 0) and (b_prev[j - 1] == 'X') and random.randint(0,1)) +
                  ((b_prev[j] == 'X') and random.randint(0,1)) +
                  (random.randint(0,1)) + 1) * (b[j] == 'X') for j in range(self.width - 1)]
      for j in range(0, self.width - 1):
        self.screen.addch(i, j, ord(b[j]), curses.color_pair(b_color[j]) | curses.A_BOLD)
      b_prev = b
    self.screen.refresh()
    self.screen.timeout(50)
    time.sleep(1 / self.speed)

if __name__ == "__main__":
  speed = 20
  if len(sys.argv) >= 2:
    speed = int(sys.argv[1])
  fire = Fire(speed)

  def signal_handler(signal, frame):
    curses.endwin()
    if fire:
      fire.shutdown()
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)

  while 1: fire.redraw()
