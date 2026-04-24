import { api, API_BASE_URL } from 'src/boot/axios'
import { getAccessToken } from 'src/api/auth'

export { API_BASE_URL }

export const getHorses = async () => {
  const response = await api.get('/horses/')
  return response.data
}

export const getHorseById = async (horseId) => {
  const response = await api.get(`/horses/${horseId}`)
  return response.data
}

export const getHorseMedicalRecords = async (horseId) => {
  const token = getAccessToken()

  const response = await api.get(`/horses/${horseId}/medical-records`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  return response.data
}
