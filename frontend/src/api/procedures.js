import { api } from 'src/boot/axios'
import { getAccessToken } from 'src/api/auth'

const withAuth = () => ({
  headers: {
    Authorization: `Bearer ${getAccessToken()}`,
  },
})

export const getProcedures = async () => {
  const response = await api.get('/procedures', withAuth())
  return response.data
}

export const createProcedure = async (horseId, payload) => {
  const response = await api.post(`/horses/${horseId}/procedures`, payload, withAuth())
  return response.data
}

export const completeProcedure = async (horseId, procedureId, payload = {}) => {
  const response = await api.post(
    `/horses/${horseId}/procedures/${procedureId}/complete`,
    payload,
    withAuth()
  )

  return response.data
}
