data = {{"Name":"Jan1","Status":True},{"Name":"Jan2","Status":False},{"Name":"Jan3","Status":True},{"Name":"Jan4","Status":False},{"Name":"Jan5","Status":True},{"Name":"Jan6","Status":False},{"Name":"Jan7","Status":True}}
data = sorted(data,key= lambda item:item["Status"])
print(data)

def print(to_print):
    for x in to_print:
        print(x)