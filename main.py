from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

class AddProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    in_charge = StringField('In Charge', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Add Project')

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM projects")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', projects=data)

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    form = AddProjectForm()
    if form.validate_on_submit():
        project_name = form.project_name.data
        in_charge = form.in_charge.data
        status = form.status.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO projects (project_name, in_charge, status) VALUES (%s, %s, %s)", (project_name, in_charge, status))
        mysql.connection.commit()
        cur.close()
        flash('Project added successfully!')
        return redirect(url_for('index'))
    return render_template('addproject.html', form=form)

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM projects WHERE id=%s", (id_data,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/update/<string:id_data>', methods=['GET', 'POST'])
def update(id_data):
    if request.method == 'POST':
        project_name = request.form['project_name']
        in_charge = request.form['in_charge']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE projects SET project_name=%s, in_charge=%s, status=%s
        WHERE id=%s
        """, (project_name, in_charge, status, id_data))
        mysql.connection.commit()
        cur.close()
        flash("Data Updated Successfully")
        return redirect(url_for('index'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM projects WHERE id=%s", (id_data,))
        data = cur.fetchone()
        cur.close()
        return render_template('update_project.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
