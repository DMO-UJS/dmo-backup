import os

def getJsonPath():
    owlpath = os.path.dirname(__file__)
    return owlpath

if __name__ == '__main__':
    path=getJsonPath()
    print(path)