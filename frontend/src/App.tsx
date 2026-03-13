import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Recover from "./pages/Recover";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import Users from "./pages/Users";
import UserProfile from "./pages/UserProfile";
import Community from "./pages/Community";
import CommunityWrite from "./pages/CommunityWrite";
import ProblemDetail from "./pages/ProblemDetail";
import ProblemCreate from "./pages/ProblemCreate";
import ProblemResolutions from "./pages/ProblemResolutions";
import Solve from "./pages/Solve";
import Rooms from "./pages/Rooms";
import RoomCreate from "./pages/RoomCreate";
import RoomLobby from "./pages/room/RoomLobby";
import RoomProblems from "./pages/room/RoomProblems";
import RoomSolve from "./pages/room/RoomSolve";
import RoomConfig from "./pages/room/RoomConfig";
import RoomMe from "./pages/room/RoomMe";
import RoomSubmissions from "./pages/room/RoomSubmissions";
import RoomChat from "./pages/room/RoomChat";
import NotFound from "./pages/NotFound";
import ProblemSolve from "./pages/ProblemSolve";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/recover" element={<Recover />} />
          <Route path="/home" element={<Home />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/users" element={<Users />} />
          <Route path="/user/:id" element={<UserProfile />} />
          <Route path="/community" element={<Community />} />
          <Route path="/community/write" element={<CommunityWrite />} />
          <Route path="/problem/:id" element={<ProblemDetail />} />
          <Route path="/problem/create" element={<ProblemCreate />} />
          <Route path="/problem/:id/solves" element={<ProblemResolutions />} />
          <Route path="/problem/:problemId/solve/:solveId" element={<ProblemSolve />}/>
          <Route path="/solve/:id" element={<Solve />} />
          <Route path="/rooms" element={<Rooms />} />
          <Route path="/room/create" element={<RoomCreate />} />
          <Route path="/room/lobby" element={<RoomLobby />} />
          <Route path="/room/problems" element={<RoomProblems />} />
          <Route path="/room/solve/:id" element={<RoomSolve />} />
          <Route path="/room/config" element={<RoomConfig />} />
          <Route path="/room/me" element={<RoomMe />} />
          <Route path="/room/submissions" element={<RoomSubmissions />} />
          <Route path="/room/chat" element={<RoomChat />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
