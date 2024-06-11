from colorama import Fore, Back, Style

print(Fore.RED + "some red text" + Fore.WHITE + " and not anymore")
print(Back.GREEN + "GREEN TEXT" + Back.RESET + " and not anymore")
print(Style.DIM + "and in dim text" + Style.RESET_ALL + " and not anymore", end="\r")
print(f"\r{Style.RESET_ALL}")
print("back to normal now")
