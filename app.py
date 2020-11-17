from flask import Flask,render_template, request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app = Flask(__name__)
app.secret_key = 'aydan_240'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

class person(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    email = db.Column(db.String(128))

    def __init__(self,name,surname,email):
        self.name = name
        self.surname = surname
        self.email = email
    
    def __repr__(self):
        return f"User('{self.name}' ,{self.surname}' ,'{self.email}' )"


@app.route('/')
def index():
    allpersons = person.query.all()
    return render_template('index.html', persons = allpersons)



@app.route('/insert', methods=['POST'])
def insert():
    # if request.method == 'POST': get ve post olanda sert qoy
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        newperson = person(name,surname,email)
        db.session.add(newperson)
        db.session.commit()

        flash('Melumat elave olundu ')

        return redirect(url_for('index'))




@app.route('/delete/<id>/', methods=['GET'])
def delete(id):
    delete_person = person.query.get(id)
    db.session.delete(delete_person)
    db.session.commit()
    flash('Melumat silindi')

    return redirect(url_for('index'))

@app.route('/edit/<id>/', methods=['GET', 'POST'])
def edit(id):
    edit_person = person.query.get(id)
    edit_person.name = request.form['name']
    edit_person.surname = request.form['surname']
    edit_person.email = request.form['email']

    db.session.commit()
    flash('Melumat yenilendi')
    return redirect(url_for('index'))






















if __name__ == '__main__':
    app.run(debug = True)
      