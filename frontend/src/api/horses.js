import { api, API_BASE_URL } from 'src/boot/axios'

export { API_BASE_URL }

export const getHorses = async () => {
  const response = await api.get('/horses/')
  return response.data
}

export const getHorseById = async (horseId) => {
  const response = await api.get(`/horses/${horseId}`)
  return response.data
}
