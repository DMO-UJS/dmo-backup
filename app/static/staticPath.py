import os

def getStaticPath():
    staticpath = os.path.dirname(__file__)
    return staticpath

if __name__ == '__main__':
    path=getStaticPath()
    print(path)