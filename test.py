from time import sleep

for x in range(10):
    print(
        """Progress {:2.1%}\n
fa
""".format(
            x / 10
        ),
        end="\033[3A",
    )
    sleep(200 / 1000)

print("Completed                \n           \n          ")
