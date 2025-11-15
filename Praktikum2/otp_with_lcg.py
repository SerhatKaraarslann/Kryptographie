#Plaintext header 
plaintext_header = [0x4C,0x43,0x47] # p1,p2,p3
cipher_hex =  "05a5206fb5d13c944dea1a7acdb482139122b76a3077f1c8ba7cd674e9257c12c8b6af9586e1dbbda13fb18328d42f2537519282859586a6449a7590dd5d1e326dc349fd" 

#Ciphertext in Byte-Liste umwandeln, damit byteweise Verarbeitung einfacher wird.
cipher_bytes = bytes.fromhex(cipher_hex)

# Erste 3 Schlüsselbytes aus XOR berechnen
s = [cipher_bytes[i] ^ plaintext_header[i] for i in range(3)]
s1,s2,s3 = s
print("s1,s2,s3",s)

# A bestimmen A = ((s2-s3) / (s1-s2)) mod 256
diff1 = (s3-s2) % 256
diff2 = (s2-s1) % 256

# Brute Force , anstatt modulare Inverse was fehlschlägt, wenn gcd(Ds​,256)>1
# alle möglichen A Werte von 0 bis 256 geprüft.
A = None
for a in range(256):
    if (a * diff2) % 256 == diff1:
        A = a
        break

print("A :",A)

#B berechnen
B = (s2-A*s1)%256
print("B:",B)

#Schlüssel Strom generieren
def lcg_stream(seed,A,B,n):
    s = seed
    out = [s]
    for i in range(n-1):
        s = (A*s + B)%256
        out.append(s)
    return out

keystream = lcg_stream(s1,A,B,len(cipher_bytes))

#Entschlüsseln durch XOR
plaintext = bytes([c^k for c, k in zip(cipher_bytes,keystream)])

#Print
print("Entschlüsselte Plaintext :",plaintext.decode("latin-1"))