<template>
  <q-card :class="[$style.root, 'app-card']">
    <div :class="$style.top">
      <div :class="$style.main">
        <div :class="$style.imageWrap">
          <img :src="imageSrc" :alt="horse.name" :class="$style.image" />
        </div>

        <div :class="$style.content">
          <div :class="$style.titleRow">
            <div>
              <h1 :class="$style.name">{{ horse.name }}</h1>

              <AppStatusBadge
                :class="$style.status"
                :label="statusLabel"
                :tone="statusTone"
              />
            </div>
          </div>

          <div :class="$style.infoGrid">
            <AppInfoItem
              :class="$style.infoBlock"
              label="Порода:"
              :value="horse.breed || 'Не указана'"
            />
            <AppInfoItem
              :class="$style.infoBlock"
              label="Возраст:"
              :value="ageLabel"
            />
            <AppInfoItem
              :class="$style.infoBlock"
              label="Куратор:"
              value="Не назначен"
            />
            <AppInfoItem
              :class="$style.infoBlock"
              label="Дата поступления:"
              :value="arrivalDateLabel"
            />
          </div>

          <div :class="$style.description">
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
        :class="$style.editButton"
      />
    </div>
  </q-card>
</template>

<script setup>
import { computed } from 'vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppInfoItem from 'src/components/ui/AppInfoItem/AppInfoItem.vue'
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

<style module lang="scss" src="./HorseProfileHeader.module.scss"></style>
