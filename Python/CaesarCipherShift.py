# could use interface?
# does not handle special characters

def caesar_cipher_shift(shift_direction, shift_num):
    # Returns dictionary
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    shifted_letters = dict()
    for i in range (len(letters)):
        if (shift_direction == "right"):
            shifted_letters[letters[i]] = letters[(i + shift_num) % len(letters)]
        else:
            shifted_letters[letters[i]] = letters[(26 + i - shift_num) % len(letters)]
    return shifted_letters


def caesar_cipher_encode(msg, key):
    coded_msg = ""
    for letter in msg:
        if (letter.isalpha()):
            coded_msg += key[letter]
        else:
            coded_msg += letter
    return coded_msg

def caesar_cipher_decode(coded_msg, key):
    decoded_msg = ""
    for letter in coded_msg:
        if (letter.isalpha()):
            char = list(key.keys())[list(key.values()).index(letter)] # what is this doing???
            decoded_msg += char
        else:
            decoded_msg += letter
    return decoded_msg

if __name__ == "__main__":
    process = input("Do you want to encode or decode your message? ").lower()
    msg = input("Type you message: ")
    shift_direction = input("Enter Caeser shift direction (right/left): ").lower()
    shift_num = int(input("Enter number of places to shift by: "))
    key = caesar_cipher_shift(shift_direction, shift_num)
    if (process == "encode"):
        output = caesar_cipher_encode(msg, key)
    else:
        output = caesar_cipher_decode(msg, key)
    print(output)
