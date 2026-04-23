import { api } from 'src/boot/axios'

export const TOKEN_KEY = 'access_token'

export const getAccessToken = () => {
  return localStorage.getItem(TOKEN_KEY)
}

export const setAccessToken = (token) => {
  localStorage.setItem(TOKEN_KEY, token)
}

export const removeAccessToken = () => {
  localStorage.removeItem(TOKEN_KEY)
}

export const loginUser = async (payload) => {
  const response = await api.post('/auth/login', payload)
  return response.data
}

export const registerUser = async (payload) => {
  const response = await api.post('/auth/register', payload)
  return response.data
}

export const getMe = async () => {
  const token = getAccessToken()

  const response = await api.get('/auth/me', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  return response.data
}

export { api }
