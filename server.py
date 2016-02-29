import os
import web
import pymongo#note: you must first run this terminal command: sudo python -m pip install pymongo to use this package.
#Database setup: Create a database named messageboard. Add a collection called posts.
from pymongo import MongoClient
client = MongoClient('localhost' , 27017)
db = client.messageboard
collection = db.posts


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
        print(comments[0].name)
        return render.index(posts)
    #sees if a comment or post was submitted and handles it
    def POST(self):
        form = web.input()
        try:
            post = form.writepost
            print(post)
        except AttributeError:
            myid = form.id
            comment = form.comment
            print(comment)
            print(myid)

        raise web.seeother('/')

#main method
if __name__ == '__main__':

    app.run()
