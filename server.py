import os
import web
import pymongo#note: you must first run this terminal command: sudo python -m pip install pymongo to use this package.
#Database setup: Create a database named messageboard. Add a collection called posts.
from pymongo import MongoClient
import unirest
client = MongoClient('mongodb://localhost:27017')
db = client['Messageboard']
key = 'f0de28e094c09589a1db004b314ed357'
oauth_nonce = []
client_id = 2260
client_secret = 'c306f7d154a86ddb0f1a'
token = 'not the token'

from web.wsgiserver import CherryPyWSGIServer

CherryPyWSGIServer.ssl_certificate = '/etc/letsencrypt/live/kdsmessageboard.com/fullchain.pem'
CherryPyWSGIServer.ssl_private_key = '/etc/letsencrypt/live/kdsmessageboard.com/privkey.pem'

render = web.template.render('website/')

urls = (
    '/' , 'index',
    '/launch', 'launch',
    '/reload' , 'reload'
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

#maybe this will help?
class reload:
    def GET(self):
        for post in postsdb:
            commentsdb = db.comments.find()
            carr = []
            for comment in commentsdb:
                if int(comment.get('referenceid')) == int(post.get('myid')):
                    c = Comment(comment.get('name') , comment.get('text') , comment.get('referenceid'))
                    carr.append(c)
            p = Post(post.get('name') , post.get('text') , post.get('pic') , carr , post.get('myid'))
            posts.append(p)
        web.header('X-Frame-Options' , 'ALLOW-FROM *')
        return render.index(posts)

#the main website homepage
class index:
    #returns the website
    def GET(self):
        try:
            error = web.input().error
            print error
            raise web.seeother('http://www.beesbeesbees.com')
        except AttributeError:
            print web.input()
            code = web.input().code
            print code
            url = 'https://learn-lti.herokuapp.com/login/oauth2/token?client_id=' + str(client_id) + '&redirect_uri=https://kdsmessageboard.com:8080/&client_secret=' + str(client_secret) + '&code=' + str(code)
            print url
            response = unirest.post(url)
            token = response.body.get('access_token')
            print 'token:' + str(token)


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
        web.header('X-Frame-Options' , 'ALLOW-FROM *')
        return render.index(posts)
    #sees if a comment or post was submitted and handles it
    def POST(self):
        form = web.input()
        print('hi')
        try:
            post = form.writepost
            posts = db.posts.find().sort('myid' , pymongo.DESCENDING)
            try:
                myid = posts[0].get('myid') + 1
            except IndexError:
                myid = 1

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

        raise web.seeother('/reload')

class launch:
    def POST(self):
        form = web.input()
        roles = form.roles
        oauth_nonce.append(form.oauth_nonce)
        if form.lti_message_type == 'basic-lti-launch-request' and form.oauth_consumer_key == key:
            print 'new user!'
            print 'lti_message_type: ' + form.lti_message_type
            print 'lti_version: ' + form.lti_version
            print 'resource_link_id: ' + form.resource_link_id
            print 'context_id: ' + form.context_id
            print 'user_id: ' + form.user_id
            print 'roles: ' + form.roles
            print 'key: ' + form.oauth_consumer_key
            print 'oauth_nonce: ' + form.oauth_nonce
            print 'oauth_timestamp: ' + form.oauth_timestamp
            print 'oauth_signature: ' + form.oauth_signature
            print 'name: ' + form.lis_person_name_full
            print 'email: ' + form.lis_person_contact_email_primary
            print 'image src: ' + form.user_image
            print 'service url: ' + form.lis_outcome_service_url

            return render.index()
        else:
            raise web.seeother('http://www.beesbeesbees.com')
    def GET(self):
        url = 'https://learn-lti.herokuapp.com/login/oauth2/auth?client_id=' + str(client_id) + '&response_type=code&redirect_uri=https://kdsmessageboard.com:8080/'
        return web.redirect(url)
#main method
if __name__ == '__main__':
    app.run()
