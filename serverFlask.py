from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask import  request
import sqlite3
import html
from limiter import limit_requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Définition du formulaire de contact
class ContactForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Envoyer')

# Route pour afficher le formulaire
@app.route('/contact', methods=['GET', 'POST'])
@limit_requests(window_size=60, max_requests=2) 
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Récupérer les données validées du formulaire
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # Connexion à la base de données SQLite
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()

        # Insérer les données dans la table contacts sans requête préparée pour faire passer l'attaque injection sql
        '''query_np = 'INSERT INTO contacts(name, email, message) VALUES ("%s", "%s", "%s")' %(name, email, message);
        print('requête générée après injection SQL', query_np)
        cursor.execute(query_np) '''


        # filtrer le name et le message recupérer les caracteres alpha b

        #Utiliser les procédures pour minimiser les requetes preparées


        # Insérer les données dans la table contacts avec requête préparée
        query_p = 'INSERT INTO contacts(name, email, message) VALUES (?,?,?)'
        print('requête générée après injection SQL', query_p)
        cursor.execute(query_p,(html.escape(name), html.escape(email), html.escape(message)))
    
        conn.commit()
        conn.close()

        return 'Formulaire soumis avec succès !'

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
