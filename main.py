from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import datetime
import json


app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db=SQLAlchemy()
db.init_app(app)


class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    auther = db.Column(db.String(20))
    title = db.Column(db.String(20))
    discription = db.Column(db.String(100))
    posted = db.Column(db.String(10))


    def to_blog(self):
        return {
            "id":self.id,
            "auther":self.auther,
            "title":self.title,
            "discription":self.discription,
            "posted":self.posted
        }



with app.app_context():
    db.create_all()



@app.route("/blog",methods=["Post"])
def create_blog():

    current_date=str(datetime.datetime.now())
    a= json.loads(request.data)
    id=a.get("id")
    auther=a.get("auther")
    title=a.get("title")
    discription=a.get("discription")
    posted=current_date

    entry = Blog(id=id,auther=auther,title=title,discription=discription,posted=posted)

    db.session.add(entry)
    db.session.commit()

    return jsonify(entry.to_blog())


@app.route("/blog",methods=["Get"])
def get_blog():

    blog= Blog.query.all()
    # print(blog)
    blog_list =[]
    for blogs in blog:
        blog_list.append({"id":blogs.id,"auther":blogs.auther,"title":blogs.title,"discription":blogs.discription,"posted":blogs.posted})




    return jsonify(blog_list)


@app.route("/blog/<int:blog_id>",methods=["Get"])
def find_blog(blog_id):
    blog = Blog.query.get(blog_id)

    return jsonify(blog.to_blog())

@app.route("/blog/<int:blog_id>",methods=["Put"])
def update_blog(blog_id):
    blog=Blog.query.get(blog_id)
    current_date=str(datetime.datetime.now())
    a= json.loads(request.data)

    discription=a.get("discription")
    auther=a.get("auther")
    posted =current_date

    blog.discription=discription
    blog.auther=auther
    blog.posted = posted

    db.session.commit()

    return jsonify(blog.to_blog())


@app.route("/blog/<int:blog_id>",methods=["Delete"])
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()

    return jsonify(blog.to_blog())




















if __name__=="__main__":
    app.run(debug=True)

