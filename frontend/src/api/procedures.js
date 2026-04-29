import { api } from 'src/boot/axios'
import { getAccessToken } from 'src/api/auth'

export const getProcedures = async () => {
  const token = getAccessToken()

  const response = await api.get('/procedures', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  return response.data
}
