# could use interface? PySimpleGUI; tkinter
# does not handle special characters as of now
# todo: let user input their list of letters in their order

def caesar_cipher_shift(shift_num):
    # Returns keyed dictionary
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    shifted_letters = dict()
    for i in range (len(letters)):
        shifted_letters[letters[i]] = letters[(i + shift_num) % len(letters)]
    return shifted_letters

def caesar_cipher_encode(msg, key):
    coded_msg = ""
    for letter in msg:
        coded_msg += key.get(letter, letter)
    return coded_msg

if __name__ == "__main__":
    process = input("Do you want to encode or decode your message? ").lower()
    msg = input("Type you message: ")
    shift_num = int(input("Enter key: "))
    if (process == "decode"):
        shift_num *= -1
    key_dict = caesar_cipher_shift(shift_num)
    output = caesar_cipher_encode(msg, key_dict)
    print(output)