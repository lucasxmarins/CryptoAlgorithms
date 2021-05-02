# Program Playfair Cipher - Python
# Author: Lucas Xavier Marins
# GitHub Profile: https://github.com/lucasxmarins
# Date: 28/05/2020
#
# Description: The Playfair cipher uses a 5 by 5 table containing a key word or phrase.
# To encrypt a message, one would break the message into digrams (groups of 2 letters) such that, for example:
# "HelloWorld" becomes "HE LL OW OR LD". These digrams will be substituted using the key table. Since encryption
# requires pairs of letters, messages with an odd number of characters usually append an uncommon letter, such as "X",
# to complete the final digram. The two letters of the digram are considered opposite corners of a rectangle in the key
# table.
# To perform the substitution, apply the following 4 rules, in order, to each pair of letters in the plaintext:
#
# 1 )If both letters are the same (or only one letter is left), add an "X" after the first letter. Encrypt the new pair
# and continue. Some variants of Playfair use "Q" instead of "X", but any letter, itself uncommon as a repeated pair,
# will do.
# 2) If the letters appear on the same row of your table, replace them with the letters to their immediate right
# respectively (wrapping around to the left side of the row if a letter in the original pair was on the right side of
# the row).
# 3) If the letters appear on the same column of your table, replace them with the letters immediately below
# respectively (wrapping around to the top side of the column if a letter in the original pair was on the bottom side
# of the column).
# 4)If the letters are not on the same row or column, replace them with the letters on the same row respectively but at
# the other pair of corners of the rectangle defined by the original pair. The order is important – the first letter of
# the encrypted pair is the one that lies on the same row as the first letter of the plaintext pair.
# 5) To decrypt, use the inverse (opposite) of the last 3 rules, and the first as-is (dropping any extra "X"s).
#
# Book used as base for program's algorithm (pt/br) : http://wiki.stoa.usp.br/images/c/cf/Stallings-cap2e3.pdf
# **********************************************************************************************************************

from unidecode import unidecode

def getindex(array, item):
    """ This function takes an 2D array and an item of arguments and returns the index of item in array. """

    item_row, item_column = '', ''

    for i, row in enumerate(array):
        for j, array_item in enumerate(row):
            if array_item == item:
                item_row = i
                item_column = j
                break

    return item_row, item_column


def split(array, n):
    """
    This function takes an array of 1 dimension and a integer (n) as arguments
    and returns the array rearranged as an array of size (n x n)
    """
    k, m = divmod(len(array), n)
    return list(array[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(int(n)))


def pf_tablemaker(key_zero):
    """
    This function takes a string key as argument and returns table to be used for encryption
    """
    key = key_zero.upper().replace(' ', '')
    # Playfair cipher uses a version of alphabet in which i and j are counted as the same letter
    pf_alphabet = list('ABCDEFGHIKLMNOPQRSTUVWXYZ')

    # An encryption table is created using the chosen key adding each letter once and excluding letter i
    table = [letter for index, letter in enumerate(key) if letter != 'J' and key.index(letter) == index]
    [table.append(letter) for letter in pf_alphabet if letter not in table]
    pf_table = split(table, 5)

    return pf_table


def playfair_cipher(clear_text, key_zero, mode='e'):
    """
      This function takes a key text to be encrypted, an integer key_zero to encrypt and a string mode
      to set the mode to encryption or decryption and outputs the original text encrypted
      """

    text = unidecode(clear_text).upper().replace(' ', '')

    # Rearrange Text and Cipher Table to Playfair's format
    text = [letter if letter != 'J' else 'I' for letter in text]

    for i, j in enumerate(text):
        if text[i] == text[i - 1] and i % 2 != 0:
            text.insert(i, 'X')

    if len(text) % 2 != 0:
        text.append('X')

    text = split(text, (len(text) // 2))
    cipher_table = pf_tablemaker(key_zero)

    # print(text) # Used to check some errors that may appear at rearrange process

    # Encrypt/Decrypt  the text
    if mode == 'd':
        md = -1
    else:
        md = 1

    crypt_lst = []
    for pair in text:
        # Same Row Case
        if getindex(cipher_table, pair[0])[0] == getindex(cipher_table, pair[1])[0]:
            # For first letter of pair
            x1, y1 = getindex(cipher_table, pair[0])
            # encrypt mode
            if y1 == (len(cipher_table) - 1) and mode == 'e':
                crypt_lst.append(cipher_table[x1][0])

            # Decryption mode
            elif y1 == 0 and mode == 'd':
                crypt_lst.append(cipher_table[x1][-1])
            else:
                crypt_lst.append(cipher_table[x1][y1 + 1 * md])

            # For second letter of pair
            x2, y2 = getindex(cipher_table, pair[1])
            if y2 == (len(cipher_table) - 1) and mode == 'e':
                crypt_lst.append(cipher_table[x2][0])

            elif y2 == 0 and mode == 'd':
                crypt_lst.append(cipher_table[x2][-1])
            else:
                crypt_lst.append(cipher_table[x2][y2 + 1 * md])

        # Same Column Case
        elif getindex(cipher_table, pair[0])[1] == getindex(cipher_table, pair[1])[1]:
            # For first letter of pair
            x1, y1 = getindex(cipher_table, pair[0])

            if x1 == (len(cipher_table) - 1) and mode == 'e':
                crypt_lst.append(cipher_table[0][y1])

            elif x1 == 0 and mode == 'd':
                crypt_lst.append(cipher_table[-1][y1])
            else:
                crypt_lst.append(cipher_table[x1 + 1 * md][y1])

            # For second letter of pair
            x2, y2 = getindex(cipher_table, pair[1])
            if x2 == (len(cipher_table) - 1) and mode == 'e':
                crypt_lst.append(cipher_table[0][y2])
            elif x2 == 0 and mode == 'd':
                crypt_lst.append(cipher_table[-1][y2])
            else:
                crypt_lst.append(cipher_table[x2 + 1 * md][y2])

        # Different Row and column Case
        else:
            x1, y1 = getindex(cipher_table, pair[0])
            x2, y2 = getindex(cipher_table, pair[1])
            # For first letter of pair
            crypt_lst.append(cipher_table[x1][y2])

            # For second letter of pair
            crypt_lst.append(cipher_table[x2][y1])

    # Transform crypt_lst into a string for output
    cipher_text = ''
    for i in range(len(crypt_lst)):
        cipher_text += crypt_lst[i]
        if i % 2 != 0:
            cipher_text += ' '

    return cipher_text


def main():
    """
    Main function that receives user input and passes it to playfair_cipher( )
    """

    print('PLAYFAIR CIPHER PROGRAM')
    while True:

        while True:
            try:
                options = ('e', 'd', 't', 'out')
                print('\nWhich mode would like to use?')
                mode = str(input('Encrypt -> e | Decrypt -> d | t -> show table for key | out -> exit program >> '))
                if mode not in options:
                    raise ValueError
                break
            except ValueError:
                print('Valid commands: Encrypt -> e | Decrypt -> d | t -> Show Crypt Table')

        if mode == 'out':
            break

        # Initializing variable cause it's value assignment is inside if statement
        text = None

        if mode != 't':
            while True:
                try:
                    text = str(input('Text to be encrypted/decrypted: ')).lower()
                    if all(char.isalpha() or char.isspace() for char in text) is False:
                        raise ValueError
                    break
                except ValueError:
                    print('Only alphabetic characters accepted for encryption and key setting!!! ')

        while True:
            try:
                key = str(input('Key to encrypt: '))
                if all(char.isalpha() or char.isspace() for char in key) is False:
                    raise ValueError
                break
            except ValueError:
                print('Only alphabetic characters accepted for encryption and key setting!!! ')

        # Exit program if user enters "out"
        if mode == 'out':
            break

        # Print Encryption table for given key
        elif mode == 't':
            [print(row) for row in pf_tablemaker(key)]
        # Encrypt/Decrypt given text
        else:
            print(f'R: {playfair_cipher(text, key, mode)}')
            print()


if __name__ == '__main__':
    main()
