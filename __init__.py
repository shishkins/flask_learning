from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intro = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create-article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        intro = request.form['intro']
        article = Article(title=title, text=text, intro=intro)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Something went wrong!'
    else:
        return render_template('create-article.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get_or_404(id)
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/del', methods=['GET', 'POST'])
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        db.session.rollback()
        return 'Something went wrong!'


@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.text = request.form['text']
        article.intro = request.form['intro']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            db.session.rollback()
            return 'Something went wrong!'
    else:
        return render_template('post_update.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)
