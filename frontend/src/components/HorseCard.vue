<template>
  <router-link :to="`/horses/${horse.id}`" class="horse-card-link">
    <q-card class="horse-card app-card app-clickable">
      <div class="horse-card__image-wrap">
        <img :src="imageSrc" :alt="horse.name" class="horse-card__image" />

        <div class="horse-card__status" :class="statusClass">
          {{ statusLabel }}
        </div>
      </div>

      <div class="horse-card__body">
        <h3 class="horse-card__name">{{ horse.name }}</h3>

        <p class="horse-card__breed">
          {{ horse.breed || 'Порода не указана' }}
        </p>

        <div class="horse-card__meta">
          <div><strong>Возраст:</strong> {{ ageLabel }}</div>
          <div><strong>Дата поступления:</strong> {{ arrivalDateLabel }}</div>
        </div>
      </div>
    </q-card>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { API_BASE_URL } from 'src/api/horses'

const props = defineProps({
  horse: {
    type: Object,
    required: true,
  },
})

const imageSrc = computed(() => {
  if (!props.horse.photo_url) {
    return 'https://placehold.co/600x400?text=Horse'
  }

  return `${API_BASE_URL}${props.horse.photo_url}`
})

const statusLabel = computed(() => {
  const map = {
    healthy: 'Здоров',
    sick: 'Болен',
    rehabilitation: 'Реабилитация',
    deceased: 'Выбыл',
  }

  return map[props.horse.status] || props.horse.status
})

const statusClass = computed(() => {
  const map = {
    healthy: 'horse-card__status--healthy',
    sick: 'horse-card__status--sick',
    rehabilitation: 'horse-card__status--rehab',
    deceased: 'horse-card__status--deceased',
  }

  return map[props.horse.status] || ''
})

const ageLabel = computed(() => {
  if (!props.horse.age) return 'Не указан'
  return `${props.horse.age} лет`
})

const arrivalDateLabel = computed(() => {
  if (!props.horse.arrival_date) return 'Не указана'

  return new Date(props.horse.arrival_date).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
})
</script>