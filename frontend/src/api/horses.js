import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
})

export const API_BASE_URL = 'http://127.0.0.1:8000'

export const getHorses = async () => {
  const response = await api.get('/horses/')
  return response.data
}

export const getHorseById = async (horseId) => {
  const response = await api.get(`/horses/${horseId}`)
  return response.data
}