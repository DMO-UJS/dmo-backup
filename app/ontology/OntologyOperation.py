from flask import Blueprint, jsonify, request, render_template
from werkzeug.utils import secure_filename
import os

from app.models.OntologyLibray import Ontolo_sets, db
from app.ontology.OtherUtils import OtherUtils
from app.owl.OwlPath import getOwlPath
from app.utils.AnalysisOwlUtils import AnalysisOwlUtils
from app.utils.OntoOperUtils import OntoOperUtils

ontolog=Blueprint('ontolog',__name__)


#1.获取OntologyLibraryList
@ontolog.route('/ontolist',methods=['GET'])
def ontolist():
    Ontolo_set = Ontolo_sets.query.all()
    ontolist_data=[]
    for onto in Ontolo_set:
        #定义显示结构
        struct = {'name': '', 'owner': '', 'date': '', 'state': ''}
        struct['name']=onto.OLname
        struct['date']=onto.LRtime.strftime("%Y-%m-%d %H:%M:%S")
        struct['owner']=onto.Owner
        if onto.state:
            struct['state']='公有'
        else:
            struct['state']='私有'
        ontolist_data.append(struct)
    return jsonify(ontolist_data)


#2.获取选取的OntologyLibrary
@ontolog.route('/ontolistselect',methods=['POST'])
def ontoselect():
    if request.method=='POST':
        select_obj=request.json['name']
        classLayerList = OntoOperUtils.searchOwlClassLayer(select_obj)
        listDirList = []
        contentList = []
        for classLayer in reversed(classLayerList):
            if len(classLayer['children']) != 0:
                if len(contentList) == 0:
                    # 如果conteneList为空，直接加入
                    for i in range(len(classLayer['children'])):
                        contentList.append(classLayer['children'][i])
                else:
                    # 否则，求conteneList与 classLayer的差集,再加入求conteneList中
                    ret_list = [item for item in classLayer['children'] if item not in contentList]
                    classLayer['children'] = ret_list
                    for i in range(len(ret_list)):
                        contentList.append(ret_list[i])
        for classDir in reversed(classLayerList):
            if len(classDir['children']) != 0:
                for i in range(len(classDir['children'])):
                    for dir in listDirList:
                        if dir['name'] == classDir['children'][i]:
                            classDir['children'][i] = dir
                            listDirList.append(classDir)
            else:
                listDirList.append(classDir)
                contentList.append(classDir['name'])
        # print(listDirList[-1])
        if len(listDirList)!=0:
            return jsonify(listDirList[-1])
        else:
            print({'name':'Thing','children':[]})
            return jsonify({'name':'Thing','children':[]})


#本体创建路由
@ontolog.route('/ontocreate',methods=['GET','POST'])
def ontocreate():
    if request.method == 'POST':
        onto_obj=request.json
        print(onto_obj)
        if onto_obj['name'].strip() and onto_obj['owner'].strip() :
            OntoOperUtils.creatOwl(onto_obj['name'],onto_obj['owner'],onto_obj['description'],str(onto_obj['state']))
            return '创建本体成功'
        else:
            return '字段不能为空欧！'

#本体删除路由
@ontolog.route('/ontodelete',methods=['POST'])
def ontodelete():
    if request.method=='POST':
        del_obj=request.json['name']
        print(del_obj)
        del_lib=Ontolo_sets.query.filter_by(OLname=del_obj).first()
        db.session.delete(del_lib)
        db.session.commit()

        owlpath=getOwlPath()
        my_file = owlpath+'/'+request.json['name']+'.owl'
        if os.path.exists(my_file):
            os.remove(my_file)
            return jsonify('删除成功！')
        else:
            return jsonify('删除失败！')



#本体文件上传路由
@ontolog.route('/ontofileupload',methods=['GET','POST'])
def ontofileupload():
    if request.method == 'POST':
        f = request.files['file']
        print(f.filename)
        filename = secure_filename(f.filename)
        owlpath = getOwlPath()
        print(owlpath)
        try:
            f.save(owlpath + '/' + str(filename))
            return '本体文件上传成功！'
        except:
            return '上传失败！'

#本体可视化json路径
@ontolog.route('/ontojson',methods=['GET','POST'])
def ontojson():
    # if request.method == 'POST':
    #     name=request.json['name']
        path=OtherUtils.owlClassToJson('妊娠糖尿病')
        haha='static/妊娠糖尿病.json'
        alljson='static/all.json'
        return render_template('visualization.html',haha=haha,alljson=alljson)