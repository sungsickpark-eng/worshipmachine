import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [songs, setSongs] = useState([]);
  const [conti, setConti] = useState([]);
  
  // 입력 폼 상태
  const [title, setTitle] = useState('');
  const [key, setKey] = useState('G');
  const [tempo, setTempo] = useState('Fast');

  // 데이터 불러오기 함수
  const fetchSongs = () => {
    axios.get('http://127.0.0.1:5000/api/songs')
      .then(res => setSongs(res.data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchSongs();
  }, []);

  // 노래 추가 핸들러
  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://127.0.0.1:5000/api/songs', { title, key, tempo })
      .then(() => {
        alert("노래가 추가되었습니다!");
        setTitle('');
        fetchSongs();
      });
  };

  // 콘티에 추가
  const addToConti = (song) => {
    if (!conti.find(item => item.id === song.id)) {
      setConti([...conti, song]);
    } else {
      alert("이미 추가된 곡입니다.");
    }
  };

  // 콘티에서 제거
  const removeFromConti = (id) => {
    setConti(conti.filter(item => item.id !== id));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎸 예배 찬양 콘티 빌더</h1>
      </header>

      <section className="add-song-form">
        <h2>새 노래 등록</h2>
        <form onSubmit={handleSubmit}>
          <input 
            type="text" placeholder="노래 제목" value={title}
            onChange={(e) => setTitle(e.target.value)} required 
          />
          <select value={key} onChange={(e) => setKey(e.target.value)}>
            {['C','D','E','F','G','A','B'].map(k => <option key={k} value={k}>{k}</option>)}
          </select>
          <select value={tempo} onChange={(e) => setTempo(e.target.value)}>
            <option value="Fast">Fast</option>
            <option value="Slow">Slow</option>
          </select>
          <button type="submit">추가하기</button>
        </form>
      </section>

      <div className="container">
        <section className="library">
          <h2>노래 라이브러리 (클릭해서 추가)</h2>
          <div className="card-container">
            {songs.map(song => (
              <div key={song.id} className="song-card" onClick={() => addToConti(song)}>
                <div className="song-info">
                  <span className="song-key">{song.key}</span>
                  <span className="song-title">{song.title}</span>
                </div>
                <span className={`tempo-badge ${song.tempo.toLowerCase()}`}>{song.tempo}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="conti-basket">
          <h2>오늘의 예배 콘티</h2>
          <div className="conti-list">
            {conti.length === 0 && <p>곡을 선택해 주세요.</p>}
            {conti.map((song, index) => (
              <div key={song.id} className="conti-item">
                <span className="order">{index + 1}</span>
                <span className="title">{song.title} ({song.key})</span>
                <button className="del-btn" onClick={() => removeFromConti(song.id)}>❌</button>
              </div>
            ))}
          </div>
          {conti.length > 0 && <button className="save-btn" onClick={() => window.print()}>프린트 / PDF 저장</button>}
        </section>
      </div>
    </div>
  );
}

export default App;