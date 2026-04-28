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

export const createHorse = async (payload) => {
  const token = getAccessToken()

  const response = await api.post('/horses/', payload, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

export const updateHorse = async (horseId, payload) => {
  const token = getAccessToken()

  const response = await api.patch(`/horses/${horseId}`, payload, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data',
    },
  })

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

export const createHorseMedicalRecord = async (horseId, payload) => {
  const token = getAccessToken()

  const response = await api.post(`/horses/${horseId}/medical-records`, payload, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  return response.data
}
