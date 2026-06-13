import api from './client'

export const dashboardApi = {
  stats: () => api.get('/dashboard/stats'),
  history: (params?: any) => api.get('/dashboard/history', { params }),
  deleteHistory: (id: string) => api.delete(`/dashboard/history/${id}`),
  graph: () => api.get('/dashboard/graph'),
  saveConnection: (data: any) => api.post('/dashboard/graph/save', data),
  deleteConnection: (id: string) => api.delete(`/dashboard/graph/${id}`),
  export: (format: string) => api.post('/dashboard/export', { format }),
}
