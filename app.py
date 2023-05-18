from flask import Flask, render_template, request, session, redirect, url_for
import stripe
import json

app = Flask(__name__, template_folder="templates", static_url_path='/static')
app.secret_key = 'Ranit001'

stripe.api_key = "sk_test_51N7Db3SJ5z0OEl6IMYrsVdCs5y7Am3OdFsc3YgWam8QI5FdtCcmkmpLbglXP4De0TzhW8AusSpNhGN2cvd6JHYaj00aY1kiNBP"
final_username=""
user_id=''
email_form=''

@app.route('/')
def hello_world():
    global user_id, final_username
    if user_id=='':
        pass
    else:
        user_data=stripe.Customer.retrieve(user_id)
        final_username=user_data["name"]
    return render_template('index.html', username=final_username)

@app.route('/templates/Sign_up.html')
def Sign_up():
    return render_template('Sign_up.html',usern="type your a suitable username here")

@app.route('/template/Sign_in.html')
def Sign_in():
    return render_template('Sign_in.html')

@app.route('/username_avilability', methods=['POST','GET'])
def checkusername():
    global final_username
    if request.method == 'POST':
        user = str(request.form['username'])
        customers = stripe.Customer.list()
        customer_names = [customer.name for customer in customers.auto_paging_iter()]
        if user in customer_names:
            return render_template('Sign_up.html', usern="")
        else:
            final_username=user
            return render_template('Sign_up.html', usern=user)
        

@app.route('/submit-form',methods=['POST','GET'])
def submit_form():
    global final_username
    if request.method=='POST':
        phonenumber=int(request.form['phonenumber'])
        emailid=str(request.form['InputEmail1'])
        customers = stripe.Customer.list()
        saved_emailid = [customer.email for customer in customers.auto_paging_iter()]
        password=str(request.form['Password'])
        if emailid in saved_emailid:
            return render_template('Sign_up.html')
        else:
            customer=stripe.Customer.create(
                name=final_username,
                phone=phonenumber,
                email=emailid
                )
            session['signed_up'] = True
            return redirect(url_for('hello_world'))

@app.route('/signin_form', methods=['GET','POST'])
def signinform():
    global user_id
    if request.method == 'POST':
        signin_email = str(request.form['signin_email'])
        customer_list = stripe.Customer.list(email=signin_email)
        if customer_list.data:
            user_id = customer_list.data[0].id
            session['signed_up'] = True
            return redirect(url_for('hello_world'))
        else:
            return redirect(url_for('submit_form'))

@app.route('/paymentpage', methods=['GET','POST'])
def paymentform():
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True)
