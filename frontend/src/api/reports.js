import { api, getAccessToken } from 'src/api/auth'

const PREVIEW_ENDPOINTS = {
  all_horses: '/reports/all-horses',
  horse_detail: '/reports/horse-detail',
  medical_procedures: '/reports/medical-procedures',
  all_tasks: '/reports/all-tasks',
  user_tasks: '/reports/user-tasks',
  finance: '/reports/finance',
  shelter_summary: '/reports/shelter-summary',
}

const EXPORT_ENDPOINTS = {
  all_horses: '/reports/all-horses/export',
  horse_detail: '/reports/horse-detail/export',
  medical_procedures: '/reports/medical-procedures/export',
  all_tasks: '/reports/all-tasks/export',
  user_tasks: '/reports/user-tasks/export',
  finance: '/reports/finance/export',
  shelter_summary: '/reports/shelter-summary/export',
}

const buildAuthHeaders = () => {
  const token = getAccessToken()

  return {
    Authorization: `Bearer ${token}`,
  }
}

const normalizeParams = (params) => {
  return Object.fromEntries(
    Object.entries(params).filter(([, value]) => value !== '' && value !== undefined),
  )
}

export const getReportFilterOptions = async () => {
  const response = await api.get('/reports/options', {
    headers: buildAuthHeaders(),
  })

  return response.data
}

export const getReportPreview = async (reportType, params) => {
  const response = await api.get(PREVIEW_ENDPOINTS[reportType], {
    headers: buildAuthHeaders(),
    params: normalizeParams(params),
  })

  return response.data
}

export const exportReport = async (reportType, params, format) => {
  const response = await api.get(EXPORT_ENDPOINTS[reportType], {
    headers: buildAuthHeaders(),
    params: normalizeParams({ ...params, format }),
    responseType: 'blob',
  })

  return {
    blob: response.data,
    contentDisposition: response.headers['content-disposition'] || '',
  }
}

