from cryptography.fernet import Fernet

f = Fernet
a = f.generate_key()
print(a)
