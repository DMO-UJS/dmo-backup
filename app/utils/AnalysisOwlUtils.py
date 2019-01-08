<<<<<<< HEAD
from owlready2 import *
=======
>>>>>>> 徐煜涵
#本体文件解析类
from owlready2 import *

from app.owl.OwlPath import getOwlPath
from app.utils.ConnectDB import ConnectDB
from app.utils.FuzzyMatch import FuzzyMatch
<<<<<<< HEAD


class AnalysisOwlUtils:
    """""
=======
from app.utils.OntoFileUtils import OntoFileUtils


class AnalysisOwlUtils:

    """""
    1.1
>>>>>>> 徐煜涵
    读OWL文件
    """""
    @classmethod
    def readOwl(cls,filepath):
        #OWL文件加载
        onto = get_ontology(filepath).load()
        return onto

<<<<<<< HEAD

    """""
=======
    """""
    1.2
>>>>>>> 徐煜涵
    存储OWL文件
    """""
    @classmethod
    def saveOwl(cls,filepath,onto):
        onto.save(file=filepath)
        print('saved success')

    """
    2.1
    创建本体文件
    """
    @classmethod
    def creatOwl(cls,fileName,Owner,OLname,Des,state):
        owlpath = getOwlPath()
        filepath = owlpath + "/%s.owl" % (fileName)
        ontoFile = OntoFileUtils()
        ontoFile.filename = filepath
        ontoFile.createOntoFile()
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db = ConnectDB()
        conn = db.getConnect()
        insertLists = [Owner,OLname,now_time,Des,state]
        db.insertDBSql('ontolo_sets', insertLists, conn)
        print("creat owlfile success")

    """
    2.2
    创建本体对象
    """
    @classmethod
    def creatOwlClass(cls,fileName,Name,ProClassName):
        ontoFile = OntoFileUtils()
        ontoFile.filename = "../owl/%s.owl" %fileName
        ontoFile.createOntoFile()
        content = ""
        content += ontoFile.addOntoClass(Name,ProClassName)
        ontoFile.writeContent(content)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db = ConnectDB()
        conn = db.getConnect()
        results = db.searchByDBColKey_All('ontolo_sets','OLname',fileName,conn)
        for result in results:
            OCid = result[0]
        insertLists = [Name, now_time, str(OCid)]
        db.insertDBSql('ontolo_classes', insertLists, conn)
        print('creat owlclass success')

    """
    2.3
    创建本体关系
    """
    @classmethod
    def creatOwlRelat(cls,fileName,RelationName,Domain,RangeList):
        ontoFile = OntoFileUtils()
        ontoFile.filename = "../owl/%s.owl" %fileName
        ontoFile.createOntoFile()
        content = ""
        content += ontoFile.addOntoRelat(RelationName, Domain, RangeList)
        ontoFile.writeContent(content)
        print('creat owlrelat success')

    """
    3.1
    删除本体对象
    """
    @classmethod
    def delOwlClass(cls,fileName,className):
        ontoFile = OntoFileUtils()
        ontoFile.filename = "../owl/%s.owl" %fileName
        ontoFile.createOntoFile()
        ontoFile.delOntoClass(className)
        print('creat owlclass success')


    """""
<<<<<<< HEAD
=======
    4.1
>>>>>>> 徐煜涵
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
<<<<<<< HEAD
=======
    4.2
>>>>>>> 徐煜涵
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
<<<<<<< HEAD
=======
    4.3
>>>>>>> 徐煜涵
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
<<<<<<< HEAD
=======
    4.4
>>>>>>> 徐煜涵
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
<<<<<<< HEAD
        sql = "select * from %s where %s = '%s'" %(DBName,colName,className)
        comments = db.queryDB(conn,sql)
        db.closedConnect(conn)
=======
        # sql = "select * from %s where %s = '%s'" %(DBName,colName,className)
        comments = db.searchByKey_All(DBName, colName, className,conn)
>>>>>>> 徐煜涵
        dictlist = []
        for comment in comments:
            dictlist.append({'name': comment[1], 'content': comment[2]})
        #print(dictlist)
        return dictlist

    """
<<<<<<< HEAD
=======
    4.5
>>>>>>> 徐煜涵
    根据关键字进行本体类模糊查询
    输入：DB，列名，关键字
    输出：列表 [可能的备选词]
    """
    @classmethod
    def ontoFuzzyMatch(cls,DBName,colName,keyWord):
        db = ConnectDB()
        conn = db.getConnect()
<<<<<<< HEAD
        sql = "select %s from %s " % (colName, DBName)
        results = db.queryDB(conn,sql)
        db.closedConnect(conn)
=======
        # sql = "select %s from %s " % (colName, DBName)
        results = db.searchColByDB(colName, DBName,conn)
>>>>>>> 徐煜涵
        fuzzyList = []
        for result in results:
            fuzzyList.append(result[0])
        #print('dictlist',dictlist)
        return  FuzzyMatch.fuzzyFinder(keyWord, fuzzyList)


<<<<<<< HEAD
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
=======
>>>>>>> 徐煜涵


#测试
if __name__ == '__main__':
<<<<<<< HEAD
    filepath = '../owl/3.owl'
=======
    filepath = '../owl/illness.owl'
>>>>>>> 徐煜涵
    #步骤：
    #   Step1:读取owl文件
    #   Step2:获取本体中所有的类
    #   Step3:所有的类的层级关系
    #   Step4:单独本体信息的查询（层级关系）
    #   Step5:从数据库中查询读取本体对象备注信息
    #   Step6:数据库中插入对象的备注信息
    #   Step7:本体类的模糊查询
<<<<<<< HEAD

    ## Step1
    onto = AnalysisOwlUtils.readOwl(filepath)
=======
    #   Step8:创建本体库
>>>>>>> 徐煜涵

    # Step1
    #onto = AnalysisOwlUtils.readOwl(filepath)
    #
    # ## Step2 所有类
    # classList = AnalysisOwlUtils.getAllClasses(onto)
    #
    # ## Step3 层级关系
    # dictLists = AnalysisOwlUtils.getAllClassesInfo(onto)
    #
    # ## Step4 查询单独一个类层级关系
    # dir = AnalysisOwlUtils.getClassInfo(onto,'检查')
    #
    # ## Step5 根据关键词读取
    # comment = AnalysisOwlUtils.getClassComent('ontolo_classes','OCname','治疗方案')
    #
    # #Step6 数据库中插入对象的备注信息
    # result = AnalysisOwlUtils.insertClassComment('ontolo_classes','治疗方案七','放松心情','1')
    #
    # #Step7 本体类的模糊查询
    # fuzzyResult = AnalysisOwlUtils.ontoFuzzyMatch('ontolo_classes','OCname','一')
    #
    #Step8 本体库创建
    # AnalysisOwlUtils.creatOwl('妊娠综合征','杨鹤标','妊娠综合征','我也不知道写啥了','0')
    # AnalysisOwlUtils.creatOwl('妊娠糖尿病', '胡惊涛', '妊娠糖尿病', '我也不知道写啥了', '1')

    #Step9 创建本体对象
    # AnalysisOwlUtils.creatOwlClass('妊娠糖尿病', '治疗方案', 'Thing', '好好吃饭')
    # AnalysisOwlUtils.creatOwlClass('妊娠糖尿病', '治疗方案一', '治疗方案', '多喝热水')
    # AnalysisOwlUtils.creatOwlClass('妊娠糖尿病', '治疗方案二', '治疗方案', '多跑步')
    # AnalysisOwlUtils.creatOwlClass('妊娠糖尿病', '治疗方案三', '治疗方案', '多睡觉')
    # AnalysisOwlUtils.creatOwlClass('妊娠糖尿病', '治疗方案四', '治疗方案', '听医生的话')

    #Step10 本体关系创建
    RelationName = "isMemberof"
    Domain = "检查"
    RangeList = ["妊娠期检查", "OGTT", "FPG", "血糖检查", "眼科检查", "宫高曲线", "子宫张力"]
    AnalysisOwlUtils.creatOwlRelat('妊娠糖尿病', RelationName, Domain, RangeList)


<<<<<<< HEAD
    #Step6 数据库中插入对象的备注信息
    result = AnalysisOwlUtils.insertClassComment('ontolo_classes','治疗方案六','放松心情','1')

    #Step7 本体类的模糊查询
    fuzzyResult = AnalysisOwlUtils.ontoFuzzyMatch('ontolo_classes','OCname','一')

    #打印
    print(onto)
    print(classList)
    print(dictLists)
    print(dir)
    print(comment)
    print(result)
    print(fuzzyResult)
=======
#ConnectDB测试
    #DBDeatils = AnalysisOwlUtils.test('ontolo_classes')

    #打印
    # print('onto:',onto)
    # print('classList:',classList)
    # print('dictLists:',dictLists)
    # print('dir:',dir)
    # print('comment:',comment)
    # print('result:',result)
    # print('fuzzyResult:',fuzzyResult)
    # print(DBDeatils)
>>>>>>> 徐煜涵




