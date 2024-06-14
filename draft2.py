from colorama import Fore, Back, Style

for c in "\033[49m":
    print("'" + chr(ord(c)) + "'")

print("fim\033[0m")
