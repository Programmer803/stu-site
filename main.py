
erreor="""
        <html>
        <head>
        <style>
        .eror{
                position:relative;
                vertical-align:middle;
                color:red;
                top:0%;
                font-size:300%;
                
                
                border: 10px solid blue;
                border-radius:30px;
                place-items: center;
                background-color:#66a946;
       
        }

        div{
            top:1%;
            right:2%;
            
        }

        body{
            display: flex;
            left:50%;
            
            justify-content: center;
        }






        </style>




        </head>
        <body>
        
        
         <div>
         <p class="eror">نام تکراری می باشد</p> 
         </div>
         </body>

         </html>
        """




from math import exp
from flask import Flask,request,render_template,url_for,make_response,session,redirect
from flask_sqlalchemy import *
from random import randint
import os
from hashlib import *




app = Flask(__name__)
dir = os.path.dirname(__file__)
route=os.path.join(dir,"login.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+route
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

# *********************************data_base*****************************************    
class User(db.Model):
    
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    password = db.Column(db.String(100))
    clas = db.Column(db.String(100))
    data = db.Column(db.String(100))
    def __repr__(self):
        return self.password
class User_paragraf(db.Model):
    key = db.Column(db.Integer , primary_key=True)
    data = db.Column(db.Text)
    name_article_href=db.Column(db.Text)
    def __repr__(self):
        return self.data
class User_article(db.Model):
    key = db.Column(db.Integer , primary_key=True)
    data_name = db.Column(db.Text)
    data_link = db.Column(db.Text)
    name_article_href=db.Column(db.Text)
    def __repr__(self):
        return self.data_link
class User_article2(db.Model):
    key = db.Column(db.Integer , primary_key=True)
    data_name = db.Column(db.Text)
    data_link = db.Column(db.Text)
    name_article_href=db.Column(db.Text)
    def __repr__(self):
        return self.data_name  
class User_property(db.Model): 
    key = db.Column(db.Integer , primary_key=True)


# *********************************data_base*****************************************    
class data():
    def __init__(self,password,number):
        password=self.password
        user=self.user
        phone_number = self.number






    
#start search
@app.route("/my-dashbord/search",methods=["POST"])
def search():
    try:
            
        data_search=request.form["data"]
        data_list=str(User_paragraf.query.filter(User_paragraf.data.like(f"%{data_search}%")).first())
        split_data=data_list.split("_")
        link=int(split_data[0])
        id_paragraf=str("http://192.168.1.103:5000/article/{link}".format(link=int(link)))
        title_paragraf=split_data[2]
        topic_paragraf=split_data[1]
        return render_template("Search.html",title=title_paragraf,link=id_paragraf)
    except:
        return render_template("Search.html",title="Not Found")
    
   
   

#-----------------------------------------------------------------------------------------------
#end
db.create_all()
# show article with number article
@app.route("/article/<num>")
def show_article(num):
    
    data=str(User_paragraf.query.filter(User_paragraf.data.like(f"%{num}%")).first())
    data=data.split("_")
    group=data[1]
    title=data[2]
    name=data[3]
    comment=data[4]
    
    return render_template("article_page.html",comment=comment,title=title,name=name,group=group)
# -----------------------------------------------------------------------------------
# make article: get the title - username - text
@app.route("/my-dashbord/make-article")
def make_article():
    pass_d=session.get("password")
    phone_d=session.get("phone_number")
    d_user=str(User.query.filter(User.password.like(f"%{phone_d}%")).first())
    d_user=d_user.split()
    print(pass_d,phone_d,d_user)
    try:
            
        if pass_d==d_user[1] and phone_d==d_user[0]:
            return render_template("send_paragraf.html")

    except:
        return redirect("/sing-up")
# **************************************************
# page dashbord and check the username and password    
@app.route("/my-dashbord")
def my_dashbord():
    number=str(session.get("phone_number"))
    password=session.get("password")
    user=session.get("username")
    data.number = number
    data.user = user
    data.password = password
    d_user=str(User.query.filter(User.password.like(f"%{number}%")).first())
    d_user=d_user.split()
    
    try:
        
        if d_user[1]==password and d_user[0] == number :
            return render_template("dashbord.html",name=user)
        else:
            return redirect("/sing-up")
    except:
        return redirect("/sing-up")
        

# ***************************************************
@app.route('/p')
def p():
    return render_template("send_paragraf.html")
#-----------------------------------------------
# qeustion
@app.route("/my-dashbord/make-question")
def question():
    return render_template("make_quest.html")
# --------------------------------------------------------------------------------------
# grid data article in database
@app.route('/data-article',methods=["POST"])
def p_test():
    comment=request.form["comment"]
    group=request.form["group"]
    title=request.form["title"]
    name=session.get("username")
    id_article=str(id(title)+id(comment))
    data=id_article+"_"+group+"_"+title+"_"+name+"_"+comment
    
    link="http://192.168.1.103:5000/article/{id_article}".format(id_article=id_article)
    n_d=title
    
    db.session.add(User_paragraf(data=data))
    db.session.add(User_article(data_link=link))
    db.session.add(User_article2(data_name=n_d))
    db.session.commit()
    return "link : http://192.168.1.103:5000/article/{id_article}".format(id_article=id_article)
#-------------------------------------------------------------------------------------------------
# about sing-in page
@app.route("/sing",methods=["POST","GET"])
def sing():
    try:
            
        password=request.form["password"]#h
        number=str(request.form["number"])#h
        d_user=str(User.query.filter(User.password.like(f"%{number}%")).first())
        d_user=d_user.split()
        chek_user2=User.query.filter(User.phone==number).scalar()
        print(d_user)
        
        if password==d_user[1] and chek_user2:
            session["phone_number"]=number
            session["password"]=password
            return redirect("/my-dashbord")
    except:
          return"""
           <html>
    <head>
    <style>
    @font-face {
  font-family: myFont;
  src: url(fonts/font.woff) format('woff');
}
@font-face {
font-family: "CustomFont";
src: url("fonts/CustomFont.eot");
src: url("fonts/CustomFont.woff") format("woff"),
url("fonts/CustomFont.otf") format("opentype"),
url("fonts/CustomFont.svg") format("svg");
}
    body{
        justify-content: center;
        place-items: center;
        
        
        display: flex;
       
    
        
    }
    h2 {
        color:#ffffffe8;
        border:0.0001px solid brown;
        background-color:brown;
        font-family: 'CustomFont';
        padding:30px 30px;
        border-radius:10px;
        
        
        
     }

    </style>
    </head>
    <title>Error</title>
    <h2 class="404">نام یا رمز عبور اشتباه می باشد
    </h2>
    
    
    </html>
    """


    

# sing-in if user save the session redirect the page "my-dashbord"
# else redirect to page 
@app.route("/sing-in")
def sing_in():
 
    phone_number=session.get("phone_number")
    password=session.get("password")
    try:
        if password and phone_number:
            return redirect("/my-dashbord")  
        else:

            return render_template("form_singin.html")
    except:
        return render_template("form_singin.html")
        
@app.route('/sing-up')
def form():
    
    return render_template("form.html")
@app.route("/")
def index():
    try:
        # *************************
        # show article in main page
        d_lists=User_article.query.all()
        lens=len(d_lists)
        lens_start=lens-14
        d_list=User_article2.query.all()
        d_article_name=d_list[lens_start:lens]
        d_name_1=d_article_name[0]
        d_name_2=d_article_name[1]
        d_name_3=d_article_name[2]
        d_name_4=d_article_name[3]
        d_name_5=d_article_name[4]
        d_name_6=d_article_name[5]
        d_name_7=d_article_name[6]
        d_name_8=d_article_name[7]
        d_name_9=d_article_name[8]
        d_name_10=d_article_name[9]
        d_name_11=d_article_name[10]
        d_name_12=d_article_name[11]
        d_name_13=d_article_name[12]
        d_name_14=d_article_name[13]
        d_article_link=d_lists[lens_start:lens]
        d_link_1=d_article_link[0]
        d_link_2=d_article_link[1]
        d_link_3=d_article_link[2]
        d_link_4=d_article_link[3]
        d_link_5=d_article_link[4]
        d_link_6=d_article_link[5]
        d_link_7=d_article_link[6]
        d_link_8=d_article_link[7]
        d_link_9=d_article_link[8]
        d_link_10=d_article_link[9]
        d_link_11=d_article_link[10]
        d_link_12=d_article_link[11]
        d_link_13=d_article_link[12]
        d_link_14=d_article_link[13]
      

        
        


            
    

        
        return render_template("index.html",link_1=d_link_1,link_2=d_link_2,link_3=d_link_3,link_4=d_link_4,link_5=d_link_5,link_6=d_link_6,link_7=d_link_7,link_8=d_link_8,link_9=d_link_9,link_10=d_link_10,link_11=d_link_11,link_12=d_link_12,link_13=d_link_13,link_14=d_link_14,name_1=d_name_1,name_2=d_name_2,name_3=d_name_3,name_4=d_name_4,name_5=d_name_5,name_6=d_name_6,name_7=d_name_7,name_8=d_name_8,name_9=d_name_9,name_10=d_name_10,name_11=d_name_11,name_12=d_name_12,name_13=d_name_13,name_14=d_name_14)
    except :    
        return render_template("index.html")

# make data user and make session    
@app.route("/dashbord",methods=["POST"])
def dashbord():
    session.permanent=True
    

    password=request.form["password"]#h
    number=str(request.form["number"])#h
    r_password=request.form["r-password"]
    clas=request.form["clas"]
    names=str(request.form["name"]).strip()#h
    chek_user=User.query.filter(User.name==names).scalar()
    chek_user2=User.query.filter(User.phone==number).scalar()
    if chek_user==None and chek_user2==None and password==r_password and number[0]=="0" and number[1]=="9" and len(number)==11 and int(clas)<12 and int(clas)>0:
        password=request.form["password"]#h
        phone=str(request.form["number"])#h
        r_password=request.form["r-password"]
        clas=request.form["clas"]
        name=str(request.form["name"])#h
        data.clas=clas
        user = User(name=name)
        passwords=number+" "+password
        clas=number+" "+clas
        user_property=User(phone=phone,password=passwords,clas=clas)
        user_id=id(name)
        db.session.add(user_property)
        db.session.add(user)
        db.session.commit()
        session["phone_number"]=number
        session["password"]=password
        session["username"]=name
        session["id_user"]=user_id

        return """           <html>
    <head>
    <style>
    @font-face {
  font-family: myFont;
  src: url(fonts/font.woff) format('woff');
}
@font-face {
font-family: "CustomFont";
src: url("fonts/CustomFont.eot");
src: url("fonts/CustomFont.woff") format("woff"),
url("fonts/CustomFont.otf") format("opentype"),
url("fonts/CustomFont.svg") format("svg");
}
    body{
        justify-content: center;
        place-items: center;
        
        
        display: flex;
       
    
        
    }
    h2 {
        color:#ffffffe8;
        
        background-color:#37538d;
        font-family: 'CustomFont';
        padding:60px 60px;
        border-radius:10px;
        
        
        
     }

    </style>
    </head>
    <title>Successfully</title>
    <h2 class="true"> ثبت نام موفقیت امیز بود
     <a href="/my-dashbord">با کلیک بر اینجا</a>
      وارد داشبورد خود شوید
    </h2>
    
    
    </html>"""
    if int(clas)>12 or int(clas)<0:
         return"""
           <html>
    <head>
    <style>
    @font-face {
  font-family: myFont;
  src: url(fonts/font.woff) format('woff');
}
@font-face {
font-family: "CustomFont";
src: url("fonts/CustomFont.eot");
src: url("fonts/CustomFont.woff") format("woff"),
url("fonts/CustomFont.otf") format("opentype"),
url("fonts/CustomFont.svg") format("svg");
}
    body{
        justify-content: center;
        place-items: center;
        
        
        display: flex;
       
    
        
    }
    h2 {
        color:#ffffffe8;
        border:0.0001px solid brown;
        background-color:brown;
        font-family: 'CustomFont';
        padding:30px 30px;
        border-radius:10px;
        
        
        
     }

    </style>
    </head>
    <title>Error</title>
    <h2 class="404">کلاس نامعتبر است
    </h2>
    
    
    </html>
    """

    if chek_user==None and chek_user2==None and password!=r_password:

        return"""
           <html>
    <head>
    <style>
    @font-face {
  font-family: myFont;
  src: url(fonts/font.woff) format('woff');
}
@font-face {
font-family: "CustomFont";
src: url("fonts/CustomFont.eot");
src: url("fonts/CustomFont.woff") format("woff"),
url("fonts/CustomFont.otf") format("opentype"),
url("fonts/CustomFont.svg") format("svg");
}
    body{
        justify-content: center;
        place-items: center;
        
        
        display: flex;
       
    
        
    }
    h2 {
        color:#ffffffe8;
        border:0.0001px solid brown;
        background-color:brown;
        font-family: 'CustomFont';
        padding:30px 30px;
        border-radius:10px;
        
        
        
     }

    </style>
    </head>
    <title>Error</title>
    <h2 class="404">پسورد ها مطابقت ندارد
    </h2>
    
    
    </html>
    """
    if len(number)!=11 or number[0]!="0" or number[1]!="9":
          return"""
           <html>
    <head>
    <style>
    @font-face {
  font-family: myFont;
  src: url(fonts/font.woff) format('woff');
}
@font-face {
font-family: "CustomFont";
src: url("fonts/CustomFont.eot");
src: url("fonts/CustomFont.woff") format("woff"),
url("fonts/CustomFont.otf") format("opentype"),
url("fonts/CustomFont.svg") format("svg");
}
    body{
        justify-content: center;
        place-items: center;
        
        
        display: flex;
       
    
        
    }
    h2 {
        color:#ffffffe8;
        border:0.0001px solid brown;
        background-color:brown;
        font-family: 'CustomFont';
        padding:30px 30px;
        border-radius:10px;
        
        
        
     }

    </style>
    </head>
    <title>Error</title>
    <h2 class="404">شماره موبایل اشتباه است
    </h2>
    
    
    </html>
    """

    else:
        return"""
           <html>
    <head>
    <style>
    @font-face {
  font-family: myFont;
  src: url(fonts/font.woff) format('woff');
}
@font-face {
font-family: "CustomFont";
src: url("fonts/CustomFont.eot");
src: url("fonts/CustomFont.woff") format("woff"),
url("fonts/CustomFont.otf") format("opentype"),
url("fonts/CustomFont.svg") format("svg");
}
    body{
        justify-content: center;
        place-items: center;
        
        
        display: flex;
       
    
        
    }
    h2 {
        color:#ffffffe8;
        border:0.0001px solid brown;
        background-color:brown;
        font-family: 'CustomFont';
        padding:30px 30px;
        border-radius:10px;
        
        
        
     }

    </style>
    </head>
    <title>Error</title>
    <h2 class="404">نام یا شماره موبایل تکراری است
    </h2>
    
    
    </html>
    """






"""chek_phone_number=User.query.filter(User.phone==number).scalar()"""
    
# error page (404)
@app.errorhandler(404)
def showerror(error):
    return """
    <html>
    <head>
    <style>
    @font-face {
  font-family: myFont;
  src: url(fonts/font.woff) format('woff');
}
@font-face {
font-family: "CustomFont";
src: url("fonts/CustomFont.eot");
src: url("fonts/CustomFont.woff") format("woff"),
url("fonts/CustomFont.otf") format("opentype"),
url("fonts/CustomFont.svg") format("svg");
}
    body{
        justify-content: center;
        place-items: center;
        
        
        display: flex;
       
    
        
    }
    h2 {
        color:#ffffffe8;
        border:0.0001px solid brown;
        background-color:brown;
        font-family: 'CustomFont';
        padding:30px 30px;
        border-radius:10px;
        
        
        
     }

    </style>
    </head>
    <title>Not Found</title>
    <h2 class="404">Sorry , Page Not Found 404
    </h2>
    
    
    </html>
    """
app.secret_key="qejijdixjadalkwakwlswx"
# ***************************
# run the program
PORT = os.getenv("PORT",5000)
app.run("192.168.1.105")