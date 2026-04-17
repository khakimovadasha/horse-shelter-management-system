<template>
  <q-card :class="[$style.root, 'app-card', 'app-clickable']">
    <div :class="$style.imageWrap">
      <img :src="imageSrc" :alt="horse.name" :class="$style.image" />

      <AppStatusBadge
        :class="$style.status"
        :label="statusLabel"
        :tone="statusTone"
      />
    </div>

    <div :class="$style.body">
      <h3 :class="$style.name">{{ horse.name }}</h3>

      <p :class="$style.breed">
        {{ horse.breed || 'Порода не указана' }}
      </p>

      <div :class="$style.meta">
        <div><strong>Возраст:</strong> {{ ageLabel }}</div>
        <div><strong>Дата поступления:</strong> {{ arrivalDateLabel }}</div>
      </div>
    </div>
  </q-card>
</template>

<script setup>
import { computed } from 'vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'
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

<style module lang="scss" src="./HorseCard.module.scss"></style>
