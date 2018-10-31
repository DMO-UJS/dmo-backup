import datetime
from owlready2 import *
#本体文件解析类

# from app.owl.CreatOwl.TreatmentOwl import *
from app.utils.ConnectDB import ConnectDB

class AnalysisOwlUtils:
    """""
    读OWL文件
    """""
    @classmethod
    def readOwl(cls,filepath):
        #OWL文件加载
        onto = get_ontology(filepath).load()
        return onto


    """""
    存储OWL文件
    """""
    @classmethod
    def saveOwl(cls,filepath,onto):
        onto.save(file=filepath)


    """""
    读取OWL文件内的所有本体对象
    返回:List
    例：['检查', 'FPG', 'OGTT', '妊娠期检测', '子宫张力', '宫高曲线', '眼科检查', '血糖检查']
    """""
    @classmethod
    def getAllClasses(cls,onto):
        classlists = []
        ontolists = list(onto.classes())
        for li in ontolists:
            classlists.append(li.name)
        return classlists


    """""
    获取所有对象及子对象信息，List返回
    输入：本体对象
    输出：列表[{'name':'*','children':[*]},{'name':'**','children':[**]}]，列表元素为字典
    例：[{'name':'检查'，'children':['宫高曲线','子宫张力','妊娠期检测','血糖检查']}]
    """""
    @classmethod
    def getAllClassesInfo(cls,onto):
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


    """""
    按照关键字进行查询
    输入 本体名 （String:'FRG'）
    输出 例：{'Name': 'FPG', 'Children': []}  （字典）
    """""
    @classmethod
    def getClassInfo(cls,onto,ClassName):
        ContentList = AnalysisOwlUtils.getAllClassesInfo(onto)
        for ClassDir in ContentList:
            if ClassDir['name'] == ClassName:
                return ClassDir


    """""
    数据库中查询读取本体对象备注信息
    输入 本体名 （String:'治疗方案'）
    输出 例：[{'name': '治疗方案', 'content': ''},{'name': '治疗方案一', 'content': ''}]
    select * from DB where label = classname
    """""
    @classmethod
    def getClassComent(cls,DBName,colName,className):
        db = ConnectDB()
        conn = db.getConnect()
        #填写sql语句
        sql = "select * from %s where %s = '%s'" %(DBName,colName,className)
        comments = db.queryDB(conn,sql)
        db.closedConnect(conn)
        dictlist = []
        for comment in comments:
            dictlist.append({'name': comment[1], 'content': comment[2]})
        #print(dictlist)
        return dictlist


    """""
    数据库中插入对象的备注信息
    输入 参数1：表名； 参数2：OCname值； 参数3：OCcommend值； 参数4：F_OLid值；
    输出 “operation success” ； “operation error”
    INSERT INTO 表名称 (列1，列2，....) VALUES (值1, 值2,....)
    insert into ontolo_classes (OCname,OCcommend,OCtime,F_OLid) values ('治疗方案六','放松心情','2018-10-31 14:44:46','1');
    """""
    @classmethod
    def insertClassComment(cls,DBName,V1,V2,V3):
        #获取当前时间
        # %Y-%m-%d %H:%M:%S  ===  年-月-日  小时-分钟-秒
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db = ConnectDB()
        conn = db.getConnect()
        # 填写sql语句
        sql = "INSERT INTO %s (OCname, OCcommend,OCtime,F_OLid) VALUES ('%s', '%s', '%s', '%s')" % (DBName,V1, V2, now_time, V3)
        comments = db.queryDB(conn, sql)
        db.closedConnect(conn)
        return comments


#测试
if __name__ == '__main__':
    filepath = '../OWL/Treatment.owl'
    #步骤：
    #   Step1:读取owl文件
    #   Step2:获取本体中所有的类
    #   Step3:所有的类的层级关系
    #   Step4:单独本体信息的查询（层级关系）
    #   Step5:从数据库中查询读取本体对象备注信息
    #   Step6:数据库中插入对象的备注信息

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

    #Step6 数据库中插入对象的备注信息
    result = AnalysisOwlUtils.insertClassComment('ontolo_classes','治疗方案六','放松心情','1')

    #打印
    print(onto)
    print(classList)
    print(dictLists)
    print(dir)
    print(comment)
    print(result)




