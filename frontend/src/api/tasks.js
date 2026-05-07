import { api } from 'src/boot/axios'
import { getAccessToken } from 'src/api/auth'

const withAuth = () => ({
  headers: {
    Authorization: `Bearer ${getAccessToken()}`,
  },
})

export const getTasks = async () => {
  const response = await api.get('/tasks', withAuth())
  return response.data
}

export const createTask = async (payload) => {
  const response = await api.post('/tasks', payload, withAuth())
  return response.data
}

export const startTask = async (taskId) => {
  const response = await api.post(`/tasks/${taskId}/start`, {}, withAuth())
  return response.data
}

export const completeTask = async (taskId) => {
  const response = await api.post(`/tasks/${taskId}/complete`, {}, withAuth())
  return response.data
}
