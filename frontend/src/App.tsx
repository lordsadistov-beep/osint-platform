import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Layout, PublicLayout } from './components/Layout'
import { useAuthStore } from './stores/authStore'
import { Landing } from './pages/Landing'
import { Login } from './pages/Login'
import { Register } from './pages/Register'
import { Learn } from './pages/Learn'
import { LessonDetail } from './pages/LessonDetail'
import { Challenges } from './pages/Challenges'
import { ChallengeDetail } from './pages/ChallengeDetail'
import { ToolUsername } from './pages/ToolUsername'
import { ToolEmail } from './pages/ToolEmail'
import { ToolPhone } from './pages/ToolPhone'
import { ToolDomain } from './pages/ToolDomain'
import { ToolLeaks } from './pages/ToolLeaks'
import { ToolMetadata } from './pages/ToolMetadata'
import { Dashboard } from './pages/Dashboard'
import { GraphView } from './pages/GraphView'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => !!s.user)
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return <>{children}</>
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PublicLayout />}>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Route>
        <Route element={<Layout />}>
          <Route path="/learn" element={<Learn />} />
          <Route path="/learn/:slug" element={<LessonDetail />} />
          <Route path="/challenges" element={<Challenges />} />
          <Route path="/challenges/:id" element={<ChallengeDetail />} />
          <Route path="/tools/username" element={<ToolUsername />} />
          <Route path="/tools/email" element={<ToolEmail />} />
          <Route path="/tools/phone" element={<ToolPhone />} />
          <Route path="/tools/domain" element={<ToolDomain />} />
          <Route path="/tools/leaks" element={<ToolLeaks />} />
          <Route path="/tools/metadata" element={<ToolMetadata />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard/graph" element={<GraphView />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
