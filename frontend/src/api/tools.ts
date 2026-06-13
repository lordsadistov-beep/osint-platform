import api from './client'

export const toolsApi = {
  username: (username: string) => api.post(`/tools/username/${username}`),
  email: (email: string) => api.post(`/tools/email/${email}`),
  phone: (phone: string) => api.post(`/tools/phone/${phone}`),
  domain: (domain: string) => api.post(`/tools/domain/${domain}`),
  metadata: (file: File) => {
    const form = new FormData()
    form.append('file', file)
    return api.post('/tools/metadata', form, { headers: { 'Content-Type': 'multipart/form-data' } })
  },
  leaks: (query: string, type: string) => api.post('/tools/leaks/search', { query, type }),
  graph: (type: string, value: string) => api.post(`/tools/graph/${type}/${value}`),
}
