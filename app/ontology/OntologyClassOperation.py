import json
from flask import Blueprint, request, jsonify, app
from owlready2 import get_ontology

from app.ontology.OtherUtils import OtherUtils
from app.owl.OwlPath import getOwlPath
from app.utils.AnalysisOwlUtils import AnalysisOwlUtils
from app.utils.OntoOperUtils import OntoOperUtils
import os

from app.viewmodel.view_classselect import view_classselect

ontologclass=Blueprint('ontologclass',__name__)

#3.class添加
@ontologclass.route('/classadd',methods=['POST'])
def ontoclassadd():
    if request.method == 'POST':
        print(request.json)
        filename,className,parentName = request.json['libraryName'],\
                                     request.json['className'],\
                                     request.json['parentName']
        OntoOperUtils.creatOwlClass(filename,className,parentName)
        contentlist=OntoOperUtils.rejectCreatMoreClass(filename,className)
        # classLayerList = OntoOperUtils.searchOwlClassLayer(filename)
        # print(classLayerList)
        return OtherUtils.decorateToJson(contentlist)

#4.class移除
@ontologclass.route('/classdel',methods=['POST'])
def ontoclassdel():
    if request.method=='POST':
        filename,classname=request.json['libraryName'],request.json['className']
        OntoOperUtils.delOwlClass(filename, classname)
        # select_obj = request.json['libraryName']
        classLayerList_del = OntoOperUtils.searchOwlClassLayer(filename)
        contentlist = OntoOperUtils.delLayerClass(filename, classname)
        # print(classLayerList_del)
        return OtherUtils.decorateToJson(contentlist)




#5.class查找
@ontologclass.route('/classsearch',methods=['POST'])
def ontoclasssearch():
    if request.method=='POST':
        DBName,colName,className='ontolo_classes','OCname',request.json['searchname']
        fuzzyResult = AnalysisOwlUtils.ontoFuzzyMatch(DBName, colName, className)
        return jsonify(fuzzyResult)


#6.class选择,返回class相关的信息，annotations,parents,relatiosnhips
@ontologclass.route('/classselect',methods=['POST'])
def ontoclassselect():
    if request.method == 'POST':
        result=view_classselect().translate(request.json['libraryName'],request.json['className'])
        result['relationships']= OntoOperUtils.searchClassRelat('Treatment','检查')
        return jsonify(result)

# #6.编辑Annotations
# @ontologclass.route('/annotationsadd',methods=['POST'])
# def addannotations():
#     # if request.method == 'POST':
#     return 'ok'
#
# #7.删除Annotations
# @ontologclass.route('/annotationsdel',methods=['POST'])
# def delannotations():
#     # if request.method == 'POST':
#     return 'ok'

#8.Parents添加
@ontologclass.route('/parentsadd',methods=['POST'])
def parentsadd():
    # if request.method == 'POST':
    return 'ok'

#9.Parents删除
@ontologclass.route('/parentsdel',methods=['POST'])
def parentsdel():
    # if request.method == 'POST':
    return 'ok'

#10.Relationships property模糊查询
@ontologclass.route('/relationsearch',methods=['POST'])
def propertysearch():
    if request.method == 'POST':
        result=OntoOperUtils.searchClassRelat(request.json['fileName'],request.json['className'])
        return jsonify(result)

#11.Relationships添加
@ontologclass.route('/reladd',methods=['POST'])
def reladd():
    if request.method == 'POST':
        fileName, relationName,proRelatName,domainName,rangeName = request.json['className'],\
                                                  request.json['relationship']['property'],\
                                                  '超类',\
                                                  request.json['classname'],\
                                                  request.json['relationship']['value']
        OntoOperUtils.creatOwlRelat(fileName, relationName, proRelatName, domainName, rangeName)
        return jsonify('ok'),201


#12.Relationships删除
@ontologclass.route('/reldel',methods=['POST'])
def reldel():
    if request.method == 'POST':

        return 'ok'