def toy_cipher(block):
    '''
    e(b1b2b3b4b5) = (b2b5b4b1b3)
    In python fängt index bei 0 an.
    Input : 0 1 2 3 4
    Output: 1 4 3 0 2
    '''
    b = list(block)
    #Mapping : 0->1, 1->4, 2->3, 3->0, 4->2
    permuted = [b[1], b[4], b[3], b[0], b[2]]
    return "".join(permuted)

def xor_strings(s1, s2):
    '''
    XOR two strings of equal length
    '''
    return "".join(str(int(a) ^ int(b)) for a, b in zip(s1, s2))

# Inputs
iv = "10101"
# Nachricht in 5-Bit Blöcken
ciphertext_blocks = ["01101","11011","11010","00110"]

#ECB
ecb_plaintext = ""
for block in ciphertext_blocks:
    decrypted_block = toy_cipher(block)
    ecb_plaintext += decrypted_block
print(f"ECB Plaintext: {ecb_plaintext}")

#CBC
cbc_plaintext = ""
previous_ciphertext = iv
for block in ciphertext_blocks:
    xor_input = xor_strings(block, previous_ciphertext)
    decrypted_block = toy_cipher(xor_input)
    cbc_plaintext += decrypted_block
    previous_ciphertext = block
print(f"CBC Plaintext: {cbc_plaintext}")

#CFB
cfb_plaintext = ""
previous_ciphertext = iv
for block in ciphertext_blocks:
    keystream = toy_cipher(previous_ciphertext)
    cipher = xor_strings(block, keystream)
    cfb_plaintext += cipher
    previous_ciphertext = block
print(f"CFB Plaintext: {cfb_plaintext}")

#OFB
ofb_plaintext = ""
previous_output = iv
for block in ciphertext_blocks:
    previous_output = toy_cipher(previous_output)
    cipher = xor_strings(block, previous_output)
    ofb_plaintext += cipher
print(f"OFB Plaintext: {ofb_plaintext}")

#CTR
ctr_plaintext = ""
counter_value = int(iv, 2)  # Convert IV from binary string to integer
for block in ciphertext_blocks:
    counter_block = format(counter_value, '05b')  # Convert counter to 5-bit binary string
    keystream = toy_cipher(counter_block)
    cipher = xor_strings(block, keystream)
    ctr_plaintext += cipher
    counter_value += 1  # Increment counter
    counter_value %= 32  # Wrap around if exceeds 5 bits
print(f"CTR Plaintext: {ctr_plaintext}")