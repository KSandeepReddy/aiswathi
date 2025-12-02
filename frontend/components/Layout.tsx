import Link from 'next/link';
import { ReactNode } from 'react';

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="container">
      <header>
        <h1>Adaptive Prep</h1>
        <nav>
          <Link href="/">Home</Link>
          <Link href="/practice">Practice</Link>
          <Link href="/analytics">Analytics</Link>
          <Link href="/plan">Study Plan</Link>
        </nav>
      </header>
      <main>{children}</main>
    </div>
  );
}
