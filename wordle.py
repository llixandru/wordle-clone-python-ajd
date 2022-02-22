# Wordle example in Python

import re
from rich.console import Console
import soda_ajd as word

console = Console()

# Function to compare the letters and display the squares

def compare(a, b):
    for x, y in zip(a, b):
        if x == y:
          console.print("🟩", end = '')
        elif b.find(x) <= 0: 
          console.print("⬛", end = '')
        else:
          console.print("🟨", end = '')

# Main

if __name__ == "__main__":

  # Get word from database
  w = word.get_word().lower()

  # Number of guesses = 6
  i = 6

  while i >= 1:
    guess = console.input("\nGuess: ").lower()
    try:
      # Check if input word is exactly 5 letters
      assert len(guess) == 5, console.print("Your guess should be a 5-letter word.")
      # Check if input word only contains allowed characters
      assert re.match("^[a-z]*$", guess), console.print("Your guess should only contain letters.")
    except Exception as e:
      continue

    compare(guess, w)
    
    if guess == w:
        console.print("\nWell done!")
        i = 1
    elif i == 1:
      console.print("\nGood tries! The answer was: " + w)  
    i -= 1