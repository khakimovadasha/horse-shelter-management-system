import { api } from 'src/boot/axios'
import { getAccessToken } from 'src/api/auth'

const withAuth = () => ({
  headers: {
    Authorization: `Bearer ${getAccessToken()}`,
  },
})

export const getFinanceOperations = async () => {
  const response = await api.get('/finance-operations', withAuth())
  return response.data
}

export const getFinanceSummary = async () => {
  const response = await api.get('/finance-operations/summary', withAuth())
  return response.data
}

export const createFinanceOperation = async (payload) => {
  const response = await api.post('/finance-operations', payload, withAuth())
  return response.data
}
