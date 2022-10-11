from flask import Flask, render_template, request, redirect, session
import mariadb
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)


conn = mariadb.connect(host="localhost",username="root",password="",database="login_page")
cursor=conn.cursor()


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login')
def home1():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/home')
def home2():
    if 'id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """
                   .format(email, password))
    users=cursor.fetchall()
    print(users)
    if len(users)>0:
        session['id']=users[0][0]
        return redirect('home')
    else:
        return redirect('login')


@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')
    cursor.execute("""INSERT INTO `users` (`id`, `name`, `email`,`password`) VALUES (NULL,'{}','{}','{}')""".format(name,email,password))
    conn.commit()

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['id']=myuser[0][0]
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('login')

if __name__ == "__main__":
    app.run(debug=True)