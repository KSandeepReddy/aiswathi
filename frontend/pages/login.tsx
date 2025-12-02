import { useState } from 'react';
import { Layout } from '../components/Layout';

export default function Login() {
  const [email, setEmail] = useState('student@example.com');
  const [password, setPassword] = useState('secret');
  const [token, setToken] = useState('');

  const submit = async () => {
    const res = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (data.token) setToken(data.token);
  };

  return (
    <Layout>
      <h2>Login</h2>
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <input value={password} type="password" onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
      <button onClick={submit}>Log in</button>
      {token && <p>Session token: {token}</p>}
    </Layout>
  );
}
