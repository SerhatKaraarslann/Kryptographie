from Crypto.Cipher import AES
import binascii

def decrypt_raw_block(ciphertext_hex: bytes, key_hex: bytes) -> bytes:
    # Umwandlung von Hex-String zu echten Bytes
    ciphertext = binascii.unhexlify(ciphertext_hex)
    key = binascii.unhexlify(key_hex)

    # AES Instanz im ECB Modus (ohne IV, da ECB)
    cipher = AES.new(key, AES.MODE_ECB)

    # Entschlüsseln (KEIN unpad benutzen, da wir den rohen Block wollen!)
    decrypted_raw = cipher.decrypt(ciphertext)

    return binascii.hexlify(decrypted_raw)

def decrypt_aes_cbc(ciphertext_hex: bytes, key_hex: bytes, iv_hex: bytes) -> bytes:
    # Umwandlung von Hex-String zu echten Bytes
    ciphertext = binascii.unhexlify(ciphertext_hex)
    key = binascii.unhexlify(key_hex)
    iv = binascii.unhexlify(iv_hex)

    # AES Instanz im CBC Modus mit IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Entschlüsseln und unpad (PKCS7)
    decrypted = cipher.decrypt(ciphertext)

    return binascii.hexlify(decrypted)

if __name__ == "__main__":
    # Der Schlüssel aus der Aufgabe
    key = b'000102030405060708090a0b0c0d0e0f'
    
    # Die temporäre Datei (Ciphertext), nicht Plaintext!
    temp_ciphertext = b'0e6bcb21f0dbf708284b788059bb3b5b'

    print(f"Key: {key}")
    print(f"Ciphertext: {temp_ciphertext}")

    # Wir entschlüsseln, um den Zwischenwert (D_k(C)) zu erhalten
    decrypted_hex = decrypt_raw_block(temp_ciphertext, key)
    
    print(f'Decrypted Raw : {decrypted_hex}')
    
    # IV Berechnung direkt hier im Code
    # IV = Decrypted_Raw XOR Plaintext (0xFF...)
    decrypted_bytes = binascii.unhexlify(decrypted_hex)
    plaintext_bytes = b'\xff' * 16 # Der bekannte Plaintext aus Aufgabe 3.1
    
    # XOR Berechnung
    iv = bytes(a ^ b for a, b in zip(decrypted_bytes, plaintext_bytes))
   
   # IV Ausgabe
    print(f'Berechneter IV (Hex): {binascii.hexlify(iv)}')
   
    # Nun können wir den kompletten Ciphertext entschlüsseln
    full_ciphertext = b'f42672e2e0fce236d844515409df8132d8b757a75cd8930dd8be61255cd118ddc30f2cea e04c505f05feff694742db3d'
    iv_hex = binascii.hexlify(iv)
    
    decrypted_full_hex = decrypt_aes_cbc(full_ciphertext.replace(b' ', b''), key, iv_hex)
    
    # Umwandlung von Hex zurück in Bytes
    decrypted_bytes = binascii.unhexlify(decrypted_full_hex)

    # Hier decodieren wir die Bytes zu einem String mit 'latin-1'
    # Damit wird aus \xfc ein 'ü'
    plaintext_string = decrypted_bytes.decode('latin-1')
    
    print(f'Lösungssatz: {plaintext_string}')