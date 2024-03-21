class MasterMind is the backend class, which allows to play logic game Master Mind. In the Czech Republic is this game known under the name Logic.

Rules of the game:

It is a game for 2 players. One player is a codemaker. The second player is a codebreaker. The Target of the game is to break a secret code.
Standard version: 
There are code pegs in 8 different colours. They have a round head. There are 5 holes. Guessing the player inserts into each hole one code peg. The colours of code pegs can be repeated in any way.
There are key pegs, which are black and white. Key pegs are flat-headed and are smaller than code pegs.
In the beginning, the codemaker creates a secret combination and covers it with the shield. The secret combination is visible to the codemaker, but not to the codebreaker.
The codebreaker tries to guess the pattern. He inserts code pegs into holes. When he finishes his attempt, the codemaker checks and evaluates it. He inserts key pegs into small holes on the left of the code pegs.
In the beginning, he inserts black key pegs into holes, then white key pegs. He inserts key pegs from left to right, independently of the position of code pegs.
Black peg means good value in a good place. White peg means good value but in a bad position.
The game continues until the codemaker breaks the secret code or all attempts are exhausted.

The old variation:
There are 6 different colours. There are 4 holes. There are usually also 10 attempts. The rest of the rules are the same as by standard version.

Stuff in if __name__ == "__main__":

Class MasterMind is primarily intended as the frontend for larger projects. It should be imported in this case.
But for testing purposes and to allow playing games in a single command line, this code snippet is used.
It is also a tutorial for a better understanding using of class MasterMind.

    attempt = 10 # you have 10 attempts
    value = 6 # value can be 1, 2, 3, 4, 5, 6
    digit = 4 # 4 digits of secret code
    time = 5  #5 minutes to break code
    the_game = MasterMind(attempt, value, digit, time)
Initiate class MasterMind as the_game.


print(repr(the_game))
generates a report about the actual state of the current game.


while the_game.is_running():
  .....
Pooling of the flag for game running.
Until the game is active, you can try to break the secret code.
print(repr(the_game)) informs you about the actual state of the current game.
When the game is over, this flag is cleared.

When the game is over, the final game report is generated and saved to the file.

Description of class MasterMind and how to use it:
class Attempt:
class Attempt is part of the class MasterMind. For each attempt to break code, one object of the class MasterMind.

def __init__(
        self, att_no, your_code=[], white=0, black=0, duration=datetime.time(0)
    ):
For a new attempt new object is initialised. Its attributes are:
 att_no  ... index of attempt
 your_code ... the value of the guessed code
 white = number of white code pegs
 black = number of black code pegs
 duration = time per attempt

def __repr__(self):
Return text string with values of this attempt.

if __name__ == "__main__":
This short main is used for testing purposes and also to show possibilities, which offers Class Mastermind. 
Class MasterMind(attempt, value, digit, time) is primarily intended to be used as an imported module.