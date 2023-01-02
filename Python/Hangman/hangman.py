import random
import string
 
WORDLIST_FILENAME = "words.txt"
 
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")

    # next two lines fix incorrect working directory...don't know which directory when debugging?
    # should not need if working directory = folder w/ hangman.py and words.txt
    # print(os.getcwd())
    # path = os.getcwd() + "\\" + WORDLIST_FILENAME

    # make sure working directory contains both files -> FileNotFoundError...else use code above to get to correct directory
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist
 
 
 
def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)
 
 
# Load the list of words into the variable wordlist to enable access from anywhere in the program
wordlist = load_words()
# ------------- end of helper code
 
def is_word_guessed(secret_word, letters_guessed):
    """
    Determines whether the wodchosen has been guessed by the player.
    Returns True if yes, returns False otherwise.
    """
    for char in secret_word:
        if (char not in letters_guessed) :
            return False
    return True
 
 
 
def get_guessed_word(secret_word, letters_guessed):
    """
    Arranges the correctly guessed letters as present in the word chosen
    and returns string.
    Represents letters that have not beem guessed yet with an underscore
    followed by a space.
    """
    guessed_word = ''
    for char in secret_word:
        if char in letters_guessed :
            guessed_word += char
        else :
            guessed_word += '_ '
    return guessed_word
 
 
 
def get_available_letters(letters_guessed):
    """
    Returns all the letters that haven't been guessed yet.
    """
    available_letters = ''
    for char in string.ascii_lowercase:
        if not (char in letters_guessed) :
            available_letters += char + ' '
    return available_letters
    
    

def hangman(secret_word):
    """
    Takes care of the game, turns, warnings, etc.
    Interracts with player and gives immediate feedback 
    regarding player's guess.
    """
    # Welcome player, explain basic rules and initialize local variables
    print ("Welcome to the game Hangman!")
    print ("I am thinking of a word that is" , len(secret_word) , "letters long")
    print ("You have 3 warnings. You will lose a warning when your guess is not a letter or if you repeat your guess. When you run out of warnings, you will lose a guess. ")
    print ("-------------")
    guess = ''
    warnings = 3
    guesses = 6
    score = 0
    letters_guessed = []
    vowels = "aeiou"
    while (guesses > 0) :
        g = "guesses"
        w = "warnings"
        print ("You have" , guesses , "guesses left.")
        print ("Available letters : " + get_available_letters(letters_guessed))
        guess = input("Please guess a letter : ").lower()
        # Checking if guess is an alphabet
        if not(guess.isalpha()) :
            if (warnings > 0) :
                warnings -= 1
                print ("Oops! That is not a valid letter. You have" , warnings, grm_error_correct(w, warnings), "left:", get_guessed_word(secret_word,letters_guessed))
            else :
                guesses -= 1
                print("Oops! That is not a valid letter. You have", guesses, grm_error_correct(g, guesses), "left:", get_guessed_word(secret_word,letters_guessed))
            continue
        # Checking if guess is being repeated 
        if (guess in letters_guessed) :
            if (warnings > 0) :
                warnings -= 1
                print ("Oops! You've already guessed that letter. You have" , warnings, grm_error_correct(w, warnings), "left:", get_guessed_word(secret_word,letters_guessed))
            else :
                guesses -= 1
                print("Oops! You've already guessed that letter. You have", guesses, grm_error_correct(g, guesses), "left:", get_guessed_word(secret_word,letters_guessed))
            continue
        letters_guessed += guess
        # Checking if guess is in secret_word
        if (guess in secret_word) :
            print ("Good guess : " + get_guessed_word(secret_word, letters_guessed))
            score += 1
        else :
            print ("Oops! That letter is not in my word : " + get_guessed_word(secret_word, letters_guessed))
            if (guess not in vowels) :
                guesses -= 1
            else :
                guesses -= 2
        print ()
        print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print ()
        # Checking if word is guessed
        if (is_word_guessed(secret_word, letters_guessed)) :
            print ("Congratulations, you won!")
            max_score = 6*score
            print ("Your total score for this game is :", guesses*score, "/", max_score)
            break
    if not(is_word_guessed(secret_word, letters_guessed)) :
        print ("Sorry, you ran out of guesses. The word was " + secret_word)
    
 
 
 
def match_with_gaps(my_word, other_word):
    """
    Takes input : 
    my_word --> player's guess so far
    other_word--> a normal English word with no underscores
    
    Checks if 2 given words have their letters arranged in the same order
    while ignoring the underscores in my_word. If they are arranged similarly
    returns True and False otherwise.
    
    Addition :Returns false for English words with letters the player has already guessed in place of
    underscores in my_word.
    """
    my_word = my_word.replace(" ","")
    if (len(my_word) != len(other_word)) :
        return False
    for i in range (len(my_word)) :
        if (my_word[i].isalpha()) and (my_word[i] != other_word[i]) :
            return False
        elif (not(my_word[i].isalpha()) and other_word[i] in letters_guessed) :
            return False
    return True
 
 
 
def show_possible_matches(my_word):
    """
    Prints all words in wordlist that match with my_word.
    """
    check = 0
    for x in wordlist :
        if (match_with_gaps(my_word, x)) :
            check += 1
            if (check == 1) :
                print ("Possible word matches are : ")
            print (x, end = ' ')
    print ()
    if (check == 0) :
        print ("No matches found.")
 
 
 
def grm_error_correct(word, value) :
    """
    Corrects grammatical errors such as 1 warnings and 1 guesses.
    """
    if (value == 1) :
        if (word[0] == "w") :
            return (word[:-1])
        else :
            return (word[:-2])
    else :
        return word
 
 
 
def hangman_with_hints(secret_word, letters_guessed):
    """
    Works the same as the hangman function. Also provides hints to player when asked.
    Hints --> Provides hints with functions match_with_gaps and show_possible_matches.
    """
    # Welcome player, explain basic rules and initialize local variables
    print ("Welcome to the game Hangman!")
    print ("I am thinking of a word that is" , len(secret_word) , "letters long")
    print ("You have 3 warnings. You will lose a warning when your guess is not a letter or")
    print ("if you repeat your guess. When you run out of warnings, you will lose a guess. ")
    print ("If you want a list of words that match with the letters you have guessed, enter '*' as your guess")
    print ("Your final score for the game is based on the number of guesses you use")
    print ("-------------")
    guess = ''
    warnings = 3
    guesses = 6
    score = 0
    vowels = "aeiou"
    g = "guesses"
    w = "warnings"
    while (guesses > 0) :
        print ("You have" , guesses , grm_error_correct(g, guesses), "left.")
        print ("Available letters : " + get_available_letters(letters_guessed))
        guess = input("Please guess a letter : ").lower()
        # Checking if guess is an alphabet
        if (guess == "*") :
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue
        if not(guess.isalpha()) :
            if (warnings > 0) :
                warnings -= 1
                print ("Oops! That is not a valid letter. You have" , warnings, grm_error_correct(w, warnings), "left:", get_guessed_word(secret_word,letters_guessed))
            else :
                guesses -= 1
                print("Oops! That is not a valid letter. You have", guesses, grm_error_correct(g, guesses), "left:", get_guessed_word(secret_word,letters_guessed))
            continue
        # Checking if guess is being repeated 
        if (guess in letters_guessed) :
            if (warnings > 0) :
                warnings -= 1
                if (warnings == 1) :
                    w = "warning"
                print ("Oops! You've already guessed that letter. You have" , warnings, grm_error_correct(w,warnings), "left:", get_guessed_word(secret_word,letters_guessed))
            else :
                guesses -= 1
                print("Oops! You've already guessed that letter. You have", guesses, grm_error_correct(g, guesses), "left:", get_guessed_word(secret_word,letters_guessed))
            continue
        letters_guessed += guess
        # Checking if guess is in secret_word
        if (guess in secret_word) :
            print ("Good guess : " + get_guessed_word(secret_word, letters_guessed))
            score += 1
        else :
            print ("Oops! That letter is not in my word : " + get_guessed_word(secret_word, letters_guessed))
            if (guess not in vowels) :
                guesses -= 1
            else :
                guesses -= 2
        print ()
        print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print ()
        # Checking if word is guessed
        if (is_word_guessed(secret_word, letters_guessed)) :
            print ("Congratulations, you won!")
            maxScore = 6*score
            print ("Your total score for this game is :", guesses*score, "/", maxScore)
            break
    if not(is_word_guessed(secret_word, letters_guessed)) :
        print ("Sorry, you ran out of guesses. The word was " + secret_word)

if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    # hangman(secret_word)
    letters_guessed = []
    hangman_with_hints(secret_word, letters_guessed)