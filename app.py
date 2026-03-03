from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # React와의 통신 허용

# --- AWS RDS 연결 설정 (본인의 정보로 꼭 수정하세요) ---
DB_USER = "admin"
DB_PASSWORD = "20100220Pss!"
DB_HOST = "worshipmachine.clqcieo6g714.ap-northeast-2.rds.amazonaws.com"
DB_NAME = "worshipmachine" 

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    song_key = db.Column(db.String(10))
    tempo = db.Column(db.String(20))

# 1. 모든 노래 가져오기 (GET)
@app.route('/api/songs', methods=['GET'])
def get_songs():
    songs = Song.query.all()
    return jsonify([
        {"id": s.id, "title": s.title, "key": s.song_key, "tempo": s.tempo} 
        for s in songs
    ])

# 2. 새 노래 추가하기 (POST)
@app.route('/api/songs', methods=['POST'])
def add_song():
    data = request.json
    new_song = Song(
        title=data['title'],
        song_key=data['key'],
        tempo=data['tempo']
    )
    db.session.add(new_song)
    db.session.commit()
    return jsonify({"message": "노래 추가 성공!"}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 테이블이 없으면 자동 생성
    app.run(debug=True, port=5000)