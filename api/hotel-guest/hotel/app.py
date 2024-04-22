import os, psycopg
from psycopg.rows import dict_row
from flask import Flask, request
from flask_cors import CORS
from markupsafe import escape
from dotenv import load_dotenv 


# pip install psycopg_binary python-dotenv

load_dotenv()

PORT=8811 # Freddes port ANVÄND DIN EGEN!

db_url = os.environ.get("DB_URL")
print(os.environ.get("FOO"))

conn = psycopg.connect(db_url, autocommit=True, row_factory=dict_row)

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests


@app.route("/", )
def info():
    #return "<h1>Hello, Flask!</h1>"
    return "Välkommen till hotellet kära gäst!"


@app.route("/rooms", methods=['GET'])
def rooms_endoint():
    with conn.cursor() as cur:
        cur.execute("""SELECT * 
                    FROM hotel_room 
                    ORDER BY room_number""")
        return cur.fetchall()

@app.route("/rooms/<int:id>", methods=['GET'] )
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
    api_key = request.args.get('api_key')
    guest_id = None

    if not api_key:
        return { "msg": "ERROR: api_key missing!" }, 401

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id 
            FROM hotel_guest
            WHERE api_key = %s""", [ api_key])
        guest = cur.fetchone()
        if not guest:
            return { "msg": "ERROR: bad api_key!" }, 403
    
        guest_id = guest['id']

    if request.method == 'GET':
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT 
                        b.*,
                        r.room_number,
                        r.type,
                        g.firstname,
                        g.address
                    FROM hotel_booking b

                    INNER JOIN hotel_room r
                        ON r.id = b.room_id

                    INNER JOIN hotel_guest g
                        ON g.id = b.guest_id

                    WHERE g.id = %s

                    ORDER by b.datefrom""", [ guest_id ])
            return cur.fetchall()
        
    if request.method == 'POST':
        body = request.get_json()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO hotel_booking (
                    room_id, 
                    guest_id,
                    datefrom,
                    addinfo
                ) VALUES (
                    %s, 
                    %s, 
                    %s,
                    %s
                ) RETURNING id""", [ 
                body['room'], 
                guest_id, 
                body['datefrom'],
                escape(body['addinfo'])
            ])
            result = cur.fetchone()
    
        return { "msg": "Du har bokat ett rum!", "result": result }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))