from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash
)


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = []
users.append(User(id=1, username='Bruno', password='1234'))
users.append(User(id=2, username='Rubens', password='1234'))
users.append(User(id=3, username='Anna', password='1234'))
users.append(User(id=4, username='Wesley', password='1234'))
users.append(User(id=5, username='Rolf', password='1234'))

app = Flask(__name__)
app.secret_key = 'teta'


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template('login.html')
    session.pop('user_id', None)

    username = request.form['username']
    password = request.form['password']

    user = [x for x in users if x.username == username][0]
    if user and user.password == password:
        session['user_id'] = user.id
        return redirect(url_for('index'))

    return redirect(url_for('/'))


@app.route('/index')
def index():
    if not g.user:
        return redirect(url_for('/'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
