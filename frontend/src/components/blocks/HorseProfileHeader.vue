<template>
  <q-card class="app-card horse-profile-card">
    <div class="horse-profile-card__top">
      <div class="horse-profile-card__main">
        <div class="horse-profile-card__image-wrap">
          <img :src="imageSrc" :alt="horse.name" class="horse-profile-card__image" />
        </div>

        <div class="horse-profile-card__content">
          <div class="horse-profile-card__title-row">
            <div>
              <h1 class="horse-profile-card__name">{{ horse.name }}</h1>

              <AppStatusBadge
                class="horse-profile-card__status"
                :label="statusLabel"
                :tone="statusTone"
              />
            </div>
          </div>

          <div class="horse-profile-card__info-grid">
            <AppInfoItem
              class="horse-profile-card__info-block"
              label="Порода:"
              :value="horse.breed || 'Не указана'"
            />
            <AppInfoItem
              class="horse-profile-card__info-block"
              label="Возраст:"
              :value="ageLabel"
            />
            <AppInfoItem
              class="horse-profile-card__info-block"
              label="Куратор:"
              value="Не назначен"
            />
            <AppInfoItem
              class="horse-profile-card__info-block"
              label="Дата поступления:"
              :value="arrivalDateLabel"
            />
          </div>

          <div class="horse-profile-card__description">
            <AppInfoItem
              label="Описание:"
              :value="horse.description || 'Описание отсутствует'"
            />
          </div>
        </div>
      </div>

      <AppButton
        outline
        no-caps
        icon="edit"
        label="Редактировать"
        class="horse-profile-card__edit-btn"
      />
    </div>
  </q-card>
</template>

<script setup>
import { computed } from 'vue'
import AppButton from 'src/components/ui/AppButton.vue'
import AppInfoItem from 'src/components/ui/AppInfoItem.vue'
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
