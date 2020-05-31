# Program Cesar Cipher - Python
# Author: Lucas Xavier Marins
# GitHub Profile: https://github.com/lucasxmarins
# Data: 31/05/2020
#
# Description: In a Caesar cipher, each letter of the alphabet is shifted along some number of places. For example, in a
# Caesar cipher of shift 3, A would become D, B would become E, Y would become B and so on. The Vigenère cipher has
# several Caesar ciphers in sequence with different shift values.
# To encrypt, a table of alphabets can be used, termed a tabula recta, Vigenère square or Vigenère table. It has the
# alphabet written out 26 times in different rows, each alphabet shifted cyclically to the left compared to the previous
# alphabet, corresponding to the 26 possible Caesar ciphers. At different points in the encryption process, the cipher
# uses a different alphabet from one of the rows. The alphabet used at each point depends on a repeating keyword.
#
# Algorithm description (pt/br) at: http://wiki.stoa.usp.br/images/c/cf/Stallings-cap2e3.pdf  
# **********************************************************************************************************************

from string import ascii_uppercase


def vigenere(clear_text, key, mode='e'):
    """
      This function takes a key text to be encrypted, an integer key to encrypt and a string mode
      to set the mode to encryption or decryption and outputs the original text encrypted
      """

    key_lst = list(key.upper().replace(' ', ''))
    text = clear_text.upper().replace(' ', '')

    # Save position of space (' ') characters
    space_pos = [i for i, char in enumerate(clear_text) if char == ' ']

    # Make key the same size as clear text (without spaces)
    for i in range(len(text) - len(key_lst)):
        key_lst.append(key_lst[i])

    # Encrypt/ Decrypt
    cipher_lst = []
    for i, char in enumerate(text):
        if mode == 'e':
            cipher_lst.append(ascii_uppercase[((ord(char) - 65) + (ord(key_lst[i]) - 65)) % 26])
        else:
            cipher_lst.append(ascii_uppercase[(ord(char) - 65) - (ord(key_lst[i]) - 65)])

    # Insert spaces in cipher text
    cipher_text = ''
    count = 0
    for i, char in enumerate(cipher_lst):
        cipher_text += char
        if i + 1 + count in space_pos:
            if i + 1 + count == space_pos[count]:
                cipher_text += ' '
                count += 1

    return cipher_text


def main():
    """
    Main function that receives user input and passes it to vigenere( )
    """

    print('VIGENERE CIPHER PROGRAM\n')

    while True:

        while True:
            try:
                mode_tb = ['0', 'e', 'd']
                mode = str(input('Modes: e -> Encryption / d -> Decryption | 0 -> Exit the program >> ')).lower()
                if mode not in mode_tb:
                    raise ValueError
                break
            except ValueError:
                print('Invalid command!!!')

        # Close program if user inputs 0
        if mode == '0':
            break

        while True:
            try:
                text = str(input('Enter text: '))
                key = str(input('Enter key: '))
                break
            except ValueError:
                print('Invalid enter. Only alphabetic characters available for text and key!!!')

        print(f'R: {vigenere(text, key, mode)}\n')

    print('End of program!')


if __name__ == '__main__':
    main()
