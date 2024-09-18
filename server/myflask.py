from flask import Flask, render_template, jsonify, request, session, escape, render_template, redirect, flash
import os
import re
import json
import requests
import string
import random
from server.movie_dao import Movie_dao
from server.bkmk_dao import Bkmk_dao
from server.users_dao import Users_dao
from server.comm_dao import MyDaoReply
from server.notice_dao import NoticeDao
from server.evl_dao import Evl_dao
from server.bbs_dao import MyDaoCommunity
from datetime import datetime
from werkzeug.utils import secure_filename
from server.qestn_dao import Qestn_dao
from server.ticket_dao import Ticket_dao
from server.genre_dao import Genre_dao
from server.nation_dao import Nation_dao
from server.faq_dao import faqDAO
from server.reco_algo import reco_algo
from server.reco_dao import Reco_dao
from server.payment_dao import Payment_dao
from flask.helpers import send_file
from server.mymail import MyMail
from server.mysms import MySms



DIR_UPLOAD = 'Z:/upload';
TIME = str(datetime.today().strftime("%Y%m%d%H%M%S"))

app = Flask(__name__, static_url_path="", static_folder='static')
app.secret_key = "secret_key"


####################################################################
def getSession():
    user_id = ""
    try:
        user_id = str(escape(session["user_id"]))
    except:
        pass
      
    if user_id == "" :
        return False, user_id
    else :
        return True, user_id

@app.route('/sign') 
def sign_render(): 
    return render_template('sign.html')

@app.route('/yak') 
def yak_render(): 
    return render_template('yakgwan.html')


@app.route('/login') 
def login_render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return render_template('login.html')
    
    return redirect("main")   

@app.route('/login.ajax', methods=['POST'])
def login_ajax():
    user_id = request.form["user_id"]
    user_password = request.form["user_password"]
    
    print("user_id", user_id)
    print("user_password", user_password)
    
    list = Users_dao().mylogin(user_id, user_password) ##
    
    pymt_obj = Payment_dao()
    pymts = pymt_obj.check(user_id, '1')
    
    mngr_flag = ''
    msg = ""
    
    if len(list) == 1:
        if list[0]['act_flag'] == 'n':
            msg = 'del'
        else:
            session["user_id"] = list[0]['user_id']
            session["user_nm"] = list[0]['user_nm']
            mngr_flag = list[0]['mngr_flag']
            msg = "ok"
            
        if len(pymts) > 0:
            session["payment_flag"] = pymts[0]['payment_flag']
    else:
        msg = "ng"

    return jsonify(msg = msg, mngr_flag = mngr_flag)

@app.route('/login_kakao.ajax', methods=['POST'])
def login_kakao_ajax():
    user_id = request.form["user_id"]
    user_nm = request.form["user_nm"]
    user_email = request.form["user_email"]
    
    print("user_id",user_id)
    print("user_nm",user_nm)
    print("user_email", user_email)
    
    cnt = Users_dao().mymerge_kakao(user_id, user_nm, user_email) ##
    
    mngr_flag = ''
    msg = ""
    if cnt == 1:
        list = Users_dao().my_kakao_login(user_id)
        pwd = list[0]["user_password"]
        session["user_id"] = user_id
        session["user_nm"] = user_nm
#         mngr_flag = list[0]['mngr_flag']
        msg = "ok"
    else:
        msg = "ng"
    

    return jsonify(msg = msg, mngr_flag = mngr_flag, pwd = pwd)

####################################################################
@app.route('/')
def front_render():
    flag_ses, user_id = getSession()
    
    return render_template('front.html')

@app.route('/main') 
def main_render():
    flag_ses, user_id = getSession()
    
    movie_obj = Movie_dao()
    movies = movie_obj.select_all()
    
    bkmk_obj = Bkmk_dao()
    bkmks = bkmk_obj.select_all(user_id)
    
    return render_template('main.html', movies = movies, bkmks= bkmks)

@app.route('/logout') 
def logout_render():
    session.clear()
    return redirect('main')

@app.route('/layout_admin') 
def logout_admin_render():
    session.clear()
    return redirect('admin')

@app.route('/customer_reco') 
def customer_reco_render(): 
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect('login')
    
    reco_obj = Reco_dao()
    movies = reco_obj.select_reco(user_id)
    
    bkmk_obj = Bkmk_dao()
    bkmks = bkmk_obj.select_bkmk(user_id)
    
    msg = ''
    if movies:
        msg = 'ok'
    else:
        msg = 'ng'
    
    return render_template('customer/customer_reco.html', movies = movies, bkmks = bkmks, msg = msg)

@app.route('/customer_HOT10') 
def customer_HOT10_render():
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect('login')
    
    movie_obj = Movie_dao()
    movies = movie_obj.select_ten()
    
    bkmk_obj = Bkmk_dao()
    bkmks = bkmk_obj.select_bkmk(user_id)
    
    return render_template('customer/customer_HOT10.html', movies = movies, bkmks = bkmks)

@app.route('/customer_bkmk') 
def customer_bkmk_render(): 
    
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect('login')
    
    bkmk_obj = Bkmk_dao()
    movies = bkmk_obj.select_all(user_id)
    bkmks = bkmk_obj.select_bkmk(user_id)
    
    return render_template('customer/customer_bkmk.html', movies = movies, bkmks = bkmks)

@app.route('/service_faq') 
def service_faq_render(): 
    list = faqDAO().myselect_list()
    return render_template('service/service_faq.html',list=list, len = len)

@app.route('/service_faq_detail') 
def service_faq_detail_render(): 
    faq_no = request.args.get('faq_no')
    obj = faqDAO().myselect(faq_no)
    return render_template('service/service_faq_detail.html',faq = obj)

################################################################
@app.route('/download')
def download():
    attach_path = request.args.get("attach_path")
    attach_file = request.args.get("attach_file")
    
    file_name = DIR_UPLOAD+"/"+attach_path
    return send_file(file_name, mimetype='image/png', attachment_filename=attach_file, as_attachment=True)
#################################################################

@app.route('/service_notice') 

def service_notice_render(): 
    
    list = NoticeDao().myselect_list()
    return render_template('service/service_notice.html', list=list, len = len)


@app.route('/notice_detail')
def notice_detail_render():
    notice_no = request.args.get('notice_no')
    obj = NoticeDao().myrdcnt(notice_no)    
    obj = NoticeDao().myselect(notice_no)
     
    return render_template("service/service_notice_detail.html",notice = obj)

@app.route('/notice_del.ajax', methods=['POST'])
def notice_del_ajax():
    flag_ses, user_id = getSession()
    notice_no = request.form['notice_no']
    cnt = NoticeDao().mydel_img(user_id,notice_no)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
    else : 
        msg = "ng"
    
    return jsonify(msg = msg)

################################################################

@app.route('/service_qna') 
def service_qna_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
    return render_template('service/service_qna.html', user_id=user_id)

@app.route('/service_qna_one') 
def service_qna_one_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
    list = Qestn_dao().myselect_qnalist(user_id)
    return render_template('service/service_qna_one.html', list=list)

@app.route('/service_qna_add') 
def service_qna_add_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")  
    return render_template('service/service_qna_add.html', user_id=user_id, enumerate=enumerate)

@app.route('/service_qna_addact', methods=['POST']) 
def service_qna_addact_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
    title = request.form["title"]
    content = request.form["content"]
    answer = " "
    writer = " "
    cnt = Qestn_dao().myinsert('', user_id, title, content, answer, writer)
    return render_template('service/service_qna_addact.html',cnt=cnt,enumerate=enumerate)

@app.route('/service_qna_detail') 
def service_qna_detail_render(): 
    qestn_no = request.args.get("qestn_no")
    
    daoqestn = Qestn_dao()
    obj = daoqestn.myselect(qestn_no)
    return render_template('service/service_qna_detail.html', qestn=obj, enumerate=enumerate)

@app.route('/qestn_del.ajax', methods=['POST']) 
def qestn_del_ajax():
    qestn_no = request.form["qestn_no"]
    cnt = Qestn_dao().mydelete(qestn_no)
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"
    return jsonify(msg=msg)

@app.route('/genre') 
def genre_render():
    movie_obj = Movie_dao()         
    movies = movie_obj.select_all()
    
    flag_ses, user_id = getSession()
    
    bkmk_obj = Bkmk_dao()
    if not flag_ses:
        bkmks = bkmk_obj.select_bkmk('')
    else:
        bkmks = bkmk_obj.select_bkmk(user_id)
        
    genre_obj = Genre_dao()
    genres = genre_obj.select_all()
    
    nation_obj = Nation_dao()
    nations = nation_obj.select_all()
    
    return render_template('genre.html',
                            movies = movies,
                            bkmks = bkmks,
                            genres = genres,
                            nations = nations)

@app.route('/service_community') 
def comunity_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")

    list = MyDaoCommunity().myselect_list()

    return render_template('service/service_community.html', list=list, len = len, enumerate = enumerate)

@app.route('/community_search.ajax', methods=['POST']) 
def community_search_ajax(): 
    target = request.form["target"]
    
    list = MyDaoCommunity().my_search(target)
    
    return jsonify(list = list)

@app.route('/community_add') 
def community_add_render(): 
    return render_template('service/service_community_add.html')

@app.route('/community_ins', methods=['POST'])
def community_ins_render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
    
    title = request.form["title"]
    content = request.form["content"]
    writer = request.form["writer"]
    
    file = request.files['file']        
    attach_file_temp = secure_filename(file.filename)
    attach_path_temp = str(datetime.today().strftime("%Y%m%d%H%M%S")) + "_" + attach_file_temp  
    file.save(os.path.join(DIR_UPLOAD, attach_path_temp))
    
    attach_path = ""
    attach_file = ""
    if file:
        attach_file = attach_file_temp
        attach_path = attach_path_temp 
        print("file O")
    else:
        print("file X")
        
    commdao = MyDaoCommunity()
    cnt = commdao.myinsert(user_id, title, content, attach_file, attach_path, writer)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
    else: 
        msg = "ng"
    
    return redirect("/service_community")

@app.route('/community_detail') 
def community_detail_render():
    bbs_no = request.args.get('bbs_no')
    commdao = MyDaoCommunity()
    shows = commdao.myselect(bbs_no)
    # 여기에 조회수 클릭하면 올라가는 것 만들기
    commdao.rdcntUp(bbs_no)
    
    return render_template('service/service_community_detail.html', shows=shows, enumerate=enumerate)

@app.route('/community_mod') 
def community_mod_render():
    flag_ses, user_id = getSession()
    
    bbs_no = request.args.get('bbs_no')
    
    commdao = MyDaoCommunity()
    shows = commdao.myselect(bbs_no)
    
    return render_template('service/service_community_mod.html', bbs_no = shows, shows = shows, enumerate=enumerate)

 
@app.route('/community_del', methods=['POST'])
def community_del_render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")    
    
    bbs_no = request.form["bbs_no"]
    
    cnt = MyDaoCommunity().mydelete_bbsReply(bbs_no)
    cnt2 = MyDaoCommunity().mydelete(bbs_no)
    
    msg = ""
    if cnt2 > 0:
        msg = 'ok'
    else:
        msg = 'no'

    return jsonify(msg = msg)


@app.route('/community_del.ajax', methods=['POST'])
def community_del_ajax():
    flag_ses, user_id = getSession()
    bbs_no = request.form["bbs_no"]
    cnt = MyDaoCommunity().mydel_img(user_id, bbs_no)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
    else : 
        msg = "ng"
    
    return jsonify(msg = msg)


@app.route('/bbs_mod', methods=['POST']) 
def bbs_mod_render():
    
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
    
    bbs_no = request.form["bbs_no"]
        
    daobbs = MyDaoCommunity()
    cnt = daobbs.myselect(bbs_no)
    
    return redirect('/service_community')

@app.route('/bbs_modact', methods=['POST']) 
def bbs_modact_render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")

    bbs_no = request.form["bbs_no"]
    
    title = request.form["title"]
    content = request.form["content"]
    file = request.files['file']        
    
    if file :
        attach_file_temp = secure_filename(file.filename)
        attach_path_temp = str(datetime.today().strftime("%Y%m%d%H%M%S")) +"_"+ attach_file_temp  
        file.save(os.path.join(DIR_UPLOAD, attach_path_temp))
    
        print("__attach_file_temp",attach_file_temp)
        print("__attach_path_temp",attach_path_temp)

        attach_file = ""
        attach_path = ""
        
        attach_file = attach_file_temp
        attach_path = attach_path_temp 
        print("file O")
        
    else:
        attach_file = ""
        attach_path = ""
        
        print("file X")
    
    daobbs = MyDaoCommunity()
    cnt = daobbs.myupdate(bbs_no, user_id, title, content, attach_file, attach_path)
    
    return render_template('service/service_community_modact.html', cnt=cnt, bbs_no = bbs_no, enumerate = enumerate)

@app.route('/reply_list.ajax', methods=['POST'])
def reply_list_ajax():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")    
    
    bbs_no = request.form["bbs_no"]
    
    list = MyDaoReply().myselect(bbs_no)

    return jsonify(list = list)

@app.route('/reply_del.ajax', methods=['POST'])
def reply_del_ajax():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")    
    
    comm_no = request.form["comm_no"]
    
    list = MyDaoReply().mydelete(comm_no)

    return jsonify(list = list)

@app.route('/reply_write.ajax', methods=['POST']) 
def reply_write_ajax(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
    
    bbs_no = request.form["bbs_no"]
    content = request.form["content"]
    
    replydao = MyDaoReply()
    cnt = replydao.myinsert(bbs_no, content, user_id)

    msg = ""
    if cnt > 0:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)

@app.route('/reply_likes.ajax', methods=['POST'])
def reply_likes__render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login.html")    
    
    comm_no = request.form["comm_no"]
    user_id = request.form["user_id"]
    like_yn = request.form["like_yn"]
    
    cnt = MyDaoReply().likesUp(comm_no, user_id, like_yn)

    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)

@app.route('/reply_dislike', methods=['POST'])
def reply_dislike_render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login.html")    
    
    comm_no = request.form["comm_no"]
    
    cnt = MyDaoReply().dislikeUp(comm_no)

    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)


@app.route('/pick2') 
def pick2_render(): 
    return render_template('pick2.html')

@app.route('/id') 
def id_render(): 
    return render_template('id.html')

@app.route('/find_id.ajax', methods= ['POST']) 
def find_id_ajax(): 
    user_nm = request.form['user_nm']
    user_email = request.form['user_email']
    
    user_obj = Users_dao()
    id = user_obj.find_id(user_nm, user_email)
    
    msg = ''
    if len(id) > 0:
        msg = 'ok'
    else:
        msg = 'ng'
        
    return jsonify(id = id, msg = msg)

@app.route('/pwd') 
def pwd_render(): 
    return render_template('pwd.html')

@app.route('/find_pwd.ajax', methods= ['POST']) 
def find_pwd_ajax(): 
    user_id = request.form['user_id']
    user_email = request.form["user_email"]

    user_obj = Users_dao()
    id = user_obj.find_pwd(user_id, user_email)

    msg = ''
    if id:
        msg = 'ok'
        result = MyMail().mysendmail(user_email, "NETFLEX 임시 비밀번호입니다.")
        cnt = user_obj.find_pwd2(result, user_id)        
        return jsonify(msg = msg)

    else:
        msg = 'ng'
        return jsonify(msg = msg)
    
#     
#     

@app.route('/admin') 
def admin_render(): 
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect("login")
    
    return render_template('admin/main_admin.html')

@app.route('/movie_admin') 
def movie_admin_render():
    movie_obj = Movie_dao()
    movies = movie_obj.select_all_admin()
    
    return render_template('admin/movie_admin.html', movies = movies)

@app.route('/movie_search.ajax', methods=['POST']) 
def movie_search_ajax():
    flag_ses, user_id = getSession()
    
    target = request.form['target']
    
    movie_obj = Movie_dao()
    movies = movie_obj.select_search(target)
    
    bkmk_obj = Bkmk_dao()
    bkmks = bkmk_obj.select_bkmk(user_id)
    
    return jsonify(movies = movies, bkmks = bkmks)

@app.route('/movie_detail') 
def movie_detail_render():
    movie_no = request.args.get('movie_no')
    
    movie_obj = Movie_dao()
    movies = movie_obj.select_one(movie_no)
    genre_obj = Genre_dao()
    genres = genre_obj.select_all()
    
    nation_obj = Nation_dao()
    nations = nation_obj.select_all()
    
    return render_template('admin/movie_detail.html', movies = movies, genres = genres, nations = nations)

@app.route('/movie_add') 
def movie_add_render():
    genre_obj = Genre_dao()
    genres = genre_obj.select_all()
    
    nation_obj = Nation_dao()
    nations = nation_obj.select_all()
    
    return render_template('admin/movie_add.html', genres = genres, nations = nations)

@app.route('/movie_add_act', methods=['POST']) 
def movie_add_act():
    flag_ses, user_id = getSession()
   
    genre_code   = request.form['genre_code']
    nation_code  = request.form['nation_code']
    title        = request.form['title']
    director     = request.form['director']
    actor        = request.form['actor']
    runtime      = request.form['runtime']
    release_date = request.form['release_date']
    url          = request.form['url']  
    in_user_id   = user_id
    
    file         = request.files['poster']
    poster = ''
    if file:
        poster = TIME + '_' + secure_filename(file.filename)
        file.save(os.path.join('D:/workspace_python/WAFLEX/server/static/img', poster))
        
    movie_obj = Movie_dao()
    cnt = movie_obj.insert(genre_code, nation_code, title, director, actor, runtime, release_date, poster, url, in_user_id, user_id)
    
    if cnt:
        flash('정상적으로 추가되었습니다.')
    else:    
        flash('추가 도중 문제가 생겼습니다.')
        
    return redirect('movie_admin')

@app.route('/movie_mod_act', methods=['POST']) 
def movie_mod_act():
    flag_ses, user_id = getSession()
   
    movie_no     = request.form['movie_no']   
    genre_code   = request.form['genre_code']
    nation_code  = request.form['nation_code']
    title        = request.form['title']
    director     = request.form['director']
    actor        = request.form['actor']
    runtime      = request.form['runtime']
    release_date = request.form['release_date']
    poster       = request.form['poster']
    url          = request.form['url']  
    up_user_id   = user_id
    
    file         = request.files['file']
    if file:
        poster = TIME + '_' + secure_filename(file.filename)
        file.save(os.path.join('D:/workspace_python/WAFLEX/server/static/img', poster))
    
    movie_obj = Movie_dao()
    cnt = movie_obj.update_all(genre_code, nation_code, title, director, actor, runtime, release_date, poster, url, up_user_id, movie_no)
    
    if cnt:
        flash('정상적으로 수정되었습니다.')
    else:    
        flash('수정 도중 문제가 생겼습니다.')
        
    return redirect('movie_admin')

@app.route('/movie_del.ajax', methods=['POST']) 
def movie_del_ajax():
    movie_no     = request.form['movie_no']   
    
    movie_obj = Movie_dao()
    cnt = movie_obj.delete(movie_no)
    
    msg = ''
    if cnt:
        msg = 'ok'
    else:    
        msg = 'ng'
        
    return jsonify(msg = msg)

@app.route('/genre_admin')
def genre_admin_render():
    genre_obj = Genre_dao()
    genres = genre_obj.select_all()
    
    return render_template('admin/genre_admin.html', genres = genres)

@app.route('/genre_detail') 
def genre_detail_render():
    genre_code = request.args.get('genre_code')
    
    genre_obj = Genre_dao()
    genres = genre_obj.select_one(genre_code)
    
    return render_template('admin/genre_detail.html', genres = genres)

@app.route('/genre_add') 
def genre_add_render(): 
    return render_template('admin/genre_add.html')

@app.route('/genre_add.ajax', methods=['POST']) 
def genre_add_ajax():
    flag_ses, user_id = getSession()
    
    genre_code = request.form['genre_code']
    name       = request.form['name']
    in_user_id = user_id
    
    genre_obj = Genre_dao()
    cnt = genre_obj.insert(genre_code, name, in_user_id)
    
    msg = ''
    if cnt:
        msg = 'ok'
    else:    
        msg = 'ng'
        
    return jsonify(msg = msg)

@app.route('/genre_mod.ajax', methods=['POST']) 
def genre_mod_ajax():
    flag_ses, user_id = getSession()
    
    genre_code     = request.form['genre_code']
    name     = request.form['name']
    
    genre_obj = Genre_dao()
    cnt = genre_obj.update(genre_code, name, user_id)
    
    msg = ''
    if cnt:
        msg = 'ok'
    else:    
        msg = 'ng'
        
    return jsonify(msg = msg)

@app.route('/genre_del.ajax', methods=['POST']) 
def genre_del_ajax():
    genre_code = request.form['genre_code']
    
    genre_obj = Genre_dao()
    cnt = genre_obj.delete(genre_code)
    
    msg = ''
    if cnt:
        msg = 'ok'
    else:    
        msg = 'ng'
        
    return jsonify(msg = msg)

@app.route('/nation_admin')
def nation_admin_render():
    nation_obj = Nation_dao()
    nations = nation_obj.select_all()
    
    return render_template('admin/nation_admin.html', nations = nations)

@app.route('/nation_detail') 
def nation_detail_render():
    nation_code = request.args.get('nation_code')
    
    nation_obj = Nation_dao()
    nations = nation_obj.select_one(nation_code)
    
    return render_template('admin/nation_detail.html', nations = nations)

@app.route('/nation_add') 
def nation_add_render(): 
    return render_template('admin/nation_add.html')

@app.route('/nation_add.ajax', methods=['POST']) 
def nation_add_ajax():
    flag_ses, user_id = getSession()
    
    nation_code = request.form['nation_code']
    name       = request.form['name']
    in_user_id = user_id
    
    nation_obj = Nation_dao()
    cnt = nation_obj.insert(nation_code, name, in_user_id)
    
    msg = ''
    if cnt:
        msg = 'ok'
    else:    
        msg = 'ng'
        
    return jsonify(msg = msg)

@app.route('/nation_mod.ajax', methods=['POST']) 
def nation_mod_ajax():
    flag_ses, user_id = getSession()
    
    nation_code     = request.form['nation_code']
    name     = request.form['name']
    
    nation_obj = Nation_dao()
    cnt = nation_obj.update(nation_code, name, user_id)
    
    msg = ''
    if cnt:
        msg = 'ok'
    else:    
        msg = 'ng'
        
    return jsonify(msg = msg)

@app.route('/nation_del.ajax', methods=['POST']) 
def nation_del_ajax():
    nation_code = request.form['nation_code']
    
    nation_obj = Nation_dao()
    cnt = nation_obj.delete(nation_code)
    
    msg = ''
    if cnt:
        msg = 'ok'
    else:    
        msg = 'ng'
        
    return jsonify(msg = msg)

@app.route('/user_admin')
def user_admin_render():
    list = Users_dao().myselect()
    
    return render_template('admin/user_admin.html',list=list)

@app.route('/user_search.ajax', methods=['POST'])
def user_search_ajax():
    target = request.form['target']
    
    user_obj = Users_dao()
    users = user_obj.my_search(target)
        
    msg = ''
    if len(users) > 0:
        msg = 'ok'
    else:    
        msg = 'ng'
        
    return jsonify(users = users, msg = msg)

@app.route('/payment_admin') 
def payment_admin_render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
    
    pymt_obj = Payment_dao()
    pymts = pymt_obj.select_all()
    
    cnt = 0
    total = 0
    for i in pymts:
        cnt += 1
        total += i['price']
    
    return render_template('admin/payment_admin.html', pymts = pymts, cnt = cnt, total = total)

@app.route('/community_admin') 
def service_community_admin_render(): 
    return render_template('admin/community_admin.html')

@app.route('/qna_admin') 
def service_qna_admin_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
    qest_no= request.args.get('qestn_no') 
    list = Qestn_dao().myselect_list()
    return render_template('admin/qna_admin.html', list=list)

@app.route('/qna_detail_admin') 
def qna_detail_admin_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
    qestn_no = request.args.get("qestn_no")
    obj = Qestn_dao().myselect(qestn_no)
    return render_template('admin/qna_detail_admin.html',qestn=obj, enumerate=enumerate)

@app.route('/qestn_upd.ajax', methods=['POST']) 
def qestn_upd_ajax():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
    qestn_no = request.form["qestn_no"]
    answer = request.form["answer"]
    up_date = request.form["up_date"]
    writer = user_id
    cnt = Qestn_dao().myupdate_answer(qestn_no, user_id, answer, up_date, writer)
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"
    return jsonify(msg=msg)

@app.route('/del_answer.ajax', methods=['POST']) 
def del_answer_ajax():
    qestn_no = request.form["qestn_no"]
    cnt = Qestn_dao().mydel_answer(qestn_no)
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"
    return jsonify(msg=msg)

@app.route('/notice_admin') 
def service_notice_admin_render(): 
    notice_no= request.args.get('notice_no') 
    list = NoticeDao().myselect_list()
    
    return render_template('admin/notice_admin.html', list = list, len = len)

@app.route('/notice_search.ajax', methods=['POST']) 
def notice_search_ajax(): 
    target = request.form["target"]
    
    notice_obj = NoticeDao()
    notices = notice_obj.my_search(target)
    
    return jsonify(notices = notices)

@app.route('/notice_detail_admin') 
def notice_detail_admin_render(): 
    
    notice_no = request.args.get('notice_no')
    
    obj_rdcnt = NoticeDao().myrdcnt(notice_no)    
    obj = NoticeDao().myselect(notice_no)
    
    return render_template('admin/notice_detail_admin.html',notice = obj)

@app.route('/notice_add_admin') 
def notice_add_admin_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
        
    notice_no = request.args.get('notice_no')
    obj = NoticeDao().myselect(notice_no)
    return render_template('admin/notice_add_admin.html')
 
@app.route('/notice_addact_admin', methods=['POST']) 
def notice_addact_admin_render(): 
    flag_ses, user_id = getSession()
    
    title = request.form["title"]
    content = request.form["content"]
    file = request.files['file']
    
    
    attach_path = ""
    attach_file = ""
    if file:
        attach_file = secure_filename(file.filename)
        attach_path = TIME +'_'+ attach_file
        file.save(os.path.join(DIR_UPLOAD, attach_path))
 
    cnt = NoticeDao().myinsert(user_id, title, content, attach_file, attach_path,  user_id,  user_id)
    
    if cnt:
        flash('정상적으로 추가되었습니다.')
    else:    
        flash('추가 도중 문제가 생겼습니다.')
    
    return redirect('notice_admin')

@app.route('/notice_mod_admin') 
def notice_mod_admin_render(): 
    flag_ses, user_id = getSession()
    notice_no = request.args.get('notice_no')
    obj = NoticeDao().myselect(notice_no)
    
    return render_template('admin/notice_mod_admin.html',notice=obj,enumerate=enumerate)
 
@app.route('/notice_modact_admin', methods=['POST']) 
def notice_modact_admin_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
 
    notice_no = request.form["notice_no"]
    title = request.form["title"]
    content = request.form["content"]
    
    
    attach_file_old = request.form["attach_file"]
    attach_path_old = request.form["attach_path"]
    
    if attach_file_old == "None":
        attach_file_old = ""
        attach_path_old = ""
    
    file = request.files['file']
    attach_file_temp = secure_filename(file.filename)
    attach_path_temp = str(datetime.today().strftime('%Y%m%d%H%M%S')) +'_'+ attach_file_temp  
    file.save(os.path.join(DIR_UPLOAD, attach_path_temp))
    
    obj = NoticeDao().myselect(notice_no)
    attach_file = obj.get('attach_file', '')
    attach_path = obj.get('attach_path', '')
    attach_path = ""
    attach_file = ""
    if file :
        attach_file = attach_file_temp
        attach_path = attach_path_temp
        print('file O')
    else :
        attach_file = attach_file_old
        attach_path = attach_path_old
        print('file X')
         
    cnt = NoticeDao().myupdate(notice_no,user_id,title,content,attach_file,attach_path,None,None,user_id,None,user_id)
    return render_template('admin/notice_modact_admin.html',cnt=cnt,enumerate=enumerate,notice_no=notice_no)

@app.route("/notice_delact_admin")
def notice_delact_render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")    
    
    notice_no = request.args.get("notice_no")
    cnt = NoticeDao().mydelete(notice_no)
    
    return render_template('admin/notice_delact_admin.html',cnt=cnt,enumerate=enumerate)



##################################################################################
@app.route('/faq_admin') 
def service_faq_admin_render():
    list = faqDAO().myselect_list()
    return render_template('admin/faq_admin.html', list=list, len=len) 

@app.route('/faq_add_admin') 
def faq_add_admin_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
        
    faq_no = request.args.get('faq_no')
    obj = faqDAO().myselect(faq_no)
    return render_template('admin/faq_add_admin.html')

@app.route('/faq_addact_admin', methods=['POST']) 
def faq_addact_admin_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
        
    title = request.form["title"]
    content = request.form["content"]
    
    cnt = faqDAO().myinsert(user_id,title,content,user_id,user_id,user_id)
    return render_template('admin/faq_addact_admin.html',cnt=cnt,enumerate=enumerate)

@app.route('/faq_detail_admin')
def faq_detail_adminfaq_add_admin_render(): 
    faq_no = request.args.get('faq_no')
    obj = faqDAO().myselect(faq_no)
    return render_template('admin/faq_detail_admin.html',faq = obj)



@app.route('/faq_mod_admin') 
def faq_mod_admin_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
        
    faq_no = request.args.get('faq_no')
    obj = faqDAO().myselect(faq_no)
    return render_template('admin/faq_mod_admin.html',faq=obj,enumerate=enumerate)
 
@app.route('/faq_modact_admin', methods=['POST']) 
def faq_modact_admin_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")
    faq_no = request.form["faq_no"]
    title = request.form["title"]
    content = request.form["content"]
    obj = faqDAO().myselect(faq_no)
  
    cnt = faqDAO().myupdate(faq_no,user_id, title, content, None, None, user_id, None, user_id)
    return render_template('admin/faq_modact_admin.html',cnt=cnt,enumerate=enumerate,faq_no=faq_no)

@app.route("/faq_delact_admin")
def faq_delact_render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")    
    
    faq_no = request.args.get("faq_no")
    cnt = faqDAO().mydelete(faq_no)
    
    return render_template('admin/faq_delact_admin.html',cnt=cnt,enumerate=enumerate)




##################################################################################

@app.route('/service_notice_detail') 
def service_notice_detail_render(): 
    return render_template('service/service_notice_detail.html')

@app.route('/service_notice_modify') 
def service_notice_modify(): 
    return render_template('service/service_notice_modify.html')
    
@app.route('/service_notice_write') 
def notice_detail2_render(): 
    return render_template('service/service_notice_write.html')


################################## 이용권 ################################################################
@app.route('/voucher') 
def voucher_render(): 
    return render_template('voucher.html')

@app.route('/payment') 
def payment(): 
    return render_template('payment.html')

@app.route("/kakaopay/paymethod.ajax", methods=['POST'])
def paymethod_render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login") 
    if request.method == 'POST':
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            'Authorization': "KakaoAK " + "Authorization",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        params = {
            "cid": "TC0ONETIME", 
            "partner_order_id": "1001",  
            "partner_user_id": user_id,  
            "item_name": "WAFLEX 이용권", 
            "quantity": 1, 
            "total_amount": 12500, 
            "tax_free_amount": 0,  
            "vat_amount" : 200,
            "approval_url": "http://127.0.0.1:5001/kakaopay/success",
            "cancel_url": "http://127.0.0.1:5001/kakaopay/cancel",
            "fail_url": "http://127.0.0.1:5001/kakaopay/fail"
        }

        res = requests.post(URL, headers=headers, params=params)
        app.tib = res.json()['tid']  # 결제 승인시 사용할 tid를 세션에 저장

        return jsonify({'next_url': res.json()['next_redirect_pc_url']})

    return render_template('voucher.html') 


@app.route("/kakaopay/success", methods=['POST', 'GET'])
def success_render():
    flag_ses, user_id = getSession()

    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "Authorization",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    params = {
        "cid": "TC0ONETIME",  # 테스트용 코드
        "tid": app.tib,  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1001",  # 주문번호
        "partner_user_id": user_id,  # 유저 아이디
        "pg_token": request.args.get("pg_token")  # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    print(res.text)
    print(res.json())
    print(res.json()['amount'])
    print(res.json()['amount']['total'])
    amount = res.json()['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount
    }
    
    pymt_obj = Payment_dao()
    cnt = pymt_obj.merge_payment(user_id, '1')
    
    if cnt > 0:
        pymts = pymt_obj.check(user_id, '1')
        session["payment_flag"] = pymts[0]['payment_flag']
    
    return render_template('pay_success.html', context = context, res = res)

@app.route("/kakaopay/cancel", methods=['POST', 'GET'])
def cancel_render():
    URL = "https://kapi.kakao.com/v1/payment/order"
    headers = {
        "Authorization": "KakaoAK " + "Authorization",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    params = {
        "cid": "TC0ONETIME",  # 가맹점 코드
        "tid": app.tib  # 결제 고유 코드
    }

    res = requests.post(URL, headers=headers, params=params)
    print(res.text)
    amount = res.json()['cancel_available_amount']['total']

    context = {
        'res': res,
        'cancel_available_amount': amount
    }
    
    if res.json()['status'] == "QUIT_PAYMENT":
        res = res.json()
        return render_template('pay_cancel.html', params = params, res = res, context = context)


@app.route("/kakaopay/fail", methods=['POST', 'GET'])
def fail_render():
    return render_template('pay_fail.html')




########################################################################################################

################################################ 회 원 가 입 ##############################################


@app.route('/sign.ajax', methods=['POST'])
def sign_ajax_render():
    user_id = request.form["user_id"]
    user_nm = request.form["user_nm"]
    user_password = request.form["user_password"]
    user_telno = request.form["user_telno"]
    user_email = request.form["user_email"]
    
    print(user_id)
    
    user_obj = Users_dao()
    cnt = user_obj.myinsert(user_id, user_nm, user_password, user_telno, user_email, "", "", "", user_id, "", user_id)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)



@app.route('/sign_sms.ajax', methods=['POST'])
def sign_sms_ajax():
    user_telno = request.form["user_telno"]
    
    result = MySms().mysendsms(user_telno)

    return jsonify(result = result)


@app.route('/sign_mail.ajax', methods=['POST'])
def sign_mail_ajax():

    user_email = request.form["user_email"]
    
    result = MyMail().mysendmail(user_email, "WAFLEX 인증메일입니다.")

    return jsonify(result = result)


# 중복체크
@app.route('/dupl.ajax', methods=['POST'])
def dupl_ajax_render():
    user_id = request.form["user_id"]
    
    print("user_id",user_id)
    
    user_obj = Users_dao()
    list = user_obj.mydupl(user_id)

    msg = ""
    if len(list) == 1:
        msg = "ng"
    else:
        msg = "ok"

    return jsonify(msg = msg)

########################################################################################################
################################################ 마 이 페 이 지 ##############################################
@app.route('/user_my_page')
def user_my_page_render():
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect('login')
    
    user_obj = Users_dao()
    infos = user_obj.my_info(user_id)

    return render_template('user/user_my_page.html', infos = infos)

@app.route('/user_detail')
def user_detail_render():
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect('login')
    
    user_obj = Users_dao()
    infos = user_obj.my_info(user_id)

    return render_template('user/user_detail.html', infos = infos)

@app.route('/user_mod', methods=['POST'])
def user_mod():
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect('login')
    
    user_id = request.form['user_id']
    user_nm = request.form['user_nm']
    user_password = request.form['user_password']
    user_telno = request.form['user_telno']
    user_email = request.form['user_email']
    
    user_telno = re.sub('[^0-9]+', '', user_telno)
    
    user_obj = Users_dao()  
    cnt = user_obj.my_update(user_nm, user_password, user_telno, user_email, user_id)
    infos = user_obj.my_info(user_id)
    
    msg = ''
    if cnt > 0:
        msg = 'ok'
    else:
        msg = 'ng'    

    return render_template('user/user_my_page.html', infos = infos, msg = msg)

@app.route('/user_del.ajax', methods=['POST'])
def user_del_ajax():
    user_id = request.form['user_id']
    
    user_obj = Users_dao()
    cnt = user_obj.my_delete(user_id)
    
    msg = ''
    if cnt > 0:
        msg = 'ok'
    else:
        msg = 'ng'    

    return jsonify(msg = msg)

@app.route('/user_my_evl')
def user_my_evl_render():
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect('login')
    
    evl_obj = Evl_dao()
    movies = evl_obj.select_evl(user_id)
    
    return render_template('user/user_my_evl.html', movies = movies, enumerate = enumerate)

@app.route('/user_rate.ajax', methods=['POST'])
def user_rate_ajax():
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect('login')
    
    movie_no = request.form['movie_no']
    title = request.form['title']
    rate = request.form['rate']
    
    evl_obj = Evl_dao()
    cnt = evl_obj.update(rate, user_id, movie_no)
    
    msg = ''
    if cnt > 0:
        msg = 'ok'
    else:
        msg = 'ng'
        
    rc = reco_algo()        
    result = rc.recommend(title, rc.matrix, 10, similar_genre = True)
    
    if result:
        reco_obj = Reco_dao()
        reco_obj.delete(user_id)
        
        for re in result:
            #re[0] : 영화제목
            print(re[0])
            reco_obj.insert(user_id, re[0], user_id, user_id)

    return jsonify(msg = msg)


####장르 관련 메서드######################################################################################
@app.route("/movie_sel_list.ajax", methods=['POST'])
def movie_sel_list_ajax():
    flag_ses, user_id = getSession()

    sel_genre = request.form['sel_genre']
    sel_nation = request.form['sel_nation']
    sel_reco = request.form['sel_reco']
    
    if sel_genre == 'all':
        sel_genre = ''
    if sel_nation == 'all':
        sel_nation = ''
    
    movie_obj = Movie_dao()
    movies = movie_obj.select_list(sel_genre, sel_nation, sel_reco)
    
    bkmk_obj = Bkmk_dao()
    bkmks = bkmk_obj.select_bkmk(user_id)

    return jsonify(movies = movies, bkmks = bkmks)

@app.route("/movie_stream.ajax", methods=['POST'])
def movie_stream_ajax():
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect('login')
    
    movie_no = str(request.form['movie_no'])
    
    movie_obj = Movie_dao()    
    cnt1 = movie_obj.update_stream_cnt(movie_no)
    
    evl_obj = Evl_dao()
    list = evl_obj.check_vali(user_id, movie_no)
    
    cnt2 = 0
    if not list:
        cnt2 = evl_obj.insert(user_id, movie_no, user_id, user_id)
        
    return jsonify(cnt1 = cnt1, cnt2 = cnt2)

@app.route("/movie_bkmk_add.ajax", methods=['POST'])
def movie_bkmk_add_ajax():
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect('login')
    
    movie_no = request.form['movie_no']
    
    bkmk_obj = Bkmk_dao()
    cnt = bkmk_obj.insert(user_id, movie_no, user_id, user_id)
    
    msg = ''
    if cnt > 0:
        msg = 'ok'
    else:
        msg = 'ng'
    

    return jsonify(msg = msg)

@app.route("/movie_bkmk_del.ajax", methods=['POST'])
def movie_bkmk_del_ajax():
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect('login')
    
    movie_no = request.form['movie_no']
    
    bkmk_obj = Bkmk_dao()
    cnt = bkmk_obj.delete(user_id, movie_no)
    
    msg = ''
    if cnt > 0:
        msg = 'ok'
    else:
        msg = 'ng'

    return jsonify(msg = msg)

############################################ 관리자 - 이용권 ###############################################

@app.route('/ticket_admin') 
def ticket_admin_render(): 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")    
    
    user_id = str(escape(session["user_id"]))
    
    obj = Ticket_dao().myselect_all()
    
    return render_template('admin/ticket_admin.html', ticket=obj, len = len)

@app.route('/ticket_detail') 
def ticket_detail_render(): 
    flag_ses, user_id = getSession()
    
    if not flag_ses:
        return redirect("login.html")    
    
    ticket_no = request.args.get('ticket_no') 
    obj = Ticket_dao().myselect(ticket_no)
    print(obj)
    return render_template('admin/ticket_detail.html', ticket=obj, enumerate=enumerate)

@app.route('/ticket_add') 
def ticket_add_render():     
     return render_template('admin/ticket_add.html')

@app.route("/ticket_addact", methods=['POST'])
def ticket_addact_render():
 
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login.html")   
     
    ticket_no = request.form["ticket_no"]
    name = request.form["ticket_name"]
    price = request.form["ticket_price"]
 
    cnt = Ticket_dao().myinsert('', name, price, None, user_id, None, user_id)
 
    return render_template('admin/ticket_addact.html', cnt=cnt, enumerate=enumerate)

@app.route("/ticket_delact")
def ticket_delact_render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login.html")    
    
    ticket_no = request.args.get('ticket_no')
    cnt = Ticket_dao().mydelete(ticket_no)
 
    return render_template('admin/ticket_delact.html', cnt=cnt)


@app.route('/ticket_ins.ajax', methods=['POST'])
def ticket_ins_ajax():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login.html")   
    
    ticket_no = request.form["ticket_no"]
    name = request.form["ticket_name"]
    price = request.form["ticket_price"]

    cnt = Ticket_dao().myinsert(name, price, user_id, user_id)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)

@app.route('/ticket_upd.ajax', methods=['POST'])
def ticket_upd_ajax():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login.html")  
    
    ticket_no = request.form["ticket_no"]
    name = request.form["ticket_name"]
    price = request.form["ticket_price"]
    
    
#     print("ticket_no",ticket_no)
    print("name",name)
    print("price",price)
    print("user_id",user_id)
    
    cnt = Ticket_dao().myupdate(ticket_no, name, price, "", user_id, "", user_id)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)


@app.route('/ticket_del.ajax', methods=['POST'])
def ticket_del_ajax():
    ticket_no = request.form["ticket_no"]

    cnt = Ticket_dao().mydelete(ticket_no)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)

#####################################################################################################

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', port=5001, debug=True)
    
    