import os

def getOwlPath():
    owlpath = os.path.dirname(__file__)
    return owlpath

if __name__ == '__main__':
    path=getOwlPath()
    print(path)