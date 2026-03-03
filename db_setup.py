from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- 본인의 정보로 수정하세요 ---
DB_USER = "admin"
DB_PASSWORD = "20100220Pss!"
DB_HOST = "worshipmachine.clqcieo6g714.ap-northeast-2.rds.amazonaws.com"
DB_NAME = "worshipmachine" 
# ---------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 노래 테이블 구조 정의
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # 제목
    song_key = db.Column(db.String(10))               # 코드(G, A 등)
    tempo = db.Column(db.String(20))                 # 빠르기(Fast, Slow)

if __name__ == '__main__':
    with app.app_context():
        # 1. 기존 테이블이 없다면 생성
        db.create_all()
        print("✅ 테이블 생성 완료!")

        # 2. 샘플 데이터 하나 넣어보기
        sample_song = Song(title="주 이름 찬양", song_key="G", tempo="Fast")
        db.session.add(sample_song)
        db.session.commit()
        print("✅ 샘플 데이터(주 이름 찬양) 입력 성공!")