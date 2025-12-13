import { ReactNode } from 'react';
import { Navbar } from './Navbar';

interface PageContainerProps {
  children: ReactNode;
  showNavbar?: boolean;
  className?: string;
}

export function PageContainer({ children, showNavbar = true, className = '' }: PageContainerProps) {
  return (
    <div className="min-h-screen bg-background">
      {showNavbar && <Navbar />}
      <main className={`container py-6 ${className}`}>
        {children}
      </main>
    </div>
  );
}
