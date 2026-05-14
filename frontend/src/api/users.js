import { api, getAccessToken } from 'src/api/auth'

const withAuth = () => {
  const token = getAccessToken()

  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }
}

export const getUsers = async () => {
  const response = await api.get('/users/', withAuth())
  return response.data
}

export const updateUserRole = async (userId, role) => {
  const response = await api.patch(`/users/${userId}/role`, { role }, withAuth())
  return response.data
}

export const updateUserActive = async (userId, isActive) => {
  const response = await api.patch(`/users/${userId}/active`, { is_active: isActive }, withAuth())
  return response.data
}
