
from flask import Blueprint, make_response, jsonify, request

from app.utils.AnalysisOwlUtils import AnalysisOwlUtils

match=Blueprint('match',__name__)


@match.route('/fuzzymatch',methods=['GET','POST'])
def fuzzymatch():
    if request.method == 'POST':
        obj=eval(request.data.decode(encoding = "utf-8"))
        fuzzyResult = AnalysisOwlUtils.ontoFuzzyMatch('ontolo_classes', 'OCname', obj['text'])
        response = make_response(jsonify(fuzzyResult))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response

