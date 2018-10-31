import os.path

from app.utils.AnalysisOwlUtils import AnalysisOwlUtils


class OntoFileUtils:
    #属性定义
    def __init__(self):
        self.filename = ""

    #创建OWL文件
    # 输入：filename：创建本体文件名
    # 返回：创建成功：True;
    #      创建失败：False
    def createOntoFile(self):
        f = open(self.filename, 'r', encoding='utf-8')
        content = f.readlines()
        if os.path.exists(self.filename) & len(content):
            print("This File Has Exited")
            return True
        else:
            RDFHead = "<?xml version='1.0'?>\n"
            RDFContend = "   <rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\n" \
                         "   xmlns:xsd='http://www.w3.org/2001/XMLSchema#'\n" \
                         "   xmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'\n" \
                         "   xmlns:owl='http://www.w3.org/2002/07/owl#'\n" \
                         "   xml:base='http://test.org/"+self.filename+"'\n" \
                         "   xmlns='http://test.org/"+self.filename+"#'>\n"
            OWLHead = "   <owl:Ontology rdf:about='http://test.org/"+self.filename+"'/>\n"
            RDFEnd = "</rdf:RDF>\n"
            Content = RDFHead+RDFContend+OWLHead+RDFEnd
            print(Content)
            f = open(self.filename, 'w+', encoding='utf-8')
            f.write(Content)
            f.close()
            print("Create Success")
            return False

    # 创建owl文件中的本体
    # 输入：Name：本体类名
    #      ProClassName :该本体父类名
    # 返回：RDF文件内容，String
    # 例：
    # <owl:Class rdf:about='#检查'>
    #  <rdfs:subClassOf rdf:resource='http://www.w3.org/2002/07/owl#Thing'/>
    # </owl:Class>
    def addOntoClass(self,Name, ProClassName):
        head = "<owl:Class rdf:about='#" + Name + "'>\n"
        if ProClassName == 'Thing':
            content = "   <rdfs:subClassOf rdf:resource='http://www.w3.org/2002/07/owl#Thing'/>\n"
        else:
            content = "   <rdfs:subClassOf rdf:resource='#" + ProClassName + "'/>\n"
        end = "</owl:Class>\n"
        #final = "</rdf:RDF>"
        resource = head + content + end
        print(resource)
        return resource

    #创建owl文件中的本体关系
    # 输入：RelationName：本体关系名
    #      Domain :领域本体名
    #      RangeList：子关系类列表
    # 返回：RDF文件内容，String
    # 例：
    # <owl:ObjectProperty rdf:about="#isMemberof">
    #   <rdfs:domain rdf:resource="#检查"/>
    #   <rdfs:range rdf:resource="#FPG"/>
    #</owl:ObjectProperty>
    def addOntoRelat(self,RelationName,Domain,RangeList):
        head = "<owl:ObjectProperty rdf:about='#"+RelationName+"'>\n"
        domainContent = "   <rdfs:domain rdf:resource='#"+Domain+"'/>\n"
        rangeContent = ""
        for Range in RangeList:
            #print(RangeList[i])
            rangeContent += "   <rdfs:range rdf:resource='#"+Range+"'/>\n"
            #print(rangeContent)
        end = "</owl:ObjectProperty>\n"
        #final = "</rdf:RDF>"
        resource = head+domainContent+rangeContent+end
        print(resource)
        return resource

    #删除OWL文件中的本体
    def delOntoClass(self,className):
        index = 0
        indexlist = 1
        f = open(self.filename,'r',encoding='utf-8')
        lines = f.readlines()
        f.close()
        onto = AnalysisOwlUtils.readOwl(self.filename)
        # dictLists = AnalysisOwlUtils.getAllClassesInfo(onto)
        dir = AnalysisOwlUtils.getClassInfo(onto,className)
        print(dir)
        if dir !=  None:
            oldStrBeg = "<owl:Class rdf:about='#"+className+"'>"
            for line in lines:
                if line.strip() == oldStrBeg:
                    print(index)
                    indexlist = index
                else:
                    index += 1
            lines[indexlist:indexlist+3] = "<!--**-->\n<!--**-->\n<!--**-->\n"
            f = open(self.filename, 'w', encoding='utf-8')
            for line in lines:
                f.write(line)
        f.close()

    #onto文件写入操作
    #将编辑好的RDF内容写入文件
    def writeContent(self,resource):
        f = open(self.filename, 'r', encoding='utf-8')
        lines = f.readlines()
        resource += "</rdf:RDF>"
        lines[-1] = resource
        f.close()
        f = open(self.filename, 'w', encoding='utf-8')
        f.truncate()
        for line in lines:
            f.write(line)
        f.close()



#测试代码
if __name__ == '__main__':
    filepath = '../OWL/3.owl'
    ontoFile = OntoFileUtils()
    ontoFile.filename = filepath
    ontoFile.createOntoFile()
    content = ""

    #本体类创建
    content += ontoFile.addOntoClass('OFPG','检查')
    content += ontoFile.addOntoClass('治疗', 'Thing')
    content += ontoFile.addOntoClass('检查', 'Thing')
    content += ontoFile.addOntoClass('血糖检查', '检查')
    #关系创建
    RelationName = "isMemberof"
    Domain = "检查"
    RangeList = ["妊娠期检查", "OGTT", "FPG", "血糖检查", "眼科检查", "宫高曲线", "子宫张力"]
    ontoFile.createOntoFile()
    content += ontoFile.addOntoRelat(RelationName,Domain,RangeList)

    #写操作
    ontoFile.writeContent(content)
    #删除
    #ontoFile.delOntoClass('OFPG')