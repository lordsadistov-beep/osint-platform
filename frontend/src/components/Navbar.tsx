import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import { Button } from './common/Button'
import { UserAvatar } from './UserAvatar'

export function Navbar() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  return (
    <nav className="fixed top-0 z-50 flex h-14 w-full items-center border-b border-gray-800 bg-gray-950/80 px-4 backdrop-blur">
      <Link to="/" className="text-lg font-bold text-primary-400">
        OSINT Platform
      </Link>
      <div className="ml-auto flex items-center gap-3">
        {user ? (
          <>
            <Link to="/learn" className="text-sm text-gray-400 hover:text-gray-200">
              Уроки
            </Link>
            <Link to="/challenges" className="text-sm text-gray-400 hover:text-gray-200">
              Челленджи
            </Link>
            <Link to="/tools/username" className="text-sm text-gray-400 hover:text-gray-200">
              Инструменты
            </Link>
            <Link to="/dashboard" className="text-sm text-gray-400 hover:text-gray-200">
              <UserAvatar user={user} />
            </Link>
          </>
        ) : (
          <>
            <Button variant="ghost" size="sm" onClick={() => navigate('/login')}>
              Войти
            </Button>
            <Button size="sm" onClick={() => navigate('/register')}>
              Регистрация
            </Button>
          </>
        )}
      </div>
    </nav>
  )
}
