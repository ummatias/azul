# conftest.py

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Now you can import modules from src directory
from game import Game
from gameboard import GameBoard

# Optionally, define fixtures or hooks if needed for your tests
