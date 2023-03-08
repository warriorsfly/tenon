from flask_httpauth import HTTPBasicAuth

basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(email:str,password:str):
    if email == '':
        return False
    
    