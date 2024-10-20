from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app) 

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  
    email = db.Column(db.String(100), nullable=False) 


with app.app_context():
    db.create_all()  

@app.route('/', methods=['GET', 'POST'])  
def index():
    if request.method == 'POST':  
        name = request.form['name'] 
        email = request.form['email'] 
        new_contact = Contact(name=name, email=email)  
        db.session.add(new_contact) 
        db.session.commit()  
        return redirect('/') 
    
    contacts = Contact.query.all() 
    return render_template('sql.html', contacts=contacts)  

@app.route('/edit/<int:id>', methods=['GET', 'POST'])  # Edit contact route
def edit_contact(id):
    contact = Contact.query.get_or_404(id) 
    if request.method == 'POST': 
        contact.name = request.form['name']  
        contact.email = request.form['email']  
        db.session.commit()  
        return redirect('/') 
    return render_template('edit_sql.html', contact=contact)  

@app.route('/delete/<int:id>')  
def delete_contact(id):
    contact = Contact.query.get_or_404(id)  
    db.session.delete(contact)  
    db.session.commit() 
    return redirect('/')

if __name__ == '__main__':  
    app.run(debug=True)  
