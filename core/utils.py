import time

def spinner(text, duration=2):
    print(text, end="", flush=True)
    for _ in range(duration):
        print(".", end="", flush=True)
        time.sleep(1)
    print(" ✅")
