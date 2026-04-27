import { api, getAccessToken } from 'src/api/auth'

export const getUsers = async () => {
  const token = getAccessToken()

  const response = await api.get('/users/', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  return response.data
}
