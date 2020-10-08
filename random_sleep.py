import time
import random


class Sleep:
    @staticmethod
    def short():
        pause = random.randrange(1, 5)
        time.sleep(pause)

    @staticmethod
    def medium():
        pause = random.randrange(5, 30)
        print(f"Medium pause {pause} sec...")
        time.sleep(pause)

    @staticmethod
    def long():
        pause = random.randrange(10, 60)
        print(f"Long pause {pause} sec...")
        time.sleep(pause)

    @staticmethod
    def very_long():
        pause = random.randrange(45, 120)
        print(f"Very long pause {pause} sec...")
        time.sleep(pause)
