from flask import Flask, request
from flask_cors import CORS 

PORT=8801 #freddes port

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

@app.route("/", methods=['GET', 'POST'])
def hello():
    #return "<h1>Hello, Flask!</h1>"
    return { 
        'greeting': "Hello, Flask-JSON!",
        'method': request.method 
    }

@app.route("/test", methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # skapa rad i databasen, returnera ny id..
        new_id = 555
        return { 
            'msg': f"Du har skapat en ny rad i databasen, id är {new_id}!",
            'method': request.method 
        }
    else:
         
        return { 
            'msg': "TESTING!",
            'method': request.method 
        }

@app.route("/test/<int:id>", methods=['GET', 'PUT', 'PATCH', 'DELETE'] )
def testId(id):
        if request.method == 'GET':
            return { 
                'msg': f"här får du id: {id}",
                'method': request.method 
            }
        if request.method == 'PUT' or request.method == 'PATCH':
            return { 
                'msg': f"Du uppdaterar id: {id}",
                'method': request.method 
            }
        if request.method == 'DELETE':
            return { 
                'msg': f"Du har raderat {id}",
                'method': request.method 
            }



@app.route("/ip")
def ip():
    return { 'ip': request.remote_addr }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))
