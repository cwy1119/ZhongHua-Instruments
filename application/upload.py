import zipfile
from .models import Audio,Image,Famous,Instruments,Comment,Masterwork,Gamut
from application import db
import json,cv2,os,datetime,shutil
from PIL import Image as PImage
import markdown
from .BlindWatermark import watermark
# from .addwatermark import add_watermark
#解压管理员上传的zip文件
def dezip(path,tmp_path):
    zip_file = zipfile.ZipFile(path)
    zip_list = zip_file.namelist()
    for f in zip_list:
        zip_file.extract(f,tmp_path)
    zip_file.close()

def joinPath(path,subpath):
    if(path[-1] != '/'):
        path.append('/')
    while(subpath[0] == '.' or subpath[0] == '/' or subpath[0] == '\\'):
        subpath = subpath[1:]
    return os.path.join(path,subpath)

#对图像进行处理和储存,返回其url
def dealImage(basepath,old_url):
    url = joinPath(basepath,old_url)
    print(url)
    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    while(os.path.exists("./application/static/images/"+dt_ms+".jpg")):
        dt_ms+="0"
    if(os.path.exists(url)):
        img = PImage.open(url)
        # todo:对文件进行处理
        print("./application/img/"+dt_ms+".jpg")
        img = img.convert('RGB')
        saveimg = "./application/static/images/"+dt_ms+".jpg"
        img_shape = img.size
        print(img_shape)
        img.save(saveimg)
        img.close()
        # 加水印 ./application/static/img/qcode.png
        if img_shape[0]*img_shape[1] >=750*750:
            print("up img is bigger enough")
            try:
                bwm1 = watermark(4399,2333,32)
                bwm1.read_ori_img(saveimg)
                bwm1.read_wm("./application/static/img/qcode.png")
                bwm1.embed(saveimg)
            except Exception as e:
                pass
    else:
        print("dealImage:file not exist")
    return "/images/"+dt_ms+".jpg"

#对音频文件进行处理
def dealAudio(basepath,old_url):
    url = joinPath(basepath,old_url)
    print(url)
    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    while(os.path.exists("./application/static/audio/"+dt_ms+".mp3")):
        dt_ms+="0"
    if(os.path.exists(url)):
        shutil.copyfile(url,"./application/static/audio/"+dt_ms+".mp3")
    else:
        print("dealImage:file not exist")
    return "/audio/"+dt_ms+".mp3"

def dealNote(basepath,old_url):
    url = joinPath(basepath,old_url)
    print(url)
    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    while(os.path.exists("./application/static/audio/"+dt_ms+".m4a")):
        dt_ms+="0"
    if(os.path.exists(url)):
        shutil.copyfile(url,"./application/static/audio/"+dt_ms+".m4a")
    else:
        print("dealImage:file not exist")
    return "/audio/"+dt_ms+".m4a"

def getContent(basepath,url):
    
    url = joinPath(basepath,url)
    print(url)
    txt = str()
    with open(url,encoding="utf-8") as f:
        txt = markdown.markdown(f.read())
        
    return txt



def findJsonPath(path, filename='source.json'):
    for root,dirs,files in os.walk(path):
        if files.count(filename):
            return root
    return None

# if __name__ == "__main__":
def addRes(zipfname):
    dt_ms = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    basepath = "./tmp/"+dt_ms+"/"
    dezip(zipfname,basepath)

    basepath = findJsonPath(basepath)+"/"
    with open(basepath+'source.json', 'r', encoding='utf-8') as f:
        resoure = json.load(f)

        #添加乐器图
        pic_url = dealImage(basepath,resoure['image'])
        inst_pic = Image(name=resoure['name'],url=pic_url)
        db.session.add(inst_pic)
        db.session.commit()

        #添加乐器
        ins_name        = resoure['name']
        ins_intro_title = resoure['briefInfo']['title']
        ins_intro       = getContent(basepath,resoure['briefInfo']['text'])
        ins_pic_id      = inst_pic.get_id()

        print("ins_pic_id:",ins_pic_id)
        instrument = Instruments(name=ins_name,title=ins_intro_title,intro = ins_intro,pic = ins_pic_id)
        db.session.add(instrument)
        db.session.commit()

        #添加名人
        famList = resoure['Famous']
        for fam in famList:
            fam_photo = dealImage(basepath,fam['photo'])
            fam_name = fam['name']

            famous_photo = Image(name = fam_name,url = fam_photo)
            db.session.add(famous_photo)
            db.session.commit()

            famous = Famous(iid = instrument.get_id(),name = fam_name,\
                pic = famous_photo.get_id())
            db.session.add(famous)
            db.session.commit()

            fam_intro   = fam['intro']
            intro_title = fam_intro['title']
            intro_text  = getContent(basepath,fam_intro['text'])
            intro = Comment(fid = famous.get_id(),title = intro_title,content= intro_text)
            db.session.add(intro)
            db.session.commit()
            
        #添加名曲
        workList = resoure['Masterwork']
        for work in workList:
            mp3     =   dealAudio(basepath,work['mp3'])
            name    =   work['name']
            audio   =   Audio(name = name,url=mp3)
            db.session.add(audio)

            pic         =   dealImage(basepath,work['image'])
            image       = Image(name=name,url=pic)
            db.session.add(image)
            db.session.commit()
            intro = work['intro']
            title = intro['title']
            text  = getContent(basepath,intro['text'])

            masterwork = Masterwork(iid = instrument.get_id(),mp3 = audio.get_id(),\
                coverpic = image.get_id(),title=title,content = text) 
            db.session.add(masterwork)
        db.session.commit()

        #添加音阶
        gamutList = resoure['Gamut']
        for gamut in gamutList:
           
            note_c  =   dealNote(basepath,gamut['c'])
            audio_c =   Audio(name="c",url=note_c)
            db.session.add(audio_c)

            note_db =   dealNote(basepath,gamut['db'])
            audio_db =   Audio(name="db",url=note_db)
            db.session.add(audio_db)

            note_d  =   dealNote(basepath,gamut['d'])
            audio_d =   Audio(name="d",url=note_d)
            db.session.add(audio_d)

            note_eb =   dealNote(basepath,gamut['eb'])
            audio_eb =   Audio(name="eb",url=note_eb)
            db.session.add(audio_eb)

            note_e  =   dealNote(basepath,gamut['e'])
            audio_e =   Audio(name="e",url=note_e)
            db.session.add(audio_e)

            note_f  =   dealNote(basepath,gamut['f'])
            audio_f =   Audio(name="f",url=note_f)
            db.session.add(audio_f)

            note_gb =   dealNote(basepath,gamut['gb'])
            audio_gb =   Audio(name="gb",url=note_gb)
            db.session.add(audio_gb)

            note_g  =   dealNote(basepath,gamut['g'])
            audio_g =   Audio(name="g",url=note_g)
            db.session.add(audio_g)

            note_ab =   dealNote(basepath,gamut['ab'])
            audio_ab =   Audio(name="ab",url=note_ab)
            db.session.add(audio_ab)

            note_a  =   dealNote(basepath,gamut['a'])
            audio_a =   Audio(name="a",url=note_a)
            db.session.add(audio_a)

            note_bb     =   dealNote(basepath,gamut['bb'])
            audio_bb    =   Audio(name="bb",url=note_bb)
            db.session.add(audio_bb)

            note_b  =   dealNote(basepath,gamut['b'])
            audio_b =   Audio(name="b",url=note_b)
            db.session.add(audio_b)

            #将note都存入数据库
            db.session.commit()

            index   =   gamut['index']

            gam = Gamut(iid = instrument.get_id(),
                        index = index,
                        note_c = audio_c.id,
                        note_db = audio_db.id,
                        note_d  = audio_d.id,
                        note_eb = audio_eb.id,
                        note_e  = audio_e.id,
                        note_f = audio_f.id,
                        note_gb = audio_gb.id,
                        note_g  = audio_g.id,
                        note_ab = audio_ab.id,
                        note_a =  audio_a.id,
                        note_bb = audio_bb.id,
                        note_b = audio_b.id)
            db.session.add(gam)
            db.session.commit()


# add_main()
def delSource(source):
    url = "./application/static"+source.url
    if(os.path.exists(url)):
        print("delSoure:","./application/static"+source.url)
        os.remove(url)
    db.session.delete(source)
    db.session.commit()
    return

def delRes(ins):
    instrument = Instruments.query.filter_by(name = ins).first()
         
   
   

    famouses = instrument.famouses
    for fam in famouses:

        commets = fam.comments
        for com in commets:
            db.session.delete(com)
        db.session.commit()

        db.session.delete(fam)
        db.session.commit()

        delSource(Image.query.filter_by(id = fam.pic).first())


        

        
        

    masterworks = instrument.masterworks
    for mw in masterworks:
        db.session.delete(mw)
        db.session.commit()

        delSource(Audio.query.filter_by(id = mw.mp3).first())
        delSource(Image.query.filter_by(id = mw.coverpic).first()) 


      

    gamut = instrument.gamuts
    for gam in gamut:

        db.session.delete(gam)
        db.session.commit()

        delSource(Audio.query.filter_by(id =gam.note_c).first())
        delSource(Audio.query.filter_by(id =gam.note_db).first())
        delSource(Audio.query.filter_by(id =gam.note_d).first())
        delSource(Audio.query.filter_by(id =gam.note_eb).first())
        delSource(Audio.query.filter_by(id =gam.note_e).first())
        delSource(Audio.query.filter_by(id =gam.note_f).first())
        delSource(Audio.query.filter_by(id =gam.note_gb).first())
        delSource(Audio.query.filter_by(id =gam.note_g).first())
        delSource(Audio.query.filter_by(id =gam.note_ab).first())
        delSource(Audio.query.filter_by(id =gam.note_a).first())
        delSource(Audio.query.filter_by(id =gam.note_bb).first())
        delSource(Audio.query.filter_by(id =gam.note_b).first())


    db.session.delete(instrument)
    db.session.commit()

    delSource(Image.query.filter_by(id = instrument.pic).first())