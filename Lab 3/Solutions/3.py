import sys
import ast
def main(args):
    list1 = ast.literal_eval(args[1])
    list1.sort()
    print(list1)
    pass


if __name__ == "__main__":
    main(sys.argv)
    pass