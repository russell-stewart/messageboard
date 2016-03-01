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
        postsdb = db.posts.find().sort('myid' , pymongo.DESCENDING)
        posts = []
        for post in postsdb:
            commentsdb = db.comments.find()
            carr = []
            for comment in commentsdb:
                if int(comment.get('referenceid')) == int(post.get('myid')):
                    c = Comment(comment.get('name') , comment.get('text') , comment.get('referenceid'))
                    carr.append(c)
            p = Post(post.get('name') , post.get('text') , post.get('pic') , carr , post.get('myid'))
            posts.append(p)
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
                 #PLACEHOLDER FIX WHEN CANVAS WORKS
                 'name' : 'should go here',
                 'text' : post,
                 #PLACEHOLDER FIX WHEN CANVAS WORKS
                 'pic' : 'https://i1.wp.com/canvas.instructure.com/images/messages/avatar-50.png?ssl=1',
                 'myid' : myid})
            print(post)
        except AttributeError:
            myid = form.id
            comment = form.comment
            db.comments.insert_one({
                'text' : comment,
                'referenceid' : myid,
                #PLACEHOLDER FIX WHEN CANVAS WORKS
                'name' : 'should go here'
            })
            print(comment)
            print(myid)

        raise web.seeother('/')

#main method
if __name__ == '__main__':
    app.run()
