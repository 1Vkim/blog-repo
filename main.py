from flask import Flask, redirect,session,request,url_for
from replit import db
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ['sessionKey']
password=os.environ['me']

def readblog():
  entry=''
  content=''
  f=open("template/display.html","r")
  entry=f.read()
  f.close()
  keys=db.keys()
  keys=list(keys)
  for key in reversed(keys):
    thisentry=entry
    if key !='user':
      thisentry=thisentry.replace("{title}",db[key]["title"])
      thisentry=thisentry.replace("{date}",db[key]["date"])
      thisentry=thisentry.replace("{text}",db[key]["remarks"])
      content+=thisentry
  return content

@app.route('/')
def index():
  
  page = ""
  with open("template/blog.html","r") as f:
    page = f.read()
    f.close()
    page=page.replace("{content}",readblog())
  return page

@app.route("/login",methods=["POST"])
def login():
  
  session["myName"]={"username":"Vinkim","password":password}
  page=""
  with open( "template/login.html","r") as f:
    page=f.read()
    f.close()

  return page

@app.route("/verify",methods=["POST"])
def do_verify():
  form=request.form
  if "myName" in session and "password" in session["myName"]:
    if form["username"]==session["myName"]["username"] and form["password"]==session["myName"]["password"]:
      return redirect("/view")

    else:
      return "Invaild username or password:Try again!"

  else:
    return redirect("/login")


@app.route('/view')
def view():

  page = ""
  with open("template/write.html","r") as f:
    page = f.read()
    f.close()
  return page

@app.route('/store_details',methods=["POST"])
def store_detail():
 
  form=request.form
  if "title" in form and "date" in form and "body" in form:
    entry={"title":form["title"],"date":form["date"],"body":form["body"]}
    db[form['date']] = entry
    content=""
    page=""
    with open("template/write.html","r") as f:
       page = f.read()
       f.close()
    page=page.replace("{content}",readblog())
    return redirect("/view")

  else:
    return "Error:Form data is missng required keys.Try again!"



@app.route("/logout")
def logout():
  session.clear()
  return redirect("/")


app.run(host='0.0.0.0', port=81,debug=True)
