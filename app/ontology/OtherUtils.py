import json

from app.d3json.JsonPath import getJsonPath
from app.static.staticPath import getStaticPath


class OtherUtils:

    @classmethod
    def decorateToJson(cls, layerList):
        for firstDir in layerList:
            for otherDir in layerList:
                for i in range(len(firstDir['children'])):
                    if firstDir['children'][i] == otherDir['name']:
                        firstDir['children'][i] = otherDir
        return json.dumps(layerList[0],ensure_ascii=False)


    @classmethod
    def owlClassToJson(cls, fileName):
        jsonList = []
        labelList = ['疾病', '症状', '检查', '治疗', '疾病诊断分类']
        from app.utils.OntoOperUtils import OntoOperUtils
        for label in labelList:
            if label not in OntoOperUtils.searchOwlClass(fileName):
                labelList.remove(label)
        # label2dir
        jsonList.append([OtherUtils.owlClassDir(label,'标签') for label in labelList])
        jsonList = jsonList[0]
        # class2dir
        # from app.utils.OntoOperUtils import OntoOperUtils
        for label in labelList:
            childrenList = OntoOperUtils.searchOwlChildren(fileName, label)
            childrenList.remove(label)
            for childClass in childrenList:
                jsonList.append(OtherUtils.owlClassDir(childClass, label))
        jsonDir = {'nodes':jsonList}
        # links
        jsonLinks = []
        for label in labelList:
            childrenList =  OntoOperUtils.searchOwlChildren(fileName, label)
            childrenList.remove(label)
            for childClass in childrenList:
                jsonLinks.append({'source':label,'target':childClass,'vlaue':5})
                jsonLinks.append({'source': childClass, 'target': label, 'vlaue': 5})
        for label1 in labelList:
            for label2 in labelList:
                if label1 == label2:
                    continue
                else:
                    jsonLinks.append({'source': label1, 'target': label2, 'vlaue': 5})
                    jsonLinks.append({'source': label2, 'target': label1, 'vlaue': 5})
        jsonDir['links'] = jsonLinks
        print(json.dumps(jsonDir,ensure_ascii=False))
        path=getStaticPath()
        print(path)
        jsonfile = open(path+'/'+fileName + '.json', 'w')
        jsonfile.write(json.dumps(jsonDir, ensure_ascii=False))
        jsonfile.close()
        return path+'/'+fileName + '.json'


    @classmethod
    def owlClassDir(cls, className, label):
        dir = {}
        labelDir = {'标签':[0,20],'疾病':[1,10], '症状':[2,10], '检查':[3,10], '治疗':[4,10], '疾病诊断分类':[5,10]}
        dir['id'] = className
        dir['class'] = label
        dir['group'] = labelDir[label][0]
        dir['size'] = labelDir[label][1]
        # print(dir)
        return dir

if __name__=='__main__':
    OtherUtils.owlClassToJson('妊娠糖尿病')