import { API_BASE_URL } from 'src/api/horses'

const HORSE_STATUS_LABELS = {
  healthy: 'Здоров',
  sick: 'Болен',
  rehabilitation: 'Реабилитация',
  deceased: 'Выбыл',
}

export const getHorseImageSrc = (photoUrl) => {
  if (!photoUrl) {
    return 'https://placehold.co/600x400?text=Horse'
  }

  return `${API_BASE_URL}${photoUrl}`
}

export const getHorseStatusLabel = (status) => HORSE_STATUS_LABELS[status] || status

export const getHorseStatusTone = (status) => {
  const tones = {
    healthy: 'healthy',
    sick: 'sick',
    rehabilitation: 'rehabilitation',
    deceased: 'deceased',
  }

  return tones[status] || 'default'
}

export const formatHorseAge = (age) => {
  if (!age) return 'Не указан'
  return `${age} лет`
}

export const formatHorseArrivalDate = (arrivalDate) => {
  if (!arrivalDate) return 'Не указана'

  return new Date(arrivalDate).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}
