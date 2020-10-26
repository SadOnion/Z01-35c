import random
    
def main():
    results = [0,0,0]
    options = ["kamień","papier","nożyce"]
    print("Gra w kamień,papier,nożyce")
    rounds = int(input("Podaj ilość rund:"))
    for x in range(rounds):
        print(f"Runda {x}")
        userInput = options.index(GetUserInput())
        computerChoice = random.randint(0,2)
        result = CalculateOutcome(userInput,computerChoice)
        print(f"Komputer wybrał {options[computerChoice]} , {GetStringBasedOnResult(result)}")
        AddVectors(results,result)
        print(results)
    print("Koniec Gry !")
    print(f"Wynik końcowy Gracz:{results[0]} Komputer:{results[1]} Remis:{results[2]}")
    pass    

def GetStringBasedOnResult(result):
    if(result[0] != 0):
        return "Wygrywasz!"
    if(result[1] != 0):
        return "Przegrywasz :O"
    if(result[2] != 0):
        return "Remis..."
    pass

def AddVectors(vec1,vec2):
    for i in range(len(vec1)):
        vec1[i]+=vec2[i]

def GetUserInput():
    userInput = ""
    while(userInput != "kamień" and userInput != "papier" and userInput != "nożyce"):
        userInput = input("Co wybierasz wpisz (kamień,papier,nożyce): ")
        print(userInput)
    return userInput
def CalculateOutcome(userChoice,computerChoice):
    if(userChoice == computerChoice):
        return [0,0,1]
    if(abs(userChoice-computerChoice) == 1):
        winner = max(userChoice,computerChoice)
        if(winner == userChoice):
            return [1,0,0]
        else:
            return [0,1,0]
    if(abs(userChoice-computerChoice) > 1):
        winner = min(userChoice,computerChoice)
        if(winner == userChoice):
            return [1,0,0]
        else:
            return [0,1,0]
    # 0 1 -> 1
    # 0 2 -> 0
    # 2 1 -> 2
    

if __name__ == "__main__":
    main()
    pass