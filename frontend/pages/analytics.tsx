import { useEffect, useState } from 'react';
import { Layout } from '../components/Layout';

type TopicStats = Record<string, { attempts: number; correct: number; accuracy: number; avg_time: number }>;

type Dashboard = {
  topics: TopicStats;
  volatility: Record<string, number>;
  recency: Record<string, number>;
};

export default function Analytics() {
  const [token, setToken] = useState('');
  const [data, setData] = useState<Dashboard | null>(null);

  useEffect(() => {
    const cached = localStorage.getItem('token');
    if (cached) setToken(cached);
  }, []);

  const load = async () => {
    const res = await fetch('http://localhost:8000/analytics', {
      headers: { Authorization: token },
    });
    const json = await res.json();
    setData(json);
  };

  return (
    <Layout>
      <h2>Analytics Dashboard</h2>
      <div className="controls">
        <label>
          Session Token
          <input value={token} onChange={(e) => { setToken(e.target.value); localStorage.setItem('token', e.target.value); }} />
        </label>
        <button onClick={load}>Refresh</button>
      </div>
      {data && (
        <div className="grid">
          {Object.entries(data.topics).map(([topic, stats]) => (
            <div key={topic} className="card">
              <h3>{topic}</h3>
              <p>Attempts: {stats.attempts}</p>
              <p>Accuracy: {(stats.accuracy * 100).toFixed(1)}%</p>
              <p>Avg Time: {stats.avg_time.toFixed(1)}s</p>
              <p>Volatility: {(data.volatility[topic] || 0).toFixed(2)}</p>
              <p>Recency: {(data.recency[topic] || 0).toFixed(2)}</p>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}
