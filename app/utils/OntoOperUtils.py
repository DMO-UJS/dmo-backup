import builtins

from owlready2 import *
import re
from app.ontology.OtherUtils import OtherUtils
from app.owl.OwlPath import getOwlPath
from app.utils.ConnectDB import ConnectDB
import os
class OntoOperUtils:

    """
    Part1 初始化
    """
    def __init__(self):
        pass

    """
    Part2 本体文件的存储、读取
    """
    # 2.1 读取本体文件、本体标识
    @classmethod
    def readOwl(cls, filePath):
        onto = get_ontology(filePath).load()
        print('read owlfile success')
        return onto
    # 2.2 存储本体文件
    @classmethod
    def saveOwl(cls,filePath):
        onto = get_ontology("http://test.org/onto.owl")
        onto.save(file=filePath)
        print('save owlfile success')

    """
    Part3 本体库内容的创建
        文件、对象、关系、备注
    """
    # 3.1 创建本体文件
    @classmethod
    def creatOwl(cls,fileName,Owner,Des,state):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology("http://test.org/onto.owl")
        with onto:
            class 超类(Thing):pass
            class 超关系(ObjectProperty):pass
        onto.save(file = filepath)
        ####数据库部分
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db = ConnectDB()
        conn = db.getConnect()
        insertLists = [fileName,Owner,now_time,Des,state]
        db.insertDBSql('ontolo_sets', insertLists, conn)
        ####
        print("creat owlfile success")
    # 3.2 创建本体对象
    @classmethod
    def creatOwlClass(cls,fileName,Name,proOwlName):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        print(list(onto.classes()))
        proClass = onto[proOwlName]
        owlClass = builtins.type(Name, (proClass,), {})
        # print(Name,proOwlName)
        print(list(onto.classes()))
        onto.save(file=filepath)
        ####数据库部分
        # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # db = ConnectDB()
        # conn = db.getConnect()
        # results = db.searchByDBColKey_All('ontolo_sets','OLname',fileName,conn)
        # for result in results:
        #     OLid = result[0]
        # insertLists = [Name, now_time, str(OLid)]
        # db.insertDBSql('ontolo_classes', insertLists, conn)
        ####
        print('creat owlclass success')
     # 3.3 创建本体关系（数据库部分待完善）
    @classmethod
    def creatOwlRelat(cls,fileName,relationName,proRelatName,domainName,rangeName):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        print(list(onto.classes()))
        proRelat = onto[proRelatName]
        domain = onto[domainName]
        range = onto[rangeName]
        owlRelat = __builtins__.type(relationName, (proRelat,), {'domain': [domain], 'range': [range]})
        onto.save(file=filepath)
        ####数据库部分
        ####
        print('creat owlrelat success')
    # 3.4 创建本体Annotations（数据库部分待完善）
    @classmethod
    def creatOwlAnno(cls,fileName,className,property,value):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        print(list(onto.classes()))
        owlClass = onto[className]
        owlClass.comment.append(locstr(property,lang = value))
        onto.save(file=filepath)
        ####数据库部分
        ####

    """
    Part4 查询
         对象、关系、备注
    """
    # 4.1 查询本体库内所有对象
    @classmethod
    def searchOwlClass(cls,fileName):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        owlClassList = list(onto.classes())
        return owlClassList

    # 4.2 查询获取本体库对象的层级关系
    ## 例：[{'name':'检查'，'children':['宫高曲线','子宫张力','妊娠期检测','血糖检查']}]
    @classmethod
    def searchOwlClassLayer(cls, fileName):
        classLayerList = []
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        for owlclass in list(onto.classes()):
            direct = {'name': owlclass.name, 'children': [owl.name for owl in owlclass.subclasses()]}
            classLayerList.append(direct)
        return classLayerList


    # 4.3 按照关键字进行单个查询
    # 输出 例：{'Name': 'FPG', 'Children': []}  （字典）
    @classmethod
    def getClassInfo(cls, fileName, ClassName):
        ContentList = OntoOperUtils.searchOwlClassLayer(fileName)
        for ClassDir in ContentList:
            if ClassDir['name'] == ClassName:
                return ClassDir


    # 4.4 查询本体库内所有关系
    @classmethod
    def searchOwlRelat(cls,fileName):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        owlRelatList = list(onto.properties())
        return owlRelatList
    # 4.5 查询本体对象备注信息
    @classmethod
    def searchOwlAnno(cls, fileName,className):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        owlClass = onto[className]
        annoList = owlClass.comment
        return annoList

    # 4.6 查询本体对象所有子类
    @classmethod
    def searchOwlChildren(cls, fileName, className):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        owlClass = onto[className]
        # annoList = owlClass.comment
        descendants = owlClass.descendants()
        # return annoList,descendants
        return [children.name for children in descendants]

    #4.7  防止多增加
    @classmethod
    def rejectCreatMoreClass(cls, fileName, className):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        owlClass = onto[className]
        print(list(owlClass.descendants()))
        contentList = [owl.name for owl in list(owlClass.descendants()) if owl.name != className]
        print(len(contentList))
        if len(contentList) != 0:
            for content in contentList:
                layerList = OntoOperUtils.delLayerClass(fileName, content)
                return layerList
        else:
            return OntoOperUtils.searchOwlClassLayer(fileName)

    #4.8 iri
    @classmethod
    def searchOwlClassIri(cls, fileName, className):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        owlClasses = list(onto.classes())
        Iri = ''
        for owlClass in owlClasses:
            if owlClass.name == className:
                Iri = owlClass.iri
        return Iri

    #4.9 parents
    @classmethod
    def searchOwlParent(cls, fileName, className):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        owlClass = onto[className]
        ancestors = list(owlClass.is_a)
        parent_data = []
        for ancestor in ancestors:
            struct={'name':''}
            struct['name']=ancestor.name
            parent_data.append(struct)
        return parent_data

    #  annotations
    @classmethod
    def searchOwlAnnotations(cls, fileName, className):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        owlClass = onto[className]
        dirList = []
        for comment in owlClass.comment:
            dir = {'property': comment.lang, 'value': comment}
            dirList.append(dir)
        return dirList

    # 9 关系查找
    # 通过给定的className,来返回所有与之有关系的class
    @classmethod
    def searchClassRelat(cls, fileName, className):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        owlClass = onto[className]
        ancestors = [owl.name for owl in list(owlClass.is_a)]
        descendants = [owl.name for owl in owlClass.descendants()]
        # 文件内容的读取
        with open(filepath, 'r', encoding='utf-8') as f:
            contents = f.read()
        contentLists = contents.split('\n\n')
        purposeLists = []
        zhengZe = '#\w*'
        dirList = []
        # 拿到包含className的元素
        for content in contentLists:
            if className in content and 'ObjectProperty' in content:
                purposeLists.append(content)
        for purpose in purposeLists:
            purposeList = purpose.split('\n')
            relation = re.search(zhengZe, purposeList[0]).group(0).lstrip('#')
            for content in purposeList[1:]:
                # className 为 domain
                if 'domain' in content and className in content:
                    for contentChild in purposeList[1:]:
                        # 查找子类
                        if 'range' in contentChild:
                            childClassName = re.search(zhengZe, contentChild).group(0).lstrip('#')
                            # 判断该子类是否属于class
                            if childClassName in descendants:
                                dir = {'relation': relation, 'domain': className, 'range': childClassName}
                                dirList.append(dir)
                # className 为 range
                else:
                    for contentParent in purposeList[1:]:
                        if 'domain' in contentParent:
                            parentClassName = re.search(zhengZe, contentParent).group(0).lstrip('#')
                            # 判断该父节点是否属于class
                            if parentClassName in ancestors:
                                dir = {'relation': relation, 'domain': parentClassName, 'range': className}
                                dirList.append(dir)
                    break

        return dirList

    #5.1 本体对象删除
    @classmethod
    def delOwlClass(cls, fileName, className):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        with open(filepath, 'r', encoding='utf-8') as f:
            contents = f.read()
        contentLists = contents.split('\n\n')
        childrenLists = OntoOperUtils.searchOwlChildren(fileName, className)
        for i in range(len(childrenLists)):
            for j in range(len(contentLists)):
                if childrenLists[i] in contentLists[j] and 'owl:Class' in contentLists[j]:
                    contentLists[j] = ''
        for i in range(len(contentLists)):
            if className in contentLists[i] and 'owl:ObjectProperty' in contentLists[i]:
                relLists = contentLists[i].split('\n')
                if className in relLists[2]:
                    contentLists[i] = ''
                    break
                else:
                    for j in range(len(relLists)):
                        if className in relLists[j]: relLists[j] = ''
                contentLists[i] = ''
                relLists = [x for x in relLists if x != '']
                for relList in relLists[:-1]:
                    contentLists[i] += relList + '\n'
                contentLists[i] += relLists[-1] + '\n\n'
            else:
                contentLists[i] += '\n\n'
        string = ""
        for content in contentLists:
            string += content

        f = open(filepath, 'w', encoding='utf-8')
        f.write(string)
        f.close()
        print('del owlclass success')

    # 5.2 删除层级对象

    @classmethod
    def delLayerClass(cls, fileName, className):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        onto = get_ontology(filepath).load()
        delClass = onto[className]
        descentList = [owlClass.name for owlClass in delClass.descendants()]
        layerList = OntoOperUtils.searchOwlClassLayer(fileName)
        for descent in descentList:
            for direct in layerList:
                if descent == direct['name']:
                    layerList.remove(direct)
        for direct in layerList:
            if className in direct['children']:
                direct['children'].remove(className)
        return layerList


"""
工具测试
"""
if __name__=='__main__':
    # a=OntoOperUtils.searchOwlClassLayer('老板')
    # print(OtherUtils.decorateToJson(a))

    OntoOperUtils.delOwlClass('老板','能力')
    content = OntoOperUtils.searchOwlClassLayer('老板')
    # b = OntoOperUtils.delLayerClass('老板','能力')
    print(OtherUtils.decorateToJson(content))