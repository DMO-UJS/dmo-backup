from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, Request, jsonify, make_response, json

from app import create_app
from app.forms.OntoAddform import OntoAddForm
from app.forms.OntoDelform import OntoDelForm
from app.forms.OntoRelAddform import OntoRelAddForm
from app.forms.OntoRelDelform import OntoRelDelForm

from app.models.OntologyLibray import Ontolo_sets, Ontolo_relats, db
from app.utils.AnalysisOwlUtils import AnalysisOwlUtils

from app.utils.OntoFileUtils import OntoFileUtils

app=create_app()


@app.route('/test',methods=['GET','POST'])
def test():
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


@app.route('/')
def hello_world():
    return 'Hello World !'

@app.route('/dmo')
def home():


    Ontolo_set=Ontolo_sets.query.all()
    Ontolo_rel=Ontolo_relats.query.all()

    return render_template('home-index.html', Ontolo_set=Ontolo_set, Ontolo_rel=Ontolo_rel)



#本体库添加
@app.route('/onto_form',methods=['GET', 'POST'])
def ontoaddform():
    form=OntoAddForm()
    if request.method == 'POST' :
        # print(form.data)
        onto_obj=form.data
        onto_name=onto_obj['onto_name']
        onto_state=onto_obj['pub_priv']
        LRtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data={'OLname':'','LRtime':LRtime,'state':0}
        data['OLname']=onto_name
        if onto_state=='on':
            data['state']=1
        print(data)

        onto = OntoFileUtils()
        filepath = 'owl/' + onto_name + '.owl'
        onto.createOntoFile(filepath)

        Ontolo_set=Ontolo_sets()
        Ontolo_set.set_attrs(data)
        db.session.add(Ontolo_set)
        db.session.commit()


        # return redirect(url_for('home'))

    return render_template('onto-form.html', form=form)

#本体库删除
@app.route('/onto_del_form', methods=['GET', 'POST'])
def ontodelform():
    form = OntoDelForm()
    Ontolo_set = Ontolo_sets.query.all()
    Ontolo_rel = Ontolo_relats.query.all()
    if request.method=='POST':
        # print(form.data)
        del_obj=form.data
        del_obj=del_obj['onto_name']
        print(del_obj)

        del_lib=Ontolo_sets.query.filter_by(OLname=del_obj).first()
        db.session.delete(del_lib)
        db.session.commit()
    return render_template('delete-owl.html', Ontolo_set=Ontolo_set, Ontolo_rel=Ontolo_rel, form=form)



#本体关系添加
@app.route('/onto_relat_form',methods=['GET', 'POST'])
def ontorealtaddform():
    form = OntoRelAddForm()
    OntoSet=Ontolo_sets().query.all()
    if request.method == 'POST':
        # print(form.data)
        ontorel_obj = form.data
        ontorel_name = ontorel_obj['onto_name']
        des_1 = ontorel_obj['des_1']
        des_2 = ontorel_obj['des_2']
        LRtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        search_obj=ontorel_obj['corresponding']
        lib = Ontolo_sets.query.filter_by(OLname=search_obj).first()
        data={'ORname':ontorel_name,'Des1':des_1,'Des2':des_2,'LRtime':LRtime,
              'F_OLid':lib.OLid}
        print(data)

        Ontolo_rel = Ontolo_relats()
        Ontolo_rel.set_attrs(data)
        db.session.add(Ontolo_rel)
        db.session.commit()
    return render_template('relat-form.html', OntoSet=OntoSet, form=form)


#本体关系删除
@app.route('/onto_relat_del_form',methods=['GET', 'POST'])
def ontorealtdelform():
    Ontolo_set = Ontolo_sets.query.all()
    Ontolo_rel = Ontolo_relats.query.all()
    form=OntoRelDelForm()
    Rel_list=[]
    data={'onto_name':'','onto_rel':''}
    if request.method == 'POST' :
        print(form.data)
        # ontorel_obj = form.data
        # search_obj = ontorel_obj['onto_name']
        # lib = Ontolo_sets.query.filter_by(OLname=search_obj).first()
        #
        # del_lib = Ontolo_relats.query.filter_by(F_OLid=lib.OLid).all()
        # for del_lib_list in del_lib:
        #     db.session.delete(del_lib_list)
        #     db.session.commit()
        onto_obj = form.data
        search_obj = onto_obj['onto_name']    #选出本体库对应关系库
        lib = Ontolo_sets.query.filter_by(OLname=search_obj).first()
        rel_list=Ontolo_relats.query.filter_by(F_OLid=lib.OLid).all()   #对应的关系库
        Rel_list=rel_list
        # print(Rel_list)

        if onto_obj['onto_rel']!='None':
            del_lib=Ontolo_relats.query.filter_by(F_OLid=lib.OLid,ORname=onto_obj['onto_rel']).all()
            print(del_lib)
            for del_lib_list in del_lib:
                db.session.delete(del_lib_list)
                db.session.commit()

    return render_template('delete-relate.html', Ontolo_set=Ontolo_set, Ontolo_rel=Ontolo_rel, Rel_list=Rel_list)


#本体库资源展示
@app.route('/index.html',methods=['GET', 'POST'])
def ontodisplay():
    filepath='http://127.0.0.1:5000/static/flare.json'
    return render_template('index.html',fp=filepath)

if __name__=='__main__':
    app.run(debug=True)

