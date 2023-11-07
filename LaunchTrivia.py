# -*- coding: utf-8 -*-

'''
Example to launch a simple trivia
'''

from mustrigen.mustrigen import play_trivia

# Setup the game parameters:
guess_time = 25 # how long before the music title is revealed
play_time = 35 # how long before jumping to next title

url_file = './ExampleTrivia.txt' # file containing the urls for the Trivia, along with the music titles and category

print("Activate 'loudness equalization' in Windows sound parameters for a better volume balance !")

play_trivia(file=url_file,guess_time=guess_time,play_time=play_time)
