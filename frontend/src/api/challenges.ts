import api from './client'

export const challengesApi = {
  list: () => api.get('/challenges'),
  get: (id: string) => api.get(`/challenges/${id}`),
  hint: (id: string) => api.post(`/challenges/${id}/hint`),
  submit: (id: string, flag: string) => api.post(`/challenges/${id}/submit`, { flag }),
  leaderboard: () => api.get('/challenges/leaderboard'),
}
