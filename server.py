import os
import web

render = web.template.render('website/')

urls = (
    '/' , 'index'
)

app = web.application(urls, globals(), True)

class Post:
    name = ""
    text = ""
    comments = []
    myid = -1

class Comment:
    name = ""
    text = ""
    referenceid = -1

class index:
    def GET(self):
        p = Post()
        p.name = 'Russell'
        p.text = 'Is this working?'
        p.id = 1
        c = Comment()
        c.name = 'Bob'
        c.text = 'This should be a comment'
        c.referenceid = -1
        comments = [c]
        p.comments = comments
        posts = [p]
        return render.index(posts)
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
