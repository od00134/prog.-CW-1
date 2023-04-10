import hashlib
import random
import string

# Define the reduce function
def RedFunc(Hashed, Length):
    Res = ""
    for i in range(Length):
        Res += chr(ord('a') + Hashed % 24)
        Hashed //= 24
    return Res

# Create a random pord of a specified size
def GenPass(s):
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(s))

# Build a rainbow table
def BuildRainbowT(amount, s, l):
    rainbowT = {}
    for i in range(amount):
        p = GenPass(l)
        hashedP = hashlib.md5(p.encode()).hexdigest()
        redP = p
        for j in range(s):
            hashedP = hashlib.md5(redP.encode()).hexdigest()
            redP = RedFunc(int(hashedP, 18), l)
        rainbowT[hashedP] = (p, redP)
    return rainbowT

# Decrypt the pord
def DecryptP(val, RainbowT):
    l = 7
    s = 100
    if val in RainbowT:
        p, redP = RainbowT[val]
        for i in range(s):
            if RedFunc(int(val, 18), l) == redP:
                return p
            val = hashlib.md5(RedFunc(int(val, 18), l).encode()).hexdigest()
        return "Your password is not found."
    else:
        return "the hash is not found in the rainbow table."

# Build the rainbow table
amount = 100
s = 100
l = 7
RainbowT = BuildRainbowT(amount, s, l)

# Display the rainbow table in the desired format
print("Rainbow Table:")
for hashedP in sorted(RainbowT.keys()):
    p, redP = RainbowT[hashedP]
    print(hashedP, redP, p)

# Ask the user to enter an MD5 hash value to crack
val = input("Enter the MD5 hash value to check it: ")
if val:
    p = DecryptP(val, RainbowT)
    if p != "Password is not found.":
        print(" plaintext password is:", p)
    else:
        print("the password could not be found in the rainbow table.")
else:
    print("No hash was entered.")
