import api from './client'

export const lessonsApi = {
  list: (params?: any) => api.get('/lessons', { params }),
  categories: () => api.get('/lessons/categories'),
  get: (slug: string) => api.get(`/lessons/${slug}`),
  practice: (slug: string) => api.get(`/lessons/${slug}/practice`),
  complete: (slug: string) => api.post(`/lessons/${slug}/complete`),
  related: (id: string) => api.get(`/lessons/${id}/related`),
}
