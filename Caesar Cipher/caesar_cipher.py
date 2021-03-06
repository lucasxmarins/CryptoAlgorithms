# Program Cesar Cipher - Python
# Author: Lucas Xavier Marins
# GitHub Profile: https://github.com/lucasxmarins
# Data: 30/05/2020
#
# Description: In cryptography, a Caesar cipher, also known as Caesar's cipher, the shift cipher, Caesar's code or
# Caesar shift, is one of the simplest and most widely known encryption techniques. It is a type of substitution cipher
# in which each letter in the plaintext is replaced by a letter some fixed number of positions down the alphabet.
# For example, with a left shift of 3, D would be replaced by A, E would become B, and so on. The method is named after
# Julius Caesar, who used it in his private correspondence.
#
# Text used as base for program's algorithm at (pt/br): http://wiki.stoa.usp.br/images/c/cf/Stallings-cap2e3.pdf
# **********************************************************************************************************************

from collections import deque


def cesar_cipher(clear_text, key, mode='e'):
    """
    This function takes a key text to be encrypted, an integer key to encrypt and a string mode
    to set the mode to encryption or decryption and outputs the original text encrypted
    """
    if mode == 'e':
        cod = -1
    elif mode == 'd':
        cod = 1
    else:
        raise ValueError

    clear_text.lower()
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    alpha_deq = deque(alpha)
    alpha_deq.rotate(key * cod)

    cypher_lst = []
    for letter in clear_text:
        if letter in alpha:
            cypher_lst.append(str.index(alpha, letter))
        elif letter == ' ':
            cypher_lst.append(' ')
        else:
            cypher_lst.append('#')

    cipher_text = ''
    for i in cypher_lst:
        if i == ' ' or i == '#':
            cipher_text += i
        else:
            cipher_text += alpha_deq[i]

    return cipher_text


def main():
    """
    Main function that receives user input and passes it to cesarcipher( )
    """
    while True:
        print('CESAR CIPHER PROGRAM\n')

        while True:
            try:
                mode_tb = ['0', 'e', 'd']
                mode = str(input('Which mode: e -> Encryption / d -> Decryption | 0 -> Exit the program >> ')).lower()
                if mode not in mode_tb:
                    raise ValueError
                break
            except ValueError:
                print('Invalid command!!!')

        if mode == '0':
            break

        while True:
            try:
                text = str(input('Enter text: '))
                key = int(input('Enter key: '))
                break
            except ValueError:
                print('Invalid enter. Only alphabetic characters available for text and integers for key!!!')

        print(f'R: {cesar_cipher(text, key, mode)}')

    print('Program closed!')


if __name__ == "__main__":
    main()
