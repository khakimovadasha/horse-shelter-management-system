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

      <HorseProfileHeader
        :horse="horse"
        :can-edit="canEditHorse"
        class="q-mt-lg"
        @edit="openEditDialog"
      />

      <HorseDetailTabs class="q-mt-lg" />

      <HorseMedicalCardPanel :horse-id="horse.id" class="q-mt-lg" />

      <HorseEditDialog
        v-model="isEditDialogOpen"
        :horse="horse"
        :curator-options="curatorOptions"
        :submitting="isUpdatingHorse"
        @submit="handleUpdateHorse"
      />
    </template>
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { Notify } from 'quasar'
import { useRoute } from 'vue-router'
import { updateHorse } from 'src/api/horses'
import HorseEditDialog from 'src/components/blocks/HorseEditDialog/HorseEditDialog.vue'
import HorseProfileHeader from 'src/components/blocks/HorseProfileHeader/HorseProfileHeader.vue'
import HorseDetailTabs from 'src/components/blocks/HorseDetailTabs/HorseDetailTabs.vue'
import HorseMedicalCardPanel from 'src/components/blocks/HorseMedicalCardPanel/HorseMedicalCardPanel.vue'
import { useCurrentUserStore } from 'src/stores/currentUser'
import { useHorseDetailsStore } from 'src/stores/horseDetails'
import { useHorsesStore } from 'src/stores/horses'
import { useUsersStore } from 'src/stores/users'
import { notifySuccess } from 'src/utils/notifySuccess'
import { canEditHorse as canEditHorsePermission } from 'src/utils/permissions'

const route = useRoute()
const horseDetailsStore = useHorseDetailsStore()
const currentUserStore = useCurrentUserStore()
const horsesStore = useHorsesStore()
const usersStore = useUsersStore()

const { user: currentUser } = storeToRefs(currentUserStore)
const { items: users } = storeToRefs(usersStore)

const horseId = computed(() => String(route.params.id))
const horse = computed(() => horseDetailsStore.items[horseId.value] || null)
const loading = computed(() => Boolean(horseDetailsStore.loadingById[horseId.value]))
const error = computed(() => horseDetailsStore.errorById[horseId.value] || '')
const isEditDialogOpen = ref(false)
const isUpdatingHorse = ref(false)

const canEditHorse = computed(() => canEditHorsePermission(currentUser.value))

const curatorOptions = computed(() => {
  const activeUsers = [...users.value]
    .filter((user) => user.is_active)
    .map((user) => ({
      label: `${user.first_name} ${user.last_name}`.trim(),
      value: user.id,
    }))
    .sort((a, b) => a.label.localeCompare(b.label, 'ru'))

  return [
    { label: 'Не указан', value: null },
    ...activeUsers,
  ]
})

const loadHorse = async () => {
  await horseDetailsStore.fetchHorse(horseId.value).catch(() => {})
}

const openEditDialog = async () => {
  if (!canEditHorse.value) {
    return
  }

  await usersStore.fetchUsers().catch(() => {
    Notify.create({
      type: 'negative',
      message: usersStore.error || 'Не удалось загрузить список кураторов',
    })
  })

  if (!usersStore.error) {
    isEditDialogOpen.value = true
  }
}

const handleUpdateHorse = async (payload) => {
  const formData = new FormData()
  formData.append('name', payload.name)
  formData.append('gender', payload.gender)
  formData.append('age', String(payload.age))
  formData.append('breed', payload.breed)
  formData.append('color', payload.color)
  formData.append('arrival_date', payload.arrival_date)
  formData.append('status', payload.status)
  formData.append('curator_id', payload.curator_id === null ? '' : String(payload.curator_id))
  formData.append('description', payload.description)
  formData.append('history', payload.history)

  if (payload.photo) {
    formData.append('photo', payload.photo)
  }

  isUpdatingHorse.value = true

  try {
    const updatedHorse = await updateHorse(horseId.value, formData)
    horseDetailsStore.updateHorse(updatedHorse)
    horsesStore.updateHorse(updatedHorse)
    isEditDialogOpen.value = false

    notifySuccess('Карточка лошади успешно обновлена')
  } catch (err) {
    Notify.create({
      type: 'negative',
      message:
        err.response?.data?.detail || err.message || 'Не удалось обновить карточку лошади',
    })
  } finally {
    isUpdatingHorse.value = false
  }
}

onMounted(loadHorse)

onMounted(() => {
  currentUserStore.fetchCurrentUser().catch(() => {})
})

watch(
  () => route.params.id,
  () => {
    loadHorse()
    isEditDialogOpen.value = false
  }
)
</script>

<style module lang="scss" src="./HorsePage.module.scss"></style>
