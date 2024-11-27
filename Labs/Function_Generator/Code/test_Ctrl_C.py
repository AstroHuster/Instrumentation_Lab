from time import sleep

try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    print("^C !!!")
