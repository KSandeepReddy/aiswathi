import Link from 'next/link';
import { Layout } from '../components/Layout';

export default function Home() {
  return (
    <Layout>
      <p>Welcome to the adaptive IIT JEE practice companion. Use the navigation to log in, practice questions, and review analytics.</p>
      <div className="grid">
        <Link className="card" href="/login">Login</Link>
        <Link className="card" href="/practice">Start Practice</Link>
        <Link className="card" href="/analytics">Analytics Dashboard</Link>
        <Link className="card" href="/plan">Study Plan</Link>
      </div>
    </Layout>
  );
}
