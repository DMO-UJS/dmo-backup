import json
from owlready2 import *
#本体文件解析类

# from app.owl.CreatOwl.TreatmentOwl import *
from app.utils.ConnectDB import ConnectDB

class AnalysisOwlUtils:
    #读OWL文件
    def readOwl(filepath):
        #OWL文件加载
        onto = get_ontology(filepath).load()
        return onto

    #存储OWL文件
    def saveOwl(filepath,onto):
        onto.save(file=filepath)

    #读取OWL文件内的所有本体对象
    #返回:List
    #例：['检查', 'FPG', 'OGTT', '妊娠期检测', '子宫张力', '宫高曲线', '眼科检查', '血糖检查']
    def getAllClasses(onto):
        classlists = []
        ontolists = list(onto.classes())
        for li in ontolists:
            classlists.append(li.name)
        return classlists

    #获取所有对象及子对象信息，List返回
    #输入：本体对象
    #输出：列表[{'name':'*','children':[*]},{'name':'**','children':[**]}]，列表元素为字典
    # 例：[{'name':'检查'，'children':['宫高曲线','子宫张力','妊娠期检测','血糖检查']}]
    def getAllClassesInfo(onto):
        classesContent = []
        dictLists = []
        for owlclass in list(onto.classes()):
            #获取子对象，存入set中
            sets = owlclass.descendants()
            sets.remove(owlclass)
            for set in sets:
                #子对象信息存入content列表中
                classesContent.append(set.name)
            dict_Content = {'name': owlclass.name, 'content': classesContent}
            classesContent = []
            dictLists.append(dict_Content)
        return dictLists

    #按照关键字进行查询
    # 输入 本体名 （String:'FRG'）
    # 输出 例：{'Name': 'FPG', 'Children': []}  （字典）
    def getClassInfo(onto, ClassName):
        ContentList = AnalysisOwlUtils.getAllClassesInfo(onto)
        for ClassDir in ContentList:
            if ClassDir['name'] == ClassName:
                return ClassDir
    #数据库中查询读取本体对象备注信息
    # 输入 本体名 （String:'治疗方案'）
    # 输出 例：[{'name': '治疗方案', 'content': ''},{'name': '治疗方案一', 'content': ''}]
    # select * from DB where label = classname
    @classmethod
    def getClassComent(cls,DBName,colName,className):
        db = ConnectDB()
        conn = db.getConnect()
        #填写sql语句
        sql = "select * from "+DBName+" where "+colName+" = '"+className +"'"
        comments = db.queryDB(conn,sql)
        db.closedConnect(conn)
        dictlist = []
        for comment in comments:
            dictlist.append({'name': comment[1], 'content': comment[2]})
        #print(dictlist)
        return dictlist

    # json数据返回
    def returnByJson(lists):
        dict_Thing = {'name': 'Thing', 'children': lists}
        jsonValue = json.dumps(dict_Thing, ensure_ascii=False)
        return jsonValue

#测试
if __name__ == '__main__':
    filepath = '../owl/2.owl'
    #步骤：
    #   Step1:读取owl文件
    #   Step2:获取本体中所有的类
    #   Step3:单独本体信息的查询
    #   Step4:从数据库中查询读取本体对象备注信息
    #   Step5:包装为JSON格式的数据

    ## Step1
    onto = AnalysisOwlUtils.readOwl(filepath)

    ## Step2 所有类
    classList = AnalysisOwlUtils.getAllClasses(onto)

    ## Step3 层级关系
    dictLists = AnalysisOwlUtils.getAllClassesInfo(onto)

    ## Step4 查询单独一个类层级关系
    dir = AnalysisOwlUtils.getClassInfo(onto,'检查')

    ## Step5 根据关键词读取
    comment = AnalysisOwlUtils.getClassComent('ontolo_classes','OCname','治疗方案')


    #打印
    print(onto)
    print(classList)
    print(dictLists)
    print(dir)
    print(comment)


