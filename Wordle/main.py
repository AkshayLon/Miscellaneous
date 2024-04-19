import random
from copy import deepcopy
from shutil import move
from ansi_escapes import ansiEscapes
import sys
from rich_text_codes import *
import time

def process_set():
    with open("words_list.txt", "r") as f:
        data = f.read()
        data_list = data.split("\n")
        return data_list

WORD_SET = process_set()

def get_random_word(word_set):
    index = random.randint(0,len(word_set)-1)
    return word_set[index]

def valid_word(input_string):
    if len(input_string) != 5:
        return "Not a 5-letter word"
    if input_string in WORD_SET:
        return "Valid"
    return "Not a valid word"

def answer_guessed(chosen_word, input_word):
    if chosen_word == input_word:
        return True
    return False

def generate_hint_string(chosen_word, input_word):
    characters_input = [*input_word]
    characters_chosen = [*chosen_word]
    copy_characters_chosen = deepcopy(characters_chosen)
    hint_string = []
    for i in range(5):
        if characters_input[i] == characters_chosen[i]:
            hint_string.append(f"{B_RED}{characters_input[i]}{RESET}")
            copy_characters_chosen.remove(characters_input[i])
            update(B_RED, characters_input[i])
        elif characters_input[i] in copy_characters_chosen:
            hint_string.append(f"{B_CYAN}{characters_input[i]}{RESET}")
            copy_characters_chosen.remove(characters_input[i])
            update(B_CYAN, characters_input[i])
        else:
            hint_string.append(characters_input[i])
            update(B_WHITE, characters_input[i])
    return "".join(hint_string)

def print_output(attempt, to_print):
    sys.stdout.write(ansiEscapes.cursorTo(0,attempt+4))
    print(to_print)
    sys.stdout.write(ansiEscapes.cursorTo(0,12))

def update(colour, letter):
    coordinates = letter_position[letter]
    sys.stdout.write(ansiEscapes.cursorTo(coordinates[0],coordinates[1]))
    print(f"{colour}{letter}{RESET}")

if __name__=="__main__":
    print(f"{BOLD}Welcome to Wordle{RESET}\nKey : {B_RED}Red{RESET} - Correct letter correct place\n      {B_CYAN}Cyan{RESET} - Correct letter wrong place\n\n_____\n_____\n_____\n_____\n_____\n\n")
    sys.stdout.write(ansiEscapes.cursorTo(0,16))
    print("q w e r t y u i o p\na s d f g h j k l\nz x c v b n m")
    sys.stdout.write(ansiEscapes.cursorTo(0,1))
    #chosen_word = get_random_word(word_set=WORD_SET)
    chosen_word = 'black'
    game_won = False
    guesses = []
    for tries in range(5):
        valid_guess = "Not a valid word"
        previously_valid = True
        while valid_guess != "Valid":
            sys.stdout.write(ansiEscapes.cursorTo(0,12) + ansiEscapes.eraseLine)
            guess = input(f"Guess a 5 letter word : ")
            valid_guess = valid_word(input_string=guess)
            if guess in guesses:
                valid_guess = "Word already guessed"
            if valid_guess != "Valid":
                sys.stdout.write(ansiEscapes.eraseLine)
                print(valid_guess)
                previously_valid = False
            else:
                previously_valid = True
                sys.stdout.write(ansiEscapes.cursorNextLine + ansiEscapes.eraseLine + ansiEscapes.cursorPrevLine)
                guesses.append(guess)
        if answer_guessed(chosen_word, guess):
            sys.stdout.write(ansiEscapes.eraseLine)
            print(f"Congrats, you guessed the word : {chosen_word}")
            hint = generate_hint_string(chosen_word, guess)
            print_output(attempt=tries, to_print=hint)
            game_won = True
            break
        else:
            hint = generate_hint_string(chosen_word, guess)
            print_output(attempt=tries, to_print=hint)
    
        
    if not game_won:
        sys.stdout.write(ansiEscapes.eraseLine)
        print("Unfortunately you lost")
        sys.stdout.write(ansiEscapes.eraseLine)
        print(f"Correct word = {chosen_word}")

    time.sleep(10000)
    
