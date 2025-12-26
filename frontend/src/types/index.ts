export interface User {
  id: string;
  name: string;
  email: string;
  login: string;
  avatar?: string;
  description?: string;
  country: string;
  problemsSolved: number;
  problemsAttempted: number;
  followers: number;
  createdAt: string;
}

export interface Problem {
  id: string;
  title: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
  creatorId: string;
  creatorName: string;
  timeLimit: number;
  memoryLimit: number;
  attempts: number;
  solved: number;
  likes: number;
  dislikes: number;
  tags: string[];
  createdAt: string;
}

export interface Comment {
  id: string;
  problemId: string;
  userId: string;
  userName: string;
  userAvatar?: string;
  content: string;
  createdAt: string;
  replies?: Comment[];
}

export interface Post {
  id: string;
  userId: string;
  userName: string;
  userAvatar?: string;
  content: string;
  tags: string[];
  createdAt: string;
  replies: Post[];
}

export interface Room {
  id: string;
  name: string;
  description: string;
  creatorId: string;
  creatorName: string;
  isPrivate: boolean;
  capacity: number;
  currentPlayers: number;
  status: 'waiting' | 'in_progress' | 'finished';
  endTime?: string;
  duration?: number;
  acceptingSubmissions?: boolean;
  problems: RoomProblem[];
}

export interface RoomProblem {
  problemId: string;
  title: string;
  points: number;
  balloonColor: string;
  submissions: number;
  correct: number;
}

export interface Submission {
  id: string;
  odId: string;
  odName: string;
  odAvatar?: string;
  problemId: string;
  problemTitle: string;
  language: 'java' | 'python' | 'c' | 'cpp';
  status: 'accepted' | 'wrong_answer' | 'time_limit' | 'runtime_error' | 'compile_error';
  points: number;
  time: number;
  memory: number;
  createdAt: string;
  code?: string;
  balloonColor?: string;
}

export interface ChatMessage {
  id: string;
  odId: string;
  odName: string;
  odAvatar?: string;
  content: string;
  createdAt: string;
}

export interface ReportCategory {
  id: string;
  name: string;
}

export interface Tag {
  id: string;
  name: string;
  color?: string;
}
