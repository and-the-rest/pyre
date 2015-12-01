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
  MAX_INTENSITY = 100
  NUM_PARTICLES = 5
  NUM_COLORS = 4

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

    self.heat = [curses.color_pair(i) for i in range(1,5)]
    self.particles = [' ', '.', '*', '#', '@']
    assert(len(self.particles) == self.NUM_PARTICLES)

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
    self.prev_fire = [[0 for i in range(self.width - 1)] if j > 0 else [self.MAX_INTENSITY for i in range(self.width - 1)] for j in range(self.height - 1)]
    self.redraw()

  # Returns the intensity of the cell in the previous iteration
  def intensity(self, i, j):
    if (i < 0): return random.randint(self.MAX_INTENSITY//2, self.MAX_INTENSITY)
    if (j < 0): return 0
    if (j >= self.width - 1): return 0
    return min(self.prev_fire[i][j], self.MAX_INTENSITY)

  def redraw(self):
    for i in range(self.height - 1):
      for j in range(self.width - 1):
        curr = self.intensity(i - 1, j) + self.intensity(i - 1, j + 1) + self.intensity(i - 1, j - 1)
        curr = random.randint(curr // 2, curr) / ((i + 1) ** 0.3)
        particle_index = int(curr / self.MAX_INTENSITY * self.NUM_PARTICLES / 3)
        color_index = int(curr / self.MAX_INTENSITY * self.NUM_COLORS / 3) + 1
        self.screen.addch(self.height - i - 1, j, self.particles[particle_index],
                          curses.color_pair(color_index)|curses.A_BOLD)
        self.prev_fire[i][j] = int(curr)
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
