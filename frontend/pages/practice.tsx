import { useEffect, useState } from 'react';
import { Layout } from '../components/Layout';

type Question = {
  id: number;
  text: string;
  options: string[];
  topic_slug: string;
};

export default function Practice() {
  const [token, setToken] = useState('');
  const [question, setQuestion] = useState<Question | null>(null);
  const [mode, setMode] = useState<'practice' | 'adaptive' | 'review'>('adaptive');
  const [feedback, setFeedback] = useState('');

  useEffect(() => {
    const cached = localStorage.getItem('token');
    if (cached) setToken(cached);
  }, []);

  const fetchQuestion = async () => {
    const res = await fetch('http://localhost:8000/next-question', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: token,
      },
      body: JSON.stringify({ mode }),
    });
    const data = await res.json();
    setQuestion(data);
  };

  const submitAttempt = async (answerIndex: number) => {
    if (!question) return;
    const res = await fetch('http://localhost:8000/attempts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: token,
      },
      body: JSON.stringify({ question_id: question.id, selected_index: answerIndex, time_spent_seconds: 20 }),
    });
    const data = await res.json();
    setFeedback(data.correct ? 'Correct!' : 'Keep trying');
    fetchQuestion();
  };

  return (
    <Layout>
      <h2>Practice Mode</h2>
      <div className="controls">
        <label>
          Session Token
          <input value={token} onChange={(e) => { setToken(e.target.value); localStorage.setItem('token', e.target.value); }} />
        </label>
        <select value={mode} onChange={(e) => setMode(e.target.value as any)}>
          <option value="practice">Practice</option>
          <option value="adaptive">Adaptive</option>
          <option value="review">Review</option>
        </select>
        <button onClick={fetchQuestion}>Get Question</button>
      </div>
      {question && (
        <div className="card">
          <p><strong>{question.topic_slug}</strong></p>
          <p>{question.text}</p>
          {question.options.map((opt, idx) => (
            <button key={idx} onClick={() => submitAttempt(idx)}>{opt}</button>
          ))}
        </div>
      )}
      {feedback && <p>{feedback}</p>}
    </Layout>
  );
}
