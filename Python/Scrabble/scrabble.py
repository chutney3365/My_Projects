# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played
    """
    score = 0
    for letter in word.lower():
        score += SCRABBLE_LETTER_VALUES.get(letter, 0)
    score *= max(1, 7 * len(word) - 3 * (n - len(word)))
    return score


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.
    """
    print("Current hand: ", end="")
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    hand['*'] = 1

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.
    """

    updated_hand = hand.copy()
    for letter in word.lower():
        if (updated_hand.get(letter, 0) != 0):
            updated_hand[letter] = updated_hand[letter] - 1
    return updated_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    """
    if (word.find('*') != -1):
        index = word.find('*')
        match = False
        for vowel in VOWELS:
            maybe_word = word[:index] + vowel + word[index + 1:]
            if (maybe_word.lower() in word_list):
                match = True
        if (match == False):
            return False
    elif (word.lower() not in word_list):
        return False
    word_freq_list = get_frequency_dict(word.lower())
    for letter in word_freq_list:
        if (word_freq_list.get(letter) > hand.get(letter, 0)):
            return False
    return True

def calculate_handlen(hand):
    length = 0
    for letter in hand:
        length += hand.get(letter)
    return length

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
    """
    score = 0
    while (calculate_handlen(hand) > 0):
        display_hand(hand)
        word = input("Enter word, or \"!!\" to indicate that you are finished: ")
        if (word == "!!"):        
            break
        else:
            if (is_valid_word(word, hand, word_list)):
                points_earned = get_word_score(word, calculate_handlen(hand))
                score += points_earned
                print("\"" + word + "\" earned " , points_earned , " points. ", sep="", end="")
                print("Total: " , score , " points", sep="")
            else:
                print("That is not a valid word. Please choose another word.")
            hand = update_hand(hand, word)
    print("Total score:", score)
    return score

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    """
    if (letter not in hand.keys()):
        return hand
    substituted_hand = hand
    letters = VOWELS + CONSONANTS
    for char in hand:
        letters = letters.replace(char, '')
    sub_letter = random.choice(letters)
    substituted_hand[sub_letter] = substituted_hand[letter]
    del substituted_hand[letter]
    return substituted_hand

    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands
    """
    num_hands = int(input("Enter total number of hands: "))
    substituted = False
    replayed = False
    total_score = 0
    for i in range (num_hands):
        hand = deal_hand(HAND_SIZE)
        display_hand(hand)
        if (substituted == False):
            substitute = input("Would you like to substitute a letter? ").lower()
            if (substitute == "yes"):
                letter_to_sub = input("Which letter would you like to replace? ").lower()
                substitute_hand(hand, letter_to_sub)
                substituted = True
        hand_score = play_hand(hand, word_list)
        print("-----------------")
        if (replayed == False):
            replay = input("Would you like to replay the hand? ").lower()
            if (replay == "yes"):
                hand_score = max(hand_score, play_hand(hand, word_list))
                replayed = True
        total_score += hand_score
    print("Total score over all hands:", total_score)
    return total_score
    
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
    # to fix: after invalid word..."please choose valid word" and 
    # then total score when letters are over in hand....
    # hand printed twice when not asked about substitution