import os
import web
import pymongo#note: you must first run this terminal command: sudo python -m pip install pymongo to use this package.
#Database setup: Create a database named messageboard. Add a collection called posts.
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['Messageboard']


render = web.template.render('website/')

urls = (
    '/' , 'index'
)

app = web.application(urls, globals(), True)

#a class for organizing posts
class Post:
    def __init__(self , n , t , p , c , m):
        self.name = n
        self.text = t
        self.pic = p
        self.comments = c
        self.myid = m

#a class for organizing comments
class Comment:
    def __init__(self , n , t , r):
        self.name = n
        self.text = t
        self.referenceid = r

#the main website homepage
class index:
    #returns the website
    def GET(self):
        c = Comment('Bob' , 'This should be a comment.' , 1)
        comments = [c]
        p = Post('Russell' , 'Is this working?' , 'https://kentdenver.instructure.com/images/thumbnails/15304/ckhEcjfPPMuJeUIXGPMdg7QoyNC0c6Ptd5vdGKfe' , comments , 1)
        posts = [p]
        return render.index(posts)
    #sees if a comment or post was submitted and handles it
    def POST(self):
        form = web.input()
        print('hi')
        try:
            post = form.writepost
            posts = db.posts.find().sort('myid' , pymongo.DESCENDING)
            myid = posts[0].get('myid') + 1

            db.posts.insert_one({
                 'name' : 'should go here',
                 'text' : post,
                 'pic' : 'should go here',
                 'myid' : myid})
            print(post)
        except AttributeError:
            myid = form.myid
            comment = form.comment
            print(comment)
            print(myid)

        raise web.seeother('/')

#main method
if __name__ == '__main__':
    c = Comment('Bob' , 'This should be a comment.' , 1)
    comments = [c]
    # p = Post('Russell' , 'Is this working?' , 'https://kentdenver.instructure.com/images/thumbnails/15304/ckhEcjfPPMuJeUIXGPMdg7QoyNC0c6Ptd5vdGKfe' , comments , 1)
    # db.posts.insert_one({
    #     'name' : p.name,
    #     'text' : p.text,
    #     'pic' : p.pic,
    #     'myid' : p.myid})
    # db.comments.insert_one({
    #     'name' : c.name,
    #     'text' : c.text,
    #     'referenceid' : c.referenceid})
    app.run()
