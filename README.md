# Mustrigen
Mustrigen is a Music Trivia Generator written in Python: feed it with a list of urls poiting to diverse musics on Youtube, and the scripts will generate and play a Music Trivia Game for you ! 

# Requirements:
- vlc (https://www.videolan.org/)

# Setup:
The code have only been tested on Windows, but should works on Linux.

**1 - Clone the repository with git (https://github.com/Amidattelion/Mustrigen.git) or download and extract it**

**2 - Install the requirements with pip:**

It is advised to first create and activate a dedicated virtual environment before proceeding.
Open a terminal and cd in the "SYMP" folder that you have just extracted, then run the following command to install the python dependencies:

```
$ pip install -r requirements.txt
```

This code relies on pafy, which has not been updated to the latest Youtube video format. We thus need to install a custom fork to fix the known "dislkike_count" bug from pafy:

```
$ pip install https://github.com/Amidattelion/pafy/archive/refs/heads/develop.zip
```

**3 - Create an empty file and fill it with urls from Youtube:**
The file must be in .txt format, and each line corresponds to a music video on Youtube. The line format is the following:

```
Title;Category;URL
```

- Title: the title of the music (will be used to display the answer)
- Category: category of this music/video (video game, film, classical music, anime...) -> you can create any category you want, the code will then identify all existing category and randomly choose musics while looping through all categories
- URL: url to the youtube video

The "ExampleTrivia.txt" file gives a complete example of my last Trivia game, with ~2400 songs and different categories.

**4 - Play**

Edit the "LaunchTrivia.py" file and change the following parameters to suits your needs:
- guess_time: the time to guess before displaying the answer, in seconds
- play_time : the total time a music is played before jumping to next one
- url_file  : path to the file containing the game's content (name, category and url for each music)

Launch the game: either with "python LaunchTrivia.py" or with "LaunchTrivia.bat". 

Once the game is launched, some usefull shortcuts can be used with the keyboard:
- ctrl+P : pause game
- ctrl+R : resume game
- ctrl+arrow up: raise volume
- ctrl+arrow down: lower volume
- ctrl+space: skip to next music
- ctrl+Q : quit game
