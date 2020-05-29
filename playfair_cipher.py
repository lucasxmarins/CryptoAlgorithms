# Program Playfair Cipher - Python
# Author: Lucas Xavier Marins
# GitHub Profile: https://github.com/lucasxmarins
# Data: 28/05/2020
#
# Description: This program is a encrypter/decrypter for Playfair cipher.
# The technique encrypts pairs of letters, instead of single letters as in the simple substitution cipher and rather
# more complex Vigenère cipher systems then in use. The Playfair is thus significantly harder to break since the
# frequency analysis used for simple substitution ciphers does not work with it. The frequency analysis of bigrams is
# possible, but considerably more difficult. With 600 possible bigrams rather than the 26 possible monograms  (single
# symbols, usually letters in this context), a considerably larger cipher text is required in order to be useful.
#
# More information about the cipher: https://en.wikipedia.org/wiki/Playfair_cipher
# **********************************************************************************************************************


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


def playfair_cipher(text_zero, key_zero, mode='e'):
    """
    This function takes a string text_zero to be encrypted, a string key_zero to create a table or encryption and a mode
    to set the mode on encryption or decryption and outputs a original text encrypted
    """
    text = text_zero.upper().replace(' ', '')

    # Rearrange Text and Cipher Table to Playfair's format
    text = [letter if letter != 'J' else 'I' for letter in text]

    for i, j in enumerate(text):
        if text[i] == text[i - 1] and i % 2 != 0:
            text.insert(i, 'X')
    # Try uncomment section bellow. You'll see range function only provides us a static length. With append()
    # the size of our list is increasing, so range cannot helps us :(
    # for i in range(len(text)):
    #     if text[i] == text[i - 1] and i % 2 != 0:
    #         text.insert(i, 'X')

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

    crypt_text = []
    for pair in text:
        # Same Row Case
        if getindex(cipher_table, pair[0])[0] == getindex(cipher_table, pair[1])[0]:
            # For first letter of pair
            x1, y1 = getindex(cipher_table, pair[0])
            # encrypt mode
            if y1 == (len(cipher_table) - 1) and mode == 'e':
                crypt_text.append(cipher_table[x1][0])
            # elif mode == 'c':
            #    crypt_text.append(cipher_table[x1][y1 + 1])

            # Decryption mode
            elif y1 == 0 and mode == 'd':
                crypt_text.append(cipher_table[x1][-1])
            else:
                crypt_text.append(cipher_table[x1][y1 + 1 * md])

            # For second letter of pair
            x2, y2 = getindex(cipher_table, pair[1])
            if y2 == (len(cipher_table) - 1) and mode == 'e':
                crypt_text.append(cipher_table[x2][0])

            elif y2 == 0 and mode == 'd':
                crypt_text.append(cipher_table[x2][-1])
            else:
                crypt_text.append(cipher_table[x2][y2 + 1 * md])

        # Same Column Case
        elif getindex(cipher_table, pair[0])[1] == getindex(cipher_table, pair[1])[1]:
            # For first letter of pair
            x1, y1 = getindex(cipher_table, pair[0])

            if x1 == (len(cipher_table) - 1) and mode == 'e':
                crypt_text.append(cipher_table[0][y1])

            elif x1 == 0 and mode == 'd':
                crypt_text.append(cipher_table[-1][y1])
            else:
                crypt_text.append(cipher_table[x1 + 1 * md][y1])

            # For second letter of pair
            x2, y2 = getindex(cipher_table, pair[1])
            if x2 == (len(cipher_table) - 1) and mode == 'e':
                crypt_text.append(cipher_table[0][y2])
            elif x2 == 0 and mode == 'd':
                crypt_text.append(cipher_table[-1][y2])
            else:
                crypt_text.append(cipher_table[x2 + 1 * md][y2])

        # Different Row and column Case
        else:
            x1, y1 = getindex(cipher_table, pair[0])
            x2, y2 = getindex(cipher_table, pair[1])
            # For first letter of pair
            crypt_text.append(cipher_table[x1][y2])

            # For second letter of pair
            crypt_text.append(cipher_table[x2][y1])

    # Transform crypt_text into a string for output
    new_text = ''
    for i in range(len(crypt_text)):
        new_text += crypt_text[i]
        if i % 2 != 0:
            new_text += ' '

    return new_text


def main():
    """
    Main function that receives user input and passes it to play_cipher( )
    """

    print('PLAYFAIR CIPHER PROGRAM')
    while True:
        while True:
            key = ''
            text = ''
            while True:
                try:
                    options = ['e', 'd', 't', 'out']
                    print('Which mode would like to use?')
                    mode = str(input('Encrypt -> e | Decrypt -> d | t -> show table for key | out -> exit program >> '))
                    if mode not in options:
                        raise ValueError
                    break
                except ValueError:
                    print('Valid commands: Encrypt -> e | Decrypt -> d | t -> Show Crypt Table')
            if mode == 'out':
                break
            try:
                if mode != 't':
                    text = str(input('Text to be encrypted/decrypted: '))
                key = str(input('Key to encrypt: '))
                break
            except ValueError:
                print('Only alphabetic characters accepted for encryption! ')

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
