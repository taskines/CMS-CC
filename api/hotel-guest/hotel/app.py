import os, psycopg
from psycopg.rows import dict_row
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv 

# pip install psycopg_binary python-dotenv

load_dotenv()

PORT=8812 # Freddes port ANVÄND DIN EGEN!

db_url = os.environ.get("DB_URL")
print(os.environ.get("FOO"))

conn = psycopg.connect(db_url, autocommit=True, row_factory=dict_row)

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

roomsTEMP = [
    { 'number': 101, 'type': "single" },
    { 'number': 202, 'type': "double" },
    { 'number': 303, 'type': "suite" }
]

@app.route("/", )
def info():
    #return "<h1>Hello, Flask!</h1>"
    return "Välkommen till hotellet kära gäst!"



@app.route("/guests", methods=['GET'])
def guests_endoint():
    with conn.cursor() as cur:
            cur.execute("""SELECT * 
                        FROM hotel_guest 
                        ORDER BY firstname""")
            return cur.fetchall()


@app.route("/rooms", methods=['GET', 'POST'])
def rooms_endoint():
    if request.method == 'POST':
        request_body = request.get_json()
        print(request_body)
        roomsTEMP.append(request_body)
        return { 
            'msg': f"Du har skapat ett nytt rum, id: {len(roomsTEMP)-1}!"
        }
    else:
        with conn.cursor() as cur:
            cur.execute("""SELECT * 
                        FROM hotel_room 
                        ORDER BY room_number""")
            return cur.fetchall()

@app.route("/rooms/<int:id>", methods=['GET', 'PUT', 'PATCH', 'DELETE'] )
def one_room_endpoint(id):
        if request.method == 'GET':
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * 
                    FROM hotel_room 
                    WHERE id = %s""", [id])

                return cur.fetchone()
        
@app.route("/bookings", methods=['GET', 'POST'])
def bookings():
    if not request.args.get('api_key'):
         return {"msg":"Error: api_key missing!"}, 401
    
    if request.method == 'GET':
        with conn.cursor() as cur:
            cur.execute("""SELECT  
    b.id,
    b.datefrom,
    r.room_number,
    r.type,
    g.firstname,
    g.address
    
FROM hotel_booking AS b 


INNER JOIN hotel_room AS r
   ON r.id =b.room_id
   

INNER JOIN hotel_guest AS g
  ON g.id =b.guest_id

WHERE g.api_key=%s                        
                        
ORDER by b.datefrom""", ['api_key'])
            return cur.fetchall()
        
    if request.method == 'POST':
        body = request.get_json()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO hotel_booking (
                    room_id, 
                    guest_id,
                    datefrom
                ) VALUES (
                    %s, 
                    %s, 
                    %s
                ) RETURNING id""", [ 
                body['room'], 
                body['guest'], 
                body['datefrom'] 
            ])
            result = cur.fetchone()
    
        return { "msg": "Du har bokat ett rum!", "result": result }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))
