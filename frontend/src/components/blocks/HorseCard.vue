<template>
  <q-card class="horse-card app-card app-clickable">
    <div class="horse-card__image-wrap">
      <img :src="imageSrc" :alt="horse.name" class="horse-card__image" />

      <AppStatusBadge
        class="horse-card__status"
        :label="statusLabel"
        :tone="statusTone"
      />
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
</template>

<script setup>
import { computed } from 'vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge.vue'
import {
  formatHorseAge,
  formatHorseArrivalDate,
  getHorseImageSrc,
  getHorseStatusLabel,
  getHorseStatusTone,
} from 'src/utils/horsePresentation'

const props = defineProps({
  horse: {
    type: Object,
    required: true,
  },
})

const imageSrc = computed(() => getHorseImageSrc(props.horse.photo_url))
const statusLabel = computed(() => getHorseStatusLabel(props.horse.status))
const statusTone = computed(() => getHorseStatusTone(props.horse.status))
const ageLabel = computed(() => formatHorseAge(props.horse.age))
const arrivalDateLabel = computed(() => formatHorseArrivalDate(props.horse.arrival_date))
</script>
