# pyre
TUI Fire in Python.  If you have PyGame, it uses sound with volume controls (- for down/+ for up).
If you don't have PyGame, you can still get sound if you have PyAudio, but there will be no volume controls.

## Usage

For a fire with a refresh rate of 10Hz:

    ./pyre.py 10


![Screenshot](http://i.imgur.com/aFindkY.png)

## Contributing

Goals:

 - Aim to be extremely lightweight
     - All used libraries should be optional (checked at runtime)
     - Prefer the smallest available library to accomplish any goal
 - Cross platform
     - Avoid platform specific libraries or usage
     - If platform awareness is necessary, ensure the feature is implemented in all cases (Linux, OS X, Windows)
 - Compatible for Python 2.7 and greater
     - Use generic design patterns that work for both Python 2.7 and Python 3.0+ (e.g. `//` for integer division).
 - Open dialogue
     - Every commit should be approved by someone else before being merged to ensure a second set of eyes has seen the change
