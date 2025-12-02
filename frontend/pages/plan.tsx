import { useEffect, useState } from 'react';
import { Layout } from '../components/Layout';

type WeeklyTask = { week: number; topic_slug: string; target_questions: number; focus: string };
type Plan = { goals: string[]; weeks: number; weekly_tasks: WeeklyTask[]; adherence?: any[] };

export default function Plan() {
  const [token, setToken] = useState('');
  const [plan, setPlan] = useState<Plan | null>(null);
  const [goalInput, setGoalInput] = useState('Master kinematics');

  useEffect(() => {
    const cached = localStorage.getItem('token');
    if (cached) setToken(cached);
  }, []);

  const create = async () => {
    const res = await fetch('http://localhost:8000/study-plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: token },
      body: JSON.stringify({ goals: [goalInput], weeks: 4 }),
    });
    const json = await res.json();
    setPlan(json);
  };

  const logWeek = async () => {
    await fetch('http://localhost:8000/study-plan/adherence', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: token },
      body: JSON.stringify({ week: 1, completed_tasks: 3, reflections: 'Need to review graphs of motion' }),
    });
  };

  return (
    <Layout>
      <h2>Study Plan</h2>
      <div className="controls">
        <label>
          Session Token
          <input value={token} onChange={(e) => { setToken(e.target.value); localStorage.setItem('token', e.target.value); }} />
        </label>
        <input value={goalInput} onChange={(e) => setGoalInput(e.target.value)} />
        <button onClick={create}>Generate Plan</button>
        <button onClick={logWeek}>Log Week</button>
      </div>
      {plan && (
        <div className="grid">
          {plan.weekly_tasks.map((task) => (
            <div key={task.week} className="card">
              <h3>Week {task.week}</h3>
              <p>Topic: {task.topic_slug}</p>
              <p>Focus: {task.focus}</p>
              <p>Target questions: {task.target_questions}</p>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}
