
from flask import Blueprint, request, make_response, jsonify

from app.utils.AnalysisOwlUtils import AnalysisOwlUtils

askfor=Blueprint('askfor',__name__)


@askfor.route('/ask/new')
def ask():
    return 'new!!!!'



@askfor.route('/ask',methods=['GET','POST'])
def server_ask():
    if request.method == 'POST':
        obj=eval(request.data.decode(encoding = "utf-8"))  #eval()将str变为dict
        # print(obj['text'])
        comment = AnalysisOwlUtils.getClassComent('ontolo_classes', 'OCname', obj['text'])
        if comment:
            response = make_response(jsonify(comment))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response
        else:
            return jsonify('没有找到相关回答')