import os
import sys
def main(args):
    for file in os.listdir(args[1]):
        if file.endswith(args[2]):
            print(file)

    pass

if __name__ == "__main__":
    main(sys.argv)
    pass