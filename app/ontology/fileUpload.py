from flask import Blueprint, request, jsonify
from gridfs import GridFS

from app.libs.error_code import NotFound, DeleteSuccess
from app.utils.FuzzyMatch import FuzzyMatch
from app.utils.mongoUtils import GFS

file=Blueprint('file',__name__)

#文件上传
@file.route('/fileupload',methods=['POST'])
def fileupload():
    if request.method == 'POST':
        print(request.files.get('file'))
        fileName=request.form.get('fileName')
        print(fileName)
        gfs = GFS('mongotest', 'file')
        (file_db, fileTable) = gfs.createDB()
        fs = GridFS(file_db, gfs.file_table)
        fileObj=request.files.get('file')
        data = fileObj.read()
        ObjectId = fs.put(data, filename=fileName)
        print(ObjectId)
        fileObj.close()
        (bdata, attri)=gfs.getFile(file_db,ObjectId)
        filename=gfs.write_2_disk(bdata, attri)
        return jsonify({'state':'OK','ID':str(ObjectId),'URL':'static/'+filename})

#文件列表
@file.route('/filelist',methods=['GET'])
def filelist():
    if request.method == 'GET':
        gfs = GFS('mongotest', 'file')
        (file_db, fileTable) = gfs.createDB()
        filelist=gfs.listFile(file_db)
        return jsonify(filelist)


#文件查询
@file.route('/filefuzzy',methods=['POST'])
def filefuzzy():
    if request.method == 'POST':
        gfs = GFS('mongotest', 'file')
        (file_db, fileTable) = gfs.createDB()
        filelist = gfs.listFile(file_db)
        queryName = request.json['fileName']
        suggestions=FuzzyMatch.fuzzyFinder(queryName, filelist)
        result=[]
        for suggestion in suggestions:
            temple={'fileName':'','filePath':''}
            temple['fileName']=suggestion
            temple['filePath']='static/'+suggestion
            result.append(temple)
        return jsonify(result)

#文件精准查询
@file.route('/filesearch',methods=['POST'])
def filesearch():
    if request.method == 'POST':
        queryName=request.json['fileName']
        query = {'filename': queryName+'.pdf'}
        gfs = GFS('mongotest', 'file')
        (file_db, fileTable) = gfs.createDB()
        id = gfs.getID(file_db, query)
        if id:
            return jsonify({'URL':'/static/'+queryName+'.pdf'})
        else:
            return NotFound()

#文件删除
@file.route('/filedelete',methods=['POST'])
def filedelete():
    if request.method == 'POST':
        queryName = request.json['fileName']
        query = {'filename': queryName + '.pdf'}
        gfs = GFS('mongotest', 'file')
        (file_db, fileTable) = gfs.createDB()
        id = gfs.getID(file_db, query)
        gfs.remove(file_db,id)
        return DeleteSuccess()