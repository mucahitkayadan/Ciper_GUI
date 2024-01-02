import codecs


class Cipher:
    @staticmethod
    def caesar_cipher(text, shift, encrypt=True):
        result = ''
        for char in text:
            if char.isalpha():
                offset = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - offset + shift * (1 if encrypt else -1)) % 26 + offset)
            else:
                result += char
        return result

    @staticmethod
    def vigenere_cipher(text, key, encrypt=True):
        result = ''
        key_index = 0
        for char in text:
            if char.isalpha():
                offset = ord('A') if char.isupper() else ord('a')
                key_char = key[key_index % len(key)]
                key_offset = ord('A') if key_char.isupper() else ord('a')
                result += chr((ord(char) - offset +
                               (ord(key_char) - key_offset) * (1 if encrypt else -1)) % 26 + offset)
                key_index += 1
            else:
                result += char
        return result

    @staticmethod
    def rail_fence_cipher(text, rails, encrypt=True):
        if encrypt:
            return ''.join(text[i::rails] for i in range(rails))
        else:
            cycle_length = 2 * (rails - 1)
            result = [' '] * len(text)
            index = 0

            for i in range(rails):
                j = 0
                while j + i < len(text):
                    result[j + i] = text[index]
                    index += 1
                    if i != 0 and i != rails - 1 and j + cycle_length - i < len(text):
                        result[j + cycle_length - i] = text[index]
                        index += 1
                    j += cycle_length

            return ''.join(result)

    @staticmethod
    def rot13_cipher(text):
        return codecs.encode(text, 'rot_13')

    @staticmethod
    def substitution_cipher(text, substitution_key, encrypt=True):
        text = text.upper()  # Convert text to uppercase
        # Convert substitution key to uppercase
        substitution_key = {k.upper(): v.upper() for k, v in substitution_key.items()}

        if encrypt:
            return ''.join(substitution_key.get(char, char) for char in text)
        else:
            reverse_key = {v: k for k, v in substitution_key.items()}
            return ''.join(reverse_key.get(char, char) for char in text)

#
# # Example Usage:
# cipher_instance = Cipher()
# # Define the substitution key
# substitution_key_ = {'A': 'Q', 'B': 'W', 'C': 'E', 'D': 'R',
#                      'E': 'T', 'F': 'Y', 'G': 'U', 'H': 'I', 'I': 'O', 'J': 'P',
#                      'K': 'A', 'L': 'S', 'M': 'D', 'N': 'F', 'O': 'G', 'P': 'H',
#                      'Q': 'J', 'R': 'K', 'S': 'L', 'T': 'Z',
#                      'U': 'X', 'V': 'C', 'W': 'V', 'X': 'B', 'Y': 'N', 'Z': 'M'}
#
#
# # Caesar Cipher
# encrypted_caesar = cipher_instance.caesar_cipher("HELLO", shift=3, encrypt=True)
# decrypted_caesar = cipher_instance.caesar_cipher(encrypted_caesar, shift=3, encrypt=False)
#
# # Vigenère Cipher
# encrypted_vigenere = cipher_instance.vigenere_cipher("HELLO", key="KEY", encrypt=True)
# decrypted_vigenere = cipher_instance.vigenere_cipher(encrypted_vigenere, key="KEY", encrypt=False)
#
# # Rail Fence Cipher
# encrypted_rail_fence = cipher_instance.rail_fence_cipher("HELLO", rails=3, encrypt=True)
# decrypted_rail_fence = cipher_instance.rail_fence_cipher(encrypted_rail_fence, rails=3, encrypt=False)
#
# # ROT13 Cipher
# encrypted_rot13 = cipher_instance.rot13_cipher("HELLO")
# decrypted_rot13 = cipher_instance.rot13_cipher(encrypted_rot13)
#
# # Substitution Cipher
# encrypted_substitution = cipher_instance.substitution_cipher("HELLO", substitution_key_, encrypt=True)
# decrypted_substitution = cipher_instance.substitution_cipher(encrypted_substitution, substitution_key_, encrypt=False)
#
# # Print Results
# print("Caesar Cipher:")
# print("Encrypted:", encrypted_caesar)
# print("Decrypted:", decrypted_caesar)
# print("\nVigenère Cipher:")
# print("Encrypted:", encrypted_vigenere)
# print("Decrypted:", decrypted_vigenere)
# print("\nRail Fence Cipher:")
# print("Encrypted:", encrypted_rail_fence)
# print("Decrypted:", decrypted_rail_fence)
# print("\nROT13 Cipher:")
# print("Encrypted:", encrypted_rot13)
# print("Decrypted:", decrypted_rot13)
# print("\nSubstitution Cipher:")
# print("Encrypted:", encrypted_substitution)
# print("Decrypted:", decrypted_substitution)
