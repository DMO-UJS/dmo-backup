import os.path
class OntoFileUtils:
    #创建OWL文件
    # 输入：filename：创建本体文件名
    # 返回：创建成功：True;
    #      创建失败：False
    def createOntoFile(self,filename):
        if os.path.exists(filename):
            print("This File Has Exited")
            return True
        else:
            RDFHead = "<?xml version='1.0'?>\n"
            RDFContend = "<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\n" \
                         "xmlns:xsd='http://www.w3.org/2001/XMLSchema#'\n" \
                         "xmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'\n" \
                         "xmlns:owl='http://www.w3.org/2002/07/owl#'\n" \
                         "xml:base='http://test.org/"+filename+"'\n" \
                         "xmlns='http://test.org/"+filename+"#'>\n"
            OWLHead = "<owl:Ontology rdf:about='http://test.org/"+filename+"'/>\n"
            RDFEnd = "</rdf:RDF>\n"
            Content = RDFHead+RDFContend+OWLHead+RDFEnd
            print(Content)
            f = open(filename, 'w+', encoding='utf-8')
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
            content = " <rdfs:subClassOf rdf:resource='http://www.w3.org/2002/07/owl#Thing'/>\n"
        else:
            content = " <rdfs:subClassOf rdf:resource='#" + ProClassName + "'/>\n"
        end = "</owl:Class>\n"
        final = "</rdf:RDF>"
        resource = head + content + end + final
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
        domainContent = " <rdfs:domain rdf:resource='#"+Domain+"'/>\n"
        rangeContent = ""
        for Range in RangeList:
            #print(RangeList[i])
            rangeContent += " <rdfs:domain rdf:resource='#"+Range+"'/>\n"
            #print(rangeContent)
        end = "</owl:ObjectProperty>\n"
        final = "</rdf:RDF>"
        resource = head+domainContent+rangeContent+end+final
        print(resource)
        return resource

    #onto文件写入操作
    #将编辑好的RDF内容写入文件
    def writeContent(self,filename,resource):
        f = open(filename, 'r', encoding='utf-8')
        lines = f.readlines()
        lines[-1] = resource
        f.close()
        f = open(filename, 'w', encoding='utf-8')
        f.truncate()
        for line in lines:
            f.write(line)
        f.close()


#测试代码
if __name__ == '__main__':
    filepath = '../../owl/3.owl'
    onto = OntoFileUtils()
    RelationName = "isMemberof"
    Domain = "检查"
    RangeList = ["妊娠期检查","OGTT","FPG","血糖检查","眼科检查","宫高曲线","子宫张力"]
    if onto.createOntoFile(filepath):
        String1 = onto.addOntoClass('检查','Thing')
        onto.writeContent(filepath,String1)
        String1 = onto.addOntoClass('检查', 'Thing')
        onto.writeContent(filepath, String1)