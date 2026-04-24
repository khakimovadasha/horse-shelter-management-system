<template>
  <q-page :class="['page-container', $style.page]">
    <div v-if="loading" :class="$style.state">
      Загрузка...
    </div>

    <div v-else-if="error" :class="[$style.state, $style.stateError]">
      Ошибка загрузки: {{ error }}
    </div>

    <template v-else-if="horse">
      <router-link to="/app/horses" :class="$style.backLink">
        <q-icon name="arrow_back" size="20px" />
        <span>Назад</span>
      </router-link>

      <HorseProfileHeader :horse="horse" class="q-mt-lg" />

      <HorseDetailTabs class="q-mt-lg" />

      <HorseMedicalCardPanel :horse-id="horse.id" class="q-mt-lg" />
    </template>
  </q-page>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useHorseDetailsStore } from 'src/stores/horseDetails'

import HorseProfileHeader from 'src/components/blocks/HorseProfileHeader/HorseProfileHeader.vue'
import HorseDetailTabs from 'src/components/blocks/HorseDetailTabs/HorseDetailTabs.vue'
import HorseMedicalCardPanel from 'src/components/blocks/HorseMedicalCardPanel/HorseMedicalCardPanel.vue'

const route = useRoute()
const horseDetailsStore = useHorseDetailsStore()

const horseId = computed(() => String(route.params.id))
const horse = computed(() => horseDetailsStore.items[horseId.value] || null)
const loading = computed(() => Boolean(horseDetailsStore.loadingById[horseId.value]))
const error = computed(() => horseDetailsStore.errorById[horseId.value] || '')

const loadHorse = async () => {
  await horseDetailsStore.fetchHorse(horseId.value).catch(() => {})
}

onMounted(loadHorse)

watch(
  () => route.params.id,
  () => {
    loadHorse()
  }
)
</script>

<style module lang="scss" src="./HorsePage.module.scss"></style>
