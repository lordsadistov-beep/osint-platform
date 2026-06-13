import { create } from 'zustand'
import { authApi } from '../api/auth'

interface User {
  id: string
  username: string
  email?: string
  avatar_url?: string
  role: string
  experience: number
  level: number
}

interface AuthState {
  user: User | null
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  register: (username: string, email: string, password: string) => Promise<void>
  logout: () => void
  fetchMe: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: true,
  login: async (username, password) => {
    const { data } = await authApi.login({ username, password })
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    const me = await authApi.me()
    set({ user: me.data })
  },
  register: async (username, email, password) => {
    const { data } = await authApi.register({ username, email, password })
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    const me = await authApi.me()
    set({ user: me.data })
  },
  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    set({ user: null })
  },
  fetchMe: async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        set({ isLoading: false })
        return
      }
      const { data } = await authApi.me()
      set({ user: data, isLoading: false })
    } catch {
      set({ isLoading: false })
    }
  },
}))
