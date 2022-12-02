from flask import Flask ,request, render_template
from main import *
app = Flask(__name__)

@app.route('/',methods = ["GET","POST"])
def home():
    if request.method =="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        profileURL = request.form.get("profileURL")
        result = openLinkedinAndLogin(email,password,profileURL)
        if result:
            return render_template('result.html',res=result)
        else:
            return render_template('error.html')

    return render_template('home.html');

if __name__ == '__main__':
    app.run(debug= True)