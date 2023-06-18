from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from flask_session import Session
import pymongo
import json
from flask import render_template,redirect,url_for
from flask import Flask, request, render_template,redirect,url_for,flash,session
app=Flask(__name__)
app.secret_key = 'random string'

myclient            =  pymongo.MongoClient("mongodb://localhost:27017/")
mydb                =  myclient['Jobdb']
UserSkill           =  mydb['UserSkill']
UserDetails         =  mydb['UserDetails']
JobRequirement      =  mydb['JobRequirement']
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

@app.route("/")
def homepage():
    if "user_id" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

@app.route("/dashboard",methods=['GET'])
def dashboard():
    loggedin_userid=session['user_id']
    loggedin_user=list(UserDetails.find({'Email':loggedin_userid}))[0]
    print(list(UserDetails.find({'Email':loggedin_userid})))
    return render_template("dashboard.html",email=loggedin_user["Email"],firstname=loggedin_user['FirstName'],lastname=loggedin_user['LastName'],phone=loggedin_user['Phone'],password=loggedin_user['Password'],confirmpassword=loggedin_user['ConfirmPassword'])

@app.route("/Applicants",methods=['GET'])
def Applicants():
    return render_template("Applicants.html")

@app.route("/OnSiteFull",methods=['GET'])
def OnSiteFull():
    return render_template("OnSiteFull.html")

@app.route("/OnSitePart",methods=['GET'])
def OnSitePart():
    return render_template("OnSitePart.html")

@app.route("/RemoteFull",methods=['GET'])
def RemoteFull():
    return render_template("RemoteFull.html")

@app.route("/RemotePart",methods=['GET'])
def RemotePart():
    return render_template("RemotePart.html")

@app.route("/aboutus",methods=['GET'])
def aboutus():
    return render_template("about_us.html")

@app.route("/add_user",methods=['GET','POST'])
def add_user():
    
    if request.method=='POST':
        _json             =request.form
        _id               =_json['email']
        FirstName         =_json['fname']
        LastName          =_json['lname']
        Email             =_json['email']
        Phone             =_json['phone']
        Password          =_json['password']
        ConfirmPassword   =_json['confirmpassword']
        Type              =_json['combobox']
        if Email:
            records          =UserDetails.find({'_id':{'$eq':_id}})
            records_cnt      =len(list(records))
            #length_check    =len(validation)
            if records_cnt>0:
                #return json.dumps({'Answer':'user already exists'})
                message="user already exists"
                flash(message)
                return redirect(url_for('add_user'))
            else:
                if FirstName and LastName and Email and Phone and Password and ConfirmPassword and Type and request.method=='POST':
                    UserDetails.insert_one({'_id':_id,'FirstName':FirstName,'LastName':LastName,'Email':Email,'Phone':Phone,'Password':Password,'ConfirmPassword':ConfirmPassword,'Type':Type})
                    #session["_id"]=_id
                    return redirect(url_for('login'))
                else:
                    return redirect(url_for('add_user'))
    return render_template("signup.html")
   
       
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        _json     =request.form
        _id       =_json['email']
        loginpassword  =_json['password']
        print(_id,loginpassword,request.method,"abcedrf")
        if _id and loginpassword:
            records=UserDetails.find({'_id':{'$eq':_id},'Password':{'$eq':loginpassword}})
            record_check=list(records)
            print(record_check)
            length_check=len(record_check)
            if length_check>0:
                session["user_id"]=_id
                return redirect(url_for('dashboard'))
            
            recordcheck=UserDetails.find()
            check_list=list(recordcheck)
            print("check_list=",check_list)
            print(len(check_list))
            email_found=False
            pasword_match=False
            for d in check_list:
                print(d)
                if  d['_id']==_id:
                        email_found=True
                        break
            if  email_found:
                message="Password Not Matched"
            else:
                message="Email Not Found"
            flash(message)
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/user_profile_update',methods=['GET'])
def user_profile_update():
    print("***************")
    _json            =request.args
    Email            =_json['email']
    FirstName        =_json['fname']
    LastName         =_json['lname']
    Phone            =_json['phone']
    Password         =_json['password']
    ConfirmPassword  =_json['confirmpassword']

    print(Email,FirstName,LastName,Phone,Password,ConfirmPassword)

    if Email and FirstName and LastName and Phone and Password and ConfirmPassword and request.method=='GET':
        UserDetails.update_one({'Email':Email},{'$set':{'FirstName':FirstName,'LastName':LastName,'Phone':Phone,'Password':Password,'ConfirmPassword':ConfirmPassword}})
        return json.dumps({'Answer':'Update Sucessfull'})
    else:
        return json.dumps({'Answer':'Update Failed'})

@app.route('/user_skill_update',methods=['POST','GET'])
def user_skill_update():

    if request.method=='GET':
        return render_template("Userskill.html")
    else:
            #print("******")
            _json   =request.form
            Email   =_json['Email']
            print("Email=",Email)
            if Email:
                validate=UserSkill.find({'Email':{'$eq':Email}})
                print(validate)
                validation=list(validate)
                print(validation)
                len_check=len(validation)
                print(len_check)
                if len_check>0:
                    _json       =request.form
                    _id         =_json['Email']
                    Skillset    =_json['Skillset']
                    Skills      =Skillset.split(',')

                    filter      ={"_id":_id}
                    updation    ={"$addToSet":{"Skillset":{"$each":Skills}}}
                    UserSkill.update_one(filter,updation)
                    return json.dumps({'Answer':"Updation Successful"})
                else:
                    _json       =request.form
                    Email       =_json['Email']
                    Skillset    =_json['Skillset']
                    Skills      =Skillset.split(',')
                    if Email and Skillset:
                        obj={
                            'Email':Email,
                            "_id":Email,
                            "Skillset":Skills
                        }
                        UserSkill.insert_one(obj)
                        return json.dumps({'Answer':'Insertion Sucessful'})

@app.route("/add_job_requirement",methods=['POST','GET'])
def add_job_requirement():
    
    if request.method=='GET':
        return render_template("Job_requirement.html")
    else:
        _json                   =   request.form
        Email                   =   _json['Email']
        Job_requirement_id      =   _json['Job_requirement_id']
        Date                    =   _json['Date']
        Location                =   _json['Location']
        Type                    =   _json['Type']
        Job_description         =   _json['Job_description']
        Required_skills         =   _json['Required_skills']
        Skills                  =   Required_skills.split(',')
        Status                  =   _json['Status']

        if Email and Job_requirement_id and Date and Location and Type  and Job_description and Required_skills and Status and request.method=='POST':
                obj={'_id':Job_requirement_id,
                    'Email':Email,
                    'Job Requirement Id':Job_requirement_id,
                    'Date':Date,
                    'Location':Location,
                    'Type':Type,
                    'Job Description':Job_description,
                    'Required Skills':Skills,
                    'Status':Status}
                
                JobRequirement.insert_one(obj)
                return json.dumps({'Answer':'Insertion Sucessful'})

@app.route("/update_job_requirement_status",methods=['POST'])
def update_job_requirement_status():
    _json              =  request.form
    Job_requirement_id = _json['Job_requirement_id'] 
    Status             = _json['Status']

    if  Job_requirement_id and Status and request.method=='POST':
        JobRequirement.update_one({'Job Requirement Id':Job_requirement_id},{'$set':{'Status':Status}})
        return json.dumps({'Answer':'Updation Sucessfull'})
    
@app.route("/get_job_requirement_details",methods=['POST','GET'])
def get_job_requirement_details():

    if request.method=='GET':
        validate=JobRequirement.find()
        print(validate)
        validation=list(validate)
        #print(validation)
        response=dumps(validation)
        print("response=",{'Answer':response})
        return json.dumps({'Answer':response})
    
@app.route("/OnSiteFullTimeJob",methods=['GET'])
def OnSiteFullJob():
    #Type=request.args.get("Type")
    if request.method=="GET":
        condition={"Type":{"$regex":"Full Time-OnSite","$options":"$i"}}
        users=JobRequirement.find(condition,{"_id":1,"Email":1,"Job Requirement Id":1,"Date":1,"Location":1,"Type":1,"Title":1,"Job Description":1,"Required Skills":1,"Status":1})
        response=dumps(users)
        return json.dumps({"Answer":response})
    
@app.route("/OnSitePartTimeJob",methods=['GET'])
def OnSitePartJob():
    if  request.method=="GET":
        condition={"Type":{"$regex":"Part Time-OnSite","$options":"$i"}}
        users=JobRequirement.find(condition,{"_id":1,"Email":1,"Job Requirement Id":1,"Date":1,"Location":1,"Type":1,"Title":1,"Job Description":1,"Required Skills":1,"Status":1})
        response=dumps(users)
        return json.dumps({"Answer":response})
    
@app.route("/RemoteFulltimeJob",methods=['GET'])
def RemoteFulltimeJob():
    #Type=request.args.get("Type")   
    if  request.method=="GET":
        condition={"Type":{"$regex":"Full-Time Remote","$options":"$i"}}
        users=JobRequirement.find(condition,{"_id":1,"Email":1,"Job Requirement Id":1,"Date":1,"Location":1,"Type":1,"Title":1,"Job Description":1,"Required Skills":1,"Status":1})
        response=dumps(users)
        return json.dumps({"Answer":response})
    
@app.route("/RemoteParttimeJob",methods=['GET'])
def RemoteParttimeJob():
    #Type=request.args.get("Type")  
    if request.method=="GET":
        condition={"Type":{"$regex":"Part Time-Remote","$options":"$i"}}
        users=JobRequirement.find(condition,{"_id":1,"Email":1,"Job Requirement Id":1,"Date":1,"Location":1,"Type":1,"Title":1,"Job Description":1,"Required Skills":1,"Status":1})
        response=dumps(users)
        return json.dumps({"Answer":response})
    

@app.route("/Skilljoin",methods=['GET'])
def Skilljoin():
    if request.method=='GET':
        condition={"Type":{"$regex":"Job Seeker","$options":"$i"}}
        pipeline=[
            {
                "$lookup":{
                    "from":"UserDetails",
                    "localField":"_id",
                    "foreignField":"_id",
                    "as":"Details"
                }
            }
        ]
        result=mydb.UserSkill.aggregate(pipeline)
        rows=[]
        #print("Result=",list(result))
        for item in result:
            print(item)
            userDetails=item['Details']
            firstname   =False
            lastName    =False
            email       =False
            phone       =False
            Skillset    =False
            print("userDetails=",userDetails)
            if len(userDetails)>0:
                print("-----",userDetails)
                userDetails_=userDetails[0]
                print("userDetails_",userDetails_)
                firstname   =userDetails_['FirstName']
                lastName    =userDetails_['LastName']
                phone       =userDetails_['Phone']
            #print(item['Skillset'])
            email       =item['Email']
            Skillset=",".join(item['Skillset'])
            #print(Skillset)
            print("****",firstname,lastName,email,phone,Skillset)
            if firstname and lastName and email and phone and Skillset:
                rows.append([firstname,lastName,email,phone,Skillset])
        print("rows=",rows)
        return json.dumps({"Answer":rows})

@app.route('/logout',)
def logout():
    if "user_id" in session :
       session.pop("user_id",None)
    return redirect(url_for("homepage"))


    
app.run(debug=True)


