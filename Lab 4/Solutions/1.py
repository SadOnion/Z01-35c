import ast
inp = ""
while inp != "exit":
    expression = input("Expression: ")
    print("Solution: ",eval(expression))
    showtree = input("Do you want to show tree? ")
    if showtree == "yes":
        tree = ast.parse(expression, mode="eval")
        print(ast.dump(tree))
    inp = input()