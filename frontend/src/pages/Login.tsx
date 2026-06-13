import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import { Button } from '../components/common/Button'
import { Input } from '../components/common/Input'
import { Card } from '../components/common/Card'

export function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuthStore()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      await login(username, password)
      navigate('/learn')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="flex min-h-[80vh] items-center justify-center px-4">
      <Card className="w-full max-w-sm">
        <h1 className="mb-6 text-xl font-bold text-gray-100">Вход</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Username или Email" value={username} onChange={(e) => setUsername(e.target.value)} />
          <Input label="Пароль" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          {error && <p className="text-sm text-red-400">{error}</p>}
          <Button type="submit" className="w-full">Войти</Button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-500">
          Нет аккаунта? <Link to="/register" className="text-primary-400 hover:underline">Регистрация</Link>
        </p>
      </Card>
    </div>
  )
}
