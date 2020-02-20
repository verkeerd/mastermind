from sys import stdout as systemout
from itertools import product
from random import choice
from time import time
import webbrowser
import random
import json


def awards(guess, answer):
    """
    Calculates the number of black and white pegs awarded for a given `guess` and `answer`. Returns a list:
    `[black, white]`.
    """

    black = 0
    white = 0
    guess = list(guess)
    answer = list(answer)
    remainingGuess = guess[:]  # the guessed colours that were not given a black peg
    remainingAnswer = answer[:]  # the answer colours that were not correctly guessed

    for n in range(len(guess)):
        if answer[n] == guess[n]:
            black += 1
            remainingGuess.remove(guess[n])
            remainingAnswer.remove(answer[n])

    for colour in remainingGuess:
        if colour in remainingAnswer:
            white += 1
            remainingAnswer.remove(colour)

    return [black, white]


def printableGuess(END, highlights, guess):
    """
    Returns a printable version of a set of colours from a string of numbers.
    """
    printable = ""
    for colour in guess:
        printable += f"{list(highlights.values())[int(colour)]}  {END}  "
    return printable


def play_knuth():
    """"""
    END, highlights, colours, examples, stdout= set_up_output()

    nColours, nSpaces, intelligence = set_up_game(END, highlights, colours, stdout)

    S = list(product('01234567'[:nColours], repeat=nSpaces))
    fullS = S[:]  # doesn't change

    show_rules(END, highlights, colours, examples, stdout)

    play_main_game_knuth(END, highlights, colours, examples, stdout, S, nSpaces, intelligence)


def set_up_output():
    """"""

    #############
    # VARIABLES #
    #############

    END = '\033[0m'

    highlights = {
        "red": '\033[41m',
        "green": '\033[42m',
        "orange": '\033[43m',
        "blue": '\033[44m',
        "purple": '\033[45m',
        "cyan": '\033[46m',
        "white": '\033[47m',
        "grey": '\033[40m',
    }

    colours = {
        "red": '\033[91m',
        "green": '\033[92m',
        "yellow": '\033[93m',
        "blue": '\033[94m',
        "purple": '\033[95m',
        "cyan": '\033[96m',
        "grey": '\033[97m',
        "white": '\033[98m',
    }

    # answer: "0012"
    examples = [
        "3545",
        "0435",
        "0002",
        "0021",
        "2011",
        "1134",
        "0012",
    ]

    #############
    # FUNCTIONS #
    #############

    class Unbuffered(object):
        def __init__(self, stream):
            self.stream = stream

        def write(self, data):
            self.stream.write(data)
            self.stream.flush()

        def writelines(self, datas):
            self.stream.writelines(datas)
            self.stream.flush()

        def __getattr__(self, attr):
            return getattr(self.stream, attr)

    stdout = Unbuffered(systemout)
    return END, highlights, colours, examples, stdout


def set_up_game(END, highlights, colours, stdout):
    """
    #########
    # SETUP #
    #########
    """
    print(f'''{highlights["red"]}                         
          WELCOME TO MASTERMIND  
                                 {END}

        An implementation of Knuth's mastermind algorithm in Python by @ThomasS1

        How many colours do you want to play with? (3-8){colours["blue"]}''')

    # Loops until valid answer
    while True:
        try:
            nColours = int(input())
            if 8 >= nColours >= 3:
                break
            else:
                raise ValueError()  # goes to except
        except:
            stdout.write("\033[{0};{1}f".format(7, 44))
            stdout.write(f'{colours["red"]}(3-8){END}')
            stdout.write("\033[{0};{1}f".format(8, 0))
            stdout.write("\033[K")
            stdout.write(colours["blue"])

    stdout.write(f'''{END}
        These are your {nColours} colours:
        ''')

    print(printableGuess(END, highlights, '01234567'[:nColours]))

    print(f'''
        How many spaces? (3-6){colours["blue"]}''')

    # Loops until valid answer
    while True:
        try:
            nSpaces = int(input())
            if 6 >= nSpaces >= 3:
                break
            else:
                raise ValueError()  # goes to except
        except:
            stdout.write("\033[{0};{1}f".format(13, 18))
            stdout.write(f'{colours["red"]}(3-6){END}')
            stdout.write("\033[{0};{1}f".format(14, 0))
            stdout.write("\033[K")
            stdout.write(colours["blue"])

    stdout.write(f'''{END}
        Now write down a code with {nSpaces} of the colours.
        You can use each of them once, more than once, or not at all.
        If you don't have coloured pencils, assign them a number,
        but make sure you know what it represents!
        The order is important.
        When you are finished, press enter.
        ''')

    input()  # waits until done

    # Chooses intelligence level
    print(f'''{highlights["red"]}                         
          WELCOME TO MASTERMIND  
                                 {END}

        How intelligent should the computer be? 
        With a higher intelligence level, the computer will 'think' for longer,
        but will take less guesses to find the answer.
        If you have chosen more than 6 colours or 5 spaces,
        maximum of level 2 is recommended.
        Otherwise, level 3 should be fine.
        So, how intelligent should the computer be? (1-3){colours["blue"]}''')

    # Loops until valid answer
    while True:
        try:
            intelligence = int(input())
            if 3 >= intelligence >= 1:
                break
            else:
                raise ValueError()  # goes to except
        except:
            stdout.write("\033[{0};{1}f".format(11, 45))
            stdout.write(f'{colours["red"]}(1-3){END}')
            stdout.write("\033[{0};{1}f".format(12, 0))
            stdout.write("\033[K")
            stdout.write(colours["blue"])
    return nColours, nSpaces, intelligence


def show_rules(END, highlights, colours, examples, stdout):
    """"""

    #########
    # RULES #
    #########

    print(f'''{END}{highlights["red"]}                         
      WELCOME TO MASTERMIND  
                             {END}

    I am now going to give you a series of guesses of your code.
    You must rate my guesses with the following system:
    For every correct colour in the correct position, award me a black peg.
    For every correct colour in the wrong position, award me a white peg.
    If there are multiple of the same colour in my guess, 
    only award me pegs for how many there are in the answer.

    Confused? (Y/N){colours["blue"]}''')

    # Loops until valid answer
    while True:
        confused = input().upper()
        if not (confused == 'Y' or confused == 'N'):
            stdout.write("\033[{0};{1}f".format(12, 11))
            stdout.write(f'{colours["red"]}(Y/N){END}')
            stdout.write("\033[{0};{1}f".format(13, 0))
            stdout.write("\033[K")
            stdout.write(colours["blue"])
        else:
            break

    while confused == 'Y':
        print(f'''{END}{highlights["red"]}                         
      WELCOME TO MASTERMIND  
                             {END}

    HELP PAGE

    Read more detailed rules online  (type R)
    Look at some examples            (type E)
    Go back                          (type G)

    Choose wisely, but don't worry - you can come back later (R/E/G){colours["blue"]}'''
              )

        # Loops until valid answer
        while True:
            helpChoice = input().upper()
            if not (helpChoice in ['R', 'E', 'G']):
                stdout.write("\033[{0};{1}f".format(11, 58))
                stdout.write(f'{colours["red"]}(R/E/G){END}')
                stdout.write("\033[{0};{1}f".format(12, 0))
                stdout.write("\033[K")
                stdout.write(colours["blue"])
            else:
                break

        if helpChoice == 'R':
            if webbrowser.open(
                    "http://www.boardgamecapital.com/game_rules/mastermind.pdf"
            ) == False:
                print(f'''{END}{highlights["red"]}                         
      WELCOME TO MASTERMIND  
                             {END}

    Sorry - tried to open the rules automagically but failed.
    You will have to manually copy this link into a new tab!
    http://www.boardgamecapital.com/game_rules/mastermind.pdf

    Press enter to return to the help page.''')

                input()

        elif helpChoice == 'E':
            answer = '0012'

            print(f'''{END}{highlights["red"]}                         
      WELCOME TO MASTERMIND  
                             {END}

    These examples are for 6 colours and 4 spaces,
    but the same rules always apply.
    They tell you the number of white and black pegs that would
    be awarded for the given guess if this were the answer code:

    Answer: ''' + printableGuess(END, highlights, answer))

            for guess in examples:
                print('\nGuess:  ' + printableGuess(END, highlights, guess))
                black, white = awards(guess, answer)
                print('Black:  ' + str(black))
                print('White:  ' + str(white))

            print('''
    Press enter to return to the help page.''')

            input()

        else:
            confused = 'N'

    print(f'''{END}{highlights["red"]}                         
      WELCOME TO MASTERMIND  
                             {END}

    Remember to follow the rules when scoring my guesses.
    If you don't, the algorithm won't work!

    Press enter when ready to continue.''')

    input()


def play_main_game_knuth(END, highlights, colours, examples, stdout, S, nSpaces, intelligence):
    """"""
    ########
    # GAME #
    ########
    go = 0
    playing = True
    guess = choose_guess_knuth(S, intelligence, stdout)[:nSpaces]

    while playing:

        print(
            f'''{END}{highlights["red"]}                         
      WELCOME TO MASTERMIND  
                             {END}

    Current number of possibilities: {len(S)}

    Guess {go+1}:  ''',
            end='')
        print(printableGuess(END, highlights, guess))

        # End if no possibilities left
        if len(S) == 0:
            print(f'''{END}{highlights["red"]}                         
      WELCOME TO MASTERMIND  
                             {END}

    Current number of possibilities: {colours["red"]}0{END}

    Oh dear, there aren't any possibilities left!
    Not meaning to be cocky, but you must have gone wrong!
    Please restart the program to try again.''')
            quit()

        # End if only one possibility left
        elif len(S) == 1:
            print(f'''{END}{highlights["red"]}                         
      WELCOME TO MASTERMIND  
                             {END}

    Current number of possibilities: {colours["green"]}1{END}

    Answer:   {printableGuess(END, highlights, S[0])}

    Correct? (Y/N){colours["blue"]}''')
            while True:
                try:
                    correct = input().upper()
                    if correct == 'Y' or correct == 'N':
                        break
                    else:
                        raise ValueError()  # goes to except
                except:
                    stdout.write("\033[{0};{1}f".format(9, 10))
                    stdout.write(f'{colours["red"]}(Y/N){END}')
                    stdout.write("\033[{0};{1}f".format(10, 0))
                    stdout.write("\033[K")
                    stdout.write(colours["blue"])

            if correct == 'N':
                print(f'''{END}{highlights["red"]}                         
      WELCOME TO MASTERMIND  
                             {END}

    DOH! Sorry to disappoint...
    If you're sure you entered all the right black/white peg numbers,
    send a comment [here], giving the number of colours and spaces
    as well as the answer code, and I'll look into it. Thanks!''')
            else:
                playing = False

        playing, awardedBlack, awardedWhite = ask_for_feedback_knuth(END, colours, stdout, nSpaces)
        print(guess)
        S = kill_impossibles_knuth(END, S, guess, awardedBlack, awardedWhite)

        guess = choose_guess_knuth(S, intelligence, stdout)

        go += 1

    post_game_knuth(END, highlights, go)


def ask_for_feedback_knuth(END, colours, stdout, nSpaces):
    """
    Asks the user for the feedback on the latest guess in the form of two variables:
    black pin = correct color in the correct space
    white pin = correct color in the wrong space
    returns black pin and white pin in the form of a tuple containing two integers.
    """

    # Gets number of black pegs
    print(f'''
    How many black pegs - correct colour and in the correct space? (0-{nSpaces}){colours["blue"]}''')
    while True:
        try:
            awardedBlack = int(input())
            if nSpaces >= awardedBlack >= 0:
                break
            else:
                raise ValueError()  # goes to except
        except:
            stdout.write("\033[{0};{1}f".format(9, 64))
            stdout.write(f'{colours["red"]}(0-{nSpaces}){END}')
            stdout.write("\033[{0};{1}f".format(10, 0))
            stdout.write("\033[K")
            stdout.write(colours["blue"])

    if awardedBlack == nSpaces:
        return False, awardedBlack, 0

    elif awardedBlack != nSpaces - 1:
        maxW = nSpaces - awardedBlack

        # Gets number of white pegs
        print(f'''{END}
    How many white pegs - correct colour but in the wrong space? (0-{maxW}){colours["blue"]}''')

        while True:
            try:
                awardedWhite = int(input())
                if maxW >= awardedWhite >= 0:
                    return True, awardedBlack, awardedWhite
                else:
                    raise ValueError()  # goes to except
            except:
                stdout.write("\033[{0};{1}f".format(12, 62))
                stdout.write(f'{colours["red"]}(0-{maxW}){END}')
                stdout.write("\033[{0};{1}f".format(13, 0))
                stdout.write("\033[K")
                stdout.write(colours["blue"])

    else:
        awardedWhite = 0
    return True, awardedBlack, awardedWhite


def kill_impossibles_knuth(END, S, guess, awardedBlack, awardedWhite):
    """
    Takes all previous possibles (S), the current guess (guess) and the amount of point assigned (awardedBlack,
    awardedWhite) as input. Returns a list of current possibles.
    """

    print(f'''{END}
    Calculating next guess...

    Estimating time remaining...
    ''')

    # Eliminates all possibles that would not award the same result if they were the answer
    passed = []
    for pos in S:
        if awards(guess, pos) == [awardedBlack, awardedWhite]:
            passed.append(pos)
    return passed[:]


def choose_guess_knuth(S, intelligence, stdout):
    """
    chooses the next best guess based on the amount of options left for the O (worst case scenario) of that guess.
    """
    # The complicated bit
    # Chooses the best next guess

    if (len(S) < 1000 and intelligence != 1) or intelligence == 3:
        scores = {}
        displayP = -1
        startTime = time()
        prevEstimate = 99999999999999999
        length = len(S)
        for posGuess in S:
            responses = {}
            for posAns in S:
                response = tuple(awards(posGuess,
                                        posAns))  # can't use lists as indexes
                try:
                    responses[response] += 1
                except:
                    responses[response] = 1
            scores[posGuess] = max(responses.values())

            # Updates % on screen
            currentP = round((S.index(posGuess) / length) * 100)
            if currentP > displayP:
                displayP = currentP
                stdout.write("\033[{0};{1}f".format(15, 27))
                stdout.write(f'{displayP}%')
                stdout.write("\033[{0};{1}f".format(19, 0))

            # Updates estimated time remaining on screen
            howFarThrough = S.index(posGuess)
            try:
                estimatedRemaining = round(
                    (((time() - startTime) / howFarThrough) *
                     (length - howFarThrough)))
                if estimatedRemaining < prevEstimate:
                    stdout.write("\033[{0};{1}f".format(17, 0))
                    stdout.write("\033[K")
                    stdout.write(
                        f'Estimated {estimatedRemaining} seconds remaining ')
                    stdout.write("\033[{0};{1}f".format(19, 0))
                    prevEstimate = estimatedRemaining
            except ZeroDivisionError:  # doesn't happen first time
                pass

        try:
            best = min(scores.values())
            guess = choice([
                posGuess for posGuess in scores.keys()
                if scores[posGuess] == best
            ])
        except ValueError:
            pass
    else:
        guess = choice(S)
        return guess


def post_game_knuth(END, highlights, go):
    """
    prints the ending message of the program.

    #############
    # POST-GAME #
    #############
    """

    print(f'''{END}{highlights["red"]}                         
      WELCOME TO MASTERMIND  
                             {END}


    Woo hoo! Got it right in just {go} guesses!
    To play again, simply restart the program (reload the page).
    Want to know how it works? Go here:
    https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm''')


# The code written on line 9 to line 571 is written by ThomasS1 with a few revisions by me. (didn't necessarily make it
# better. mainly brought a lot of variables out of the global scope.
# https://repl.it/talk/share/~-Knuths-MASTERMIND-algorithm-in-Python-board-game-~/17435
# https://repl.it/@ThomasS1


def encode(correct, guess):
    """Checks the guess from the user against the answer and returns the following answering sheet:
    - * (n) n = amount of slots the user has chosen.
    legend:
    '-' = character is not contained in the answer
    '0' = character is contained in the answer but not in this spot
    'X' = character is contained in the answer in this exact spot
    """
    output_arr = [''] * len(correct)

    for i, (correct_char, guess_char) in enumerate(zip(correct, guess)):
        output_arr[i] = 'X' if guess_char == correct_char else 'O' if guess_char in correct else '-'

    return ''.join(output_arr)


def safe_int_input(prompt, min_val, max_val):
    """
    ensures the user gives valid input.
    """
    while True:
        user_input = input(prompt)

        try:
            user_input = int(user_input)
        except ValueError:
            continue

        if min_val <= user_input <= max_val:
            return user_input


def play_game():
    """
    plays mastermind where the user has to guess a random code.
    """
    print("Welcome to Mastermind.")
    print("You will need to guess a random code.")
    print("For each guess, you will receive a hint.")
    print(
        "In this hint, X denotes a correct letter, and O a letter in the original string but in a different position.")
    print()

    number_of_letters = safe_int_input("Select a number of possible letters for the code (2-20): ", 2, 20)
    code_length = safe_int_input("Select a length for the code (4-10): ", 4, 10)

    letters = 'ABCDEFGHIJKLMNOPQRST'[:number_of_letters]
    code = ''.join(random.choices(letters, k=code_length))
    guesses = []

    while True:
        print()
        guess = input(f"Enter a guess of length {code_length} ({letters}): ").upper().strip()

        if len(guess) != code_length or any([char not in letters for char in guess]):
            continue
        elif guess == code:
            print(f"\nYour guess {guess} was correct!")
            break
        else:
            guesses.append(f"{len(guesses)+1}: {' '.join(guess)} => {' '.join(encode(code, guess))}")

        for i_guess in guesses:
            print("------------------------------------")
            print(i_guess)
        print("------------------------------------")


# line 576 to 644 are written by a collection of anonymous rosettacode.org community members.
# https://www.rosettacode.org/wiki/Mastermind#Python


def make_statistic_json(project_file):
    """
    makes the empty statistics json file (a library containing libraries that contain the statistical advantage of
    each combination has in that iteration.
    """
    S = list(product('012345', repeat=4))
    S_strings = make_strings(S)
    the_statistics = {'static': {'go': 4},
                      'total': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
                                14: 0}}

    for i in range(15):
        the_statistics[i] = {}
        for code in S_strings:
            the_statistics[i][code] = 1

    with open(project_file, 'a') as json_file:
        json_content = json.dump(the_statistics, json_file, indent=4)


def make_history_file(historic_file):
    void_statistics = {'total': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0,
                                 13: 0, 14: 0},
                       'parts': {}}
    for i in range(20):
        void_statistics['parts'][i] = {'total' : {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                                                  11: 0, 12: 0, 13: 0, 14: 0}, 'history': []}
    with open(historic_file, 'w') as json_file:
        json_content = json.dump(void_statistics, json_file, indent=4)


def play_teach_computer(project_file, historic_file):
    """
    Teach mastermind to the standard computer account 'mastermind', or make your own computer account to teach
    mastermind to.
    """
    nSpaces = 4
    while True:  # explains the game concept to the user.
        confused = input('Hi, I am mastermind. I want to be the best code breaker in the game that shares my name. \nI '
                        'Please help me become a better code breaker my letting me practice against you! \nPlease make '
                        'a random code out of the following six colors: [yellow, red, green, blue, cyan, purple]'
                        '\nYou are allowed to use a color more than once, so remember, the order matters!\n'
                        'confused? (Y/N)\n').upper()
        if not (confused == 'Y' or confused == 'N'):
            pass
        elif confused == 'Y':
            print('Make a random code out of the six colors [yellow, red, green, blue, cyan, purple], for example: (yellow, red, red, blue). I will try to guess the')
        elif confused == 'N':
            break
        else:
            print('Something broke! if this keeps happening, restart the program. If the problem persists, re-pull the '
                  'code from the source.')
    while True:  # explains the game concept to the user
        confused = input('I am now going to give you a series of guesses of your code.\nYou must rate my guesses with '
                         'the following system:\nFor every correct colour in the correct position, award me a black '
                         'peg.\nFor every correct colour in the wrong position, award me a white peg.\nIf there are '
                         'multiple of the same colour in my guess,\nonly award me pegs for how many there are in the '
                         'answer. \nconfused? (Y/N)\n').upper()
        if not (confused == 'Y' or confused == 'N'):
            pass
        elif confused == 'Y':
            if webbrowser.open("http://www.boardgamecapital.com/game_rules/mastermind.pdf") == False:
                print('Sorry - tried to open the rules automagically but failed. \nYou will have to manually copy this '
                      'link into a new tab! \nhttp://www.boardgamecapital.com/game_rules/mastermind.pdf \nPress enter '
                      'to return to the help page.')
                input()
        elif confused == 'N':
            break
        else:
            print('Something broke! if this keeps happening, restart the program. If the problem persists, re-pull the '
                  'code from the source.')

    while True:  # explains what game modes are available and asks the user which game more he wants to play.
        mode = input('You have three ways to play. \nDo you want to play against my currently best found strategy? \nDo'
                     ' you want to help me get better by playing against new strategies?\nDo you want to play against '
                     'completely random guesses so I can grow my reference of knowaledge for future strategies? '
                     '\nBest, new or random? (B/N/R)\n').upper()
        if not (mode == 'B' or mode == 'N' or mode == 'R'):
            pass
        else:  # starts the program in the selected game mode.
            play_strategy(project_file, historic_file, mode)
            break



def play_strategy(project_file, historic_file, mode):
    """
    takes the file with statistics and the strategy the user chose (mode) as input.
    Plays the game.
    The computer guesses for a code the user came up with with with the chosen strategy.
    The guesses are based on the statistics of earlier played games, or completely random in case of strategy 'R'.
    """

    print('Make a random code out of the six colors [yellow, red, green, blue, cyan, purple]')
    input()  # waits until the user is ready

    with open(project_file, 'r') as json_file:
        data = json.load(json_file)
    playing = True
    colors = ['yellow', 'red', 'green', 'blue', 'cyan', 'purple']

    S_original = list(product('012345', repeat=4))
    S = S_original[:]

    go = 0
    library_temp = {}

    while playing:  # fetches the next combination code based on the chosen game mode
        S_strings = make_strings(S)  # converts the currently available combinations into strings.
        if mode == 'B':
            code = get_best(S_strings, data, go)
        elif mode == 'N':
            code = get_good(S_strings, data, go)
        elif mode == 'R':
            code = get_random(S_strings)
        else:
            print('Something broke! if this keeps happening, restart the program. If the problem persists, re-pull the '
                  'code from the source.')
        guess_print = get_colors(colors, code)  # converts the combination into a list with the corresponding colors.
        print('There are', len(S_strings), 'possibilities. \nMy guess is', guess_print)

        if len(S_strings) == 0:  # stops the program if there are no more combinations available
            print('Current number of possibilities: 0\nOh dear, there aren\'t any possibilities left! \nNot meaning to '
                  'be cocky, but you must have gone wrong! \nPlease restart the program to try again.')

            quit()
        if len(S_strings) == 1:  # stops the program if there is only one combination available.
            print('Current number of possibilities: 1\nAnswer:', guess_print, '\nCorrect? (Y/N)')
            while True:
                correct = input().upper()
                if not(correct == 'Y' or correct == 'N'):
                    pass
                elif correct == 'Y':
                    playing = False
                    break
                elif correct == 'N':
                    print('DOH! Sorry to disappoint...')

                    quit()
                else:
                    print('Something broke! if this keeps happening, restart the program. If the problem persists, '
                          're-pull the code from the source.')
        if playing:  # awards black and white pins to the combination guess. stops the program if four black
            playing, awardedBlack, awardedWhite = ask_for_feedback()                      # pins are awarded

            guess = []

            for i in code:  # converts the combination code into a tuple for the next function.
                guess.append(i)

            S = kill_impossibles(S, guess, awardedBlack, awardedWhite)  # eliminates all combinations that are no longer
                                                                        # possible.
            library_temp = gather_statistics(library_temp, go, code)    # collects all guesses for statistics.

            go += 1
    post_game(project_file, historic_file, library_temp, go)


def gather_statistics(library_temp, i, code):
    """
    takes the a library with current guesses with their corresponding iteration library_temp) as input. Adds current
    code and iteration to the library. Returns the library.
    """
    library_temp[i] = code
    return library_temp


def get_best(S, data, go):
    """
    takes the available combinations (S), the statistics (data) and the iteration the game is in (go) as input.
    returns the best guess the computer can make based on the statistics of previously played games.
    """
    best_starter = ''
    best_starting_index = 0
    for code in S:                                         # loops for every possible combination
        starting_index = 1 / len(S) * data[str(go)][code]  # calculates the probability of a combination
        if starting_index > best_starting_index:           # replaces the best found combination if the new combination
            best_starter = code                            # his probability is higher than the last highest probability
            best_starting_index = starting_index           # found. updates highest probability found.
    return best_starter                                    # returns the combination with the highest probability found.


def get_good(S, data, go):
    """
    takes the available combinations (S), the statistics (data) and the iteration the game is in (go) as input.
    returns a reasonable guess the computer can make based on the statistics of previously played games.
    """
    best_starters = []
    best_starting_index = 0
    for code in S:                                          # loops for every possible combination
        starting_index = 1 / len(S) * data[str(go)][code]   # calculates the probability of a combination
        if starting_index > best_starting_index:            # adds a best found combination to best combination list if
            best_starters.append(code)                      # the new combination his probability is higher than the
            best_starting_index = starting_index            # last highest probability found. updates highest
                                                            # probability found.
    return best_starters[random.randrange(len(best_starters) // 2, len(best_starters))]
    # returns a random item of the latter half of the list with best starter combination.


def get_random(S):
    """
    returns a random guess. Function is used to gather more random data for more robust statistics.
    """
    if len(S) < 1:  # unbreaks the function when the list is too small for indexing
        return S
    return S[random.randrange(0, len(S))]   # returns a random element of the list.


def get_colors(colors, code):
    """
    takes a list of colors (colors) and a string that contains a numbered combination (code) as input. Each number
    represents the color on the matching index of the list. returns the colors contained in the code in a list.
    """
    list_colors = []
    for i in code:                          # repeats for every char in the combination code
        list_colors.append(colors[int(i)])  # adds the color corresponding to the char in the code to the list.
    return list_colors                      # returns the list with colors.


def make_strings(S_old):
    """
    takes a list containing tuples that contain integers. returns a list with strings consisting of the integers.
    """
    S = []  # resulting list

    for i in S_old:  # repeats for each element in S_old
        code = ''    # resulting string
        for j in i:  # repeats for each char in the element.
            code += str(j)  # adds each char to the resulting string.
        S.append(code)      # adds resulting string to resulting list

    return S


def change_statistics(data, library_temp, coefficient):
    """
    takes statistical probability data (data), a library of codes in a certain iteration (library_temp) and the
    coefficient in which the statistical likelihood of the code in that iteration changes (coefficient) as input.
    changes tha statistical probibility of the codes in certain iterations contained in the library.
    """
    for i, code in library_temp.items():
        data[str(i)][code] += coefficient
    return data


def ask_for_feedback():
    """
    Asks the user for the feedback on the latest guess in the form of two variables:
    black pin = correct color in the correct space
    white pin = correct color in the wrong space
    returns black pin and white pin in the form of a tuple containing two integers.
    """

    # Gets number of black pegs
    print(f'''
    How many black pegs - correct colour and in the correct space? (0-4)''')
    while True:  # loops until valid input (1 - 4) is given.
        try:
            awardedBlack = int(input())
            if 4 >= awardedBlack >= 0:
                break
            else:
                raise ValueError()  # goes to except
        except:
            pass

    if awardedBlack == 4:  # stops the program if the code combination is correct.
        return False, awardedBlack, 0

    elif awardedBlack != 4 - 1:  # calculates max amount of white pins
        maxW = 4 - awardedBlack

        # Gets number of white pegs
        print(f'''
    How many white pegs - correct colour but in the wrong space? (0-{maxW})''')

        while True:  # loops until valid input is given.
            try:
                awardedWhite = int(input())
                if maxW >= awardedWhite >= 0:
                    return True, awardedBlack, awardedWhite
                else:
                    raise ValueError()  # goes to except
            except:
                pass

    else:
        awardedWhite = 0
    return True, awardedBlack, awardedWhite


def kill_impossibles(S, guess, awardedBlack, awardedWhite):
    """
    Takes all previous possibles (S), the current guess (guess) and the amount of point assigned (awardedBlack,
    awardedWhite) as input. Returns a list of current possibles.
    """

    print(f'''
    Calculating next guess...

    Estimating time remaining...
    ''')
    # Eliminates all possibles that would not award the same result if they were the answer
    passed = []
    for pos in S:
        if awards(guess, pos) == [awardedBlack, awardedWhite]:
            passed.append(pos)
    return passed[:]

# the code on line 894 to 958 is written by ThomasS1 with a few revisions by me.
# https://repl.it/talk/share/~-Knuths-MASTERMIND-algorithm-in-Python-board-game-~/17435
# https://repl.it/@ThomasS1

def post_game(project_file, historic_file, library_temp, go):
    """
    takes the file of the probability data (project_file), a library with codes with their iteration (library_temp)
    and the total number of iterations (go) as input.  Prints victory message. Changes the probability data of the codes
    in their iterations in the file.
    """
    print(f'''Woo hoo! Got it right in just {go} guesses!\n\nediting program... \n\n...\n\nexiting program...''')
    with open(project_file, 'r') as json_file:   # reads the current information in the 'history' file as to not lose
        data = json.load(json_file)              # it when the new information is added.
    modus = data['static']['go']
    if go > modus + 6:               # calculates the probability factor of each guess based on how many guesses it took
        coefficient = - 0.03         # to get the answer
    elif go >= modus + 3:
        coefficient = - 0.01
    elif go < modus + 3 and go > modus:
        coefficient = - 0.005
    elif go == modus:
        coefficient = 0.02
    elif go < modus and go > 2:
        coefficient = 0.035
    elif go <= 2:
        coefficient = 0.05
    data = change_statistics(data, library_temp, coefficient)  # changes the probability factors of all the guess
    data['total'][str(go)] += 1
    with open(project_file, 'w') as json_file:                 # combinations and writes the new factors to the external
        json_content = json.dump(data, json_file, indent=4)    # 'statistics' file.

    with open(historic_file, 'r') as json_file:                # reads the current information in the 'history' file as
        data_statistics = json.load(json_file)                 # to not lose it when the new information is added.

    data_statistics['total'][str(go)] += 1

    valid = False
    part = None
    if not valid:  # finds a part in the 'history' file that is not yet full. (has no more than 10.000 games in it's
        for i in range(20):                                                                              # history).
            if len(data_statistics['parts'][str(i)]) < 10000:
                valid = True
                part = str(i)
                break

    data_statistics['parts'][part]['total'][str(go)] += 1       # adds currently played game to the total scoreboard
    data_statistics['parts'][part]['history'].append(library_temp)           # adds currently played game to history
    with open(historic_file, 'w') as json_file:  # records the guess combinations of this game in the 'history' file.
        json_content = json.dump(data_statistics, json_file, indent=4)


def play_teach_mastermind_quickly(project_file, historic_file, iterations):
    """plays the computer against itself in a game of mastermind in the random mode in order to gather statistics for a
    robust foundation for the computer to make its assumptions on."""
    for i in range(iterations):
        play_strategy_quickly(project_file, historic_file)

def play_strategy_quickly(project_file, historic_file):
    """
    takes the file with statistics as input.
    Plays the game in random mode. The game is playing by the computer on both ends.
    The computer guesses for a code the user came up with with with the chosen strategy.
    The guesses are based on the statistics of earlier played games, or completely random in case of strategy 'R'.
    this function is used to gather a lot of statistics by making the computer play itself.
    """

    with open(project_file, 'r') as json_file:  # reads the file with the statistics for guesses.
        data = json.load(json_file)
    playing = True
    colors = ['yellow', 'red', 'green', 'blue', 'cyan', 'purple']

    S_original = list(product('012345', repeat=4))
    S = S_original[:]
    S_strings = make_strings(S)

    answer = get_random(S_strings)  # generates a random answer key
    print(answer)
    go = 0
    library_temp = {}

    while playing:  # plays the game
        S_strings = make_strings(S)   # makes a string-copy of the available combinations
        code = get_random(S_strings)  # fetches a random combination out of the available combinations
        guess_print = get_colors(colors, code)  # converts combination code to colours and puts them in a list.
        print('There are', len(S_strings), 'possibilities. \nMy guess is', guess_print)

        if len(S_strings) == 0:  # stops the program if there are no more combinations available
            print('Current number of possibilities: 0\nOh dear, there aren\'t any possibilities left! \nNot meaning to '
                  'be cocky, but you must have gone wrong! \nPlease restart the program to try again.')

            quit()
        if len(S_strings) == 1:  # stops the program if there is only one combination available.
            print('Current number of possibilities: 1\nAnswer:', guess_print, '\nCorrect? (Y/N)')
            while True:
                if code == answer:
                    playing = False
                    break
                else:
                    print('DOH! Sorry to disappoint...')
                    quit()
        if playing:    # awards black and white pins to the combination guess. stops the program if four black
            playing, awardedBlack, awardedWhite = ask_for_feedback_quickly(code, answer)    # pins are awarded

            guess = []

            for i in code:  # converts the combination code into a tuple for the next function.
                guess.append(i)

            S = kill_impossibles(S, guess, awardedBlack, awardedWhite)  # eliminates all combinations that are no longer
                                                                        # possible.
            library_temp = gather_statistics(library_temp, go, code)    # collects all guesses for statistics.

            go += 1
    post_game(project_file, historic_file, library_temp, go)


def ask_for_feedback_quickly(code, answer):
    """
    Asks the computer for the feedback on the latest guess in the form of two variables:
    black pin = correct color in the correct space
    white pin = correct color in the wrong space
    returns black pin and white pin in the form of a tuple containing two integers.
    this function is used to gather a lot of statistics by making the computer play itself.
    """

    # Gets number of black pegs
    print(f'''
    How many black pegs - correct colour and in the correct space? (0-4)''')

    awardedBlack, code, answer = give_black_pins(code, answer)  # computer calculates the amount of awarded black pins to the
                                                          # code combination with the answer key.

    if awardedBlack == 4:  # stops the program if the code combination is correct.
        return False, awardedBlack, 0

    elif awardedBlack != 4 - 1:  # calculates max amount of white pins
        maxW = 4 - awardedBlack

        # Gets number of white pegs
        print(f'''
    How many white pegs - correct colour but in the wrong space? (0-{maxW})''')

        awardedWhite = give_white_pins(code, answer)  # computer calculates the amount of awarded black pins to the code
                                                      # combination with the answer key.
    else:
        awardedWhite = 0

    return True, awardedBlack, awardedWhite


def give_black_pins(code, answer):
    """
    takes the guess of a code (code) and the answer key (answer) as input. calculates the amount of black
    pins the guess (code) gets with the answer key. returns the amount of black pins and the answer key without the
    correctly guessed pins.
    """
    awardedBlack = 0
    for i in range(4):                      # compares each char in the guess to the answer key on the same index.
        if code[i] == answer[i]:
            awardedBlack += 1               # adds a black pin if the chars are identical.
            if i == 3:
                answer = answer[:-1] + 'X'  # removes the color from the answer sheet so it cannot
                code = code[:-1] + 'O'
            else:                           # accidentally flag a white pin.
                answer = answer[:i] + 'X' + answer[i + 1:]
                code = code[:i] + 'O' + code[i + 1:]
    print(awardedBlack, answer)
    return awardedBlack, code, answer


def give_white_pins(code, answer):
    """
    takes the guess of a code (code) and the answer key (answer) as input. calculates the amount of white
    pins the guess (code) gets with the answer key. returns the amount of white pins.
    """
    awardedWhite = 0
    for i in range(4):              # compares each char in the guess to the answer key on the same index.
        if code[i] != answer[i]:    # line 1117 to 1125 are run if the code index is not identical to the answer index
            if code[i] in answer:   # adds a white pin if the color on the code index is in the answer key.
                awardedWhite += 1
                ans_index = answer.find(code[i])
                if ans_index == len(answer) - 1:       # removes the used color in the answer key so it cannot
                    answer = answer[:-1] + 'X'         # accidentally flag another guessed color.
                else:
                    answer = answer[0:ans_index] + 'X' + answer[ans_index + 1:]
    print(awardedWhite, answer)
    return awardedWhite


def play_portal(project_file, historic_file):
    """
    displays the game mode options for users to chose what game mode they want to play.
    """
    while True:
        root = input(
            '\n\nHi, and welcome to Mastermind!\n There are three different game modes available. \nDo you want to '
            'guess a code the computer generated?\nDo you want to come up with a code for the computer to crack?\nDo '
            'you want to teach our algorithm \'mastermind\' the best code-breaking strategy by playing against him?\n'
            'guess, create or teach? (G/C/T)\nenter exit if you want to leave the program\nEnter stat if you want to '
            'gather statistics for \'mastermind\'\n').upper()
        if not (root == 'G' or root == 'C' or root == 'T' or root == 'EXIT' or root == 'STAT'):  # un-breaks the program
            pass                                                                                 # if invalid input is
        if root == 'G':                                                                          # given.
            play_game()     # plays the standard mastermind game where you guess a code the computer generates
        elif root == 'C':
            play_knuth()    # plays mastermind where the computer guesses your code according to knuth's strategy.
        elif root == 'T':
            play_teach_computer(project_file, historic_file)  # plays mastermind where the computer guesses your code
        elif root == 'STAT':                                  # according to what guess has the statistical advantage
            play_teach_mastermind_quickly(project_file, historic_file, 1000)  # according to his earlier played games.
        elif root == 'EXIT':
            quit()
        else:
            print(
                'Something broke! if this keeps happening, restart the program. If the problem persists, re-pull the '
                'code from the source.')


the_statistic_file = 'statistics'
historic_file = 'history'


if __name__ == '__main__':
    play_portal(the_statistic_file, historic_file)

