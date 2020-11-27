# from application import app
# from application.forms import LoginForm, RegisterForm 

from flask import render_template,request,redirect,flash,session,url_for
from application import db
from . import main
from ..models import Audio,Image,Famous,Instruments,Comment,Masterwork,Users
from application import upload
import json,datetime
from flask_login import login_required

@main.route("/",methods=["GET","POST"])
@main.route("/index",methods=["GET","POST"])
def index():
    # upload.add_main()

    info = []
    
    instruments = Instruments.query.all()
    for ins in instruments:
        ins_info = dict()
        ins_info["name"] = ins.name
        ins_info["url"] = "../static/"+Image.query.filter_by(id = ins.pic).first().url
        ins_info['link'] = url_for('.base',ins=ins.name)
        # ins_info['link'] = "https://a.maorx.cn/"
        info.append(ins_info)
    print(info)
    return render_template("index.html",info=info)

@main.route("/base/<ins>",methods=["GET","POST"])
def base(ins):
    instrument = Instruments.query.filter_by(name = ins).first()
    if not instrument:
        return "main:base:error"
    
    #乐器的主要信息
    info = dict()
    info["name"]        =   ins
    info["pic_url"]     =   "../static"+Image.query.filter_by(id = instrument.pic).first().url
    info["intro_title"] =   instrument.title
    info["intro_text"]  =   instrument.intro

    #名人信息
    famouses = instrument.famouses
    fam_info = []
    for fam in famouses:
        info_tmp = {}
        info_tmp["name"]    =   fam.name
        info_tmp["pic_url"] =   "../static"+Image.query.filter_by(id = fam.pic).first().url
        #待完善
        fam_info.append(info_tmp)
    fam_len = len(fam_info)

    return render_template("base.html",info=info,finfo=fam_info,flen=fam_len)

@main.route("/piano/<ins>",methods=["GET","POST"])
def piano(ins):
    instrument = Instruments.query.filter_by(name = ins).first()
    if not instrument:
        return "main:base:error"
     #音阶信息
    gamuts = instrument.gamuts
    gam_info = []
    for gam in gamuts:
        info_tmp = {}
        info_tmp["c"] = "C" + str(gam.index)
        info_tmp["c_url"] = "../static"+Audio.query.filter_by(id = gam.note_c).first().url

        info_tmp["db"] = "Db" + str(gam.index)
        info_tmp["db_url"] = "../static"+Audio.query.filter_by(id = gam.note_db).first().url

        info_tmp["d"] = "D" + str(gam.index)
        info_tmp["d_url"] = "../static"+Audio.query.filter_by(id = gam.note_d).first().url

        info_tmp["eb"] = "Eb" + str(gam.index)
        info_tmp["eb_url"] = "../static"+Audio.query.filter_by(id = gam.note_eb).first().url

        info_tmp["e"] = "E" + str(gam.index)
        info_tmp["e_url"] = "../static"+Audio.query.filter_by(id = gam.note_e).first().url

        info_tmp["f"] = "F" + str(gam.index)
        info_tmp["f_url"] = "../static"+Audio.query.filter_by(id = gam.note_f).first().url

        info_tmp["gb"] = "Gb" + str(gam.index)
        info_tmp["gb_url"] = "../static"+Audio.query.filter_by(id = gam.note_gb).first().url

        info_tmp["g"] = "G" + str(gam.index)
        info_tmp["g_url"] = "../static"+Audio.query.filter_by(id = gam.note_g).first().url

        info_tmp["ab"] = "Ab" + str(gam.index)
        info_tmp["ab_url"] = "../static"+Audio.query.filter_by(id = gam.note_ab).first().url

        info_tmp["a"] = "A" + str(gam.index)
        info_tmp["a_url"] = "../static"+Audio.query.filter_by(id = gam.note_a).first().url

        info_tmp["bb"] = "Bb" + str(gam.index)
        info_tmp["bb_url"] = "../static"+Audio.query.filter_by(id = gam.note_bb).first().url

        info_tmp["b"] = "B" + str(gam.index)
        info_tmp["b_url"] = "../static"+Audio.query.filter_by(id = gam.note_b).first().url

        gam_info.append(info_tmp)
    return render_template("piano.html",ginfo = gam_info)
@main.route("/work/<ins>",methods=["GET","POST"])
def work(ins):
    print("work:",ins)
    instrument = Instruments.query.filter_by(name = ins).first()
    if not instrument:
        return "main:base:error"
    works = instrument.masterworks

    work_info = []
    for w in works:
        info_tmp = {}
        info_tmp["mp3_url"] = "../static"+Audio.query.filter_by(id = w.mp3).first().url  
        info_tmp["mp3_name"] = Audio.query.filter_by(id = w.mp3).first().name
        info_tmp["pic_url"] = "../static"+Image.query.filter_by(id = w.coverpic).first().url
        info_tmp["title"]   = w.title
        info_tmp["content"] = w.content
        work_info.append(info_tmp)
    tmp = json.dumps(work_info)
    return (tmp,200)

@main.route("/manage",methods=["GET","POST"])
@login_required
def manage():
    info = []
    instruments = Instruments.query.all()
    for ins in instruments:
        info_tmp = {}
        info_tmp["name"] = ins.name
        info_tmp["pic_url"] = "../static"+Image.query.filter_by(id = ins.pic).first().url
        info.append(info_tmp)
    name = '游客'
    email = session.get('email')
    if(email):
        name = Users.query.filter_by(email=email).first().name
    else:
        redirect(url_for("auth.login"))
    return render_template("manage.html",info=info,username=name)

@main.route("/delIns/<ins>",methods=["GET"])
@login_required
def delIns(ins):
    print("delIns:",ins)
    upload.delRes(ins)
    return redirect(url_for(".manage"))

@main.route("/uploadZip",methods=["GET","POST"])
@login_required
def uploadZip():
    zip_resource = request.files.get('zip_resoure')
    if zip_resource:
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        fname = "./tmp/"+dt_ms+".zip"
        zip_resource.save(fname)
        upload.addRes(fname)
    return redirect(url_for(".manage"))
