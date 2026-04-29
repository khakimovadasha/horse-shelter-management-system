<template>
  <q-page :class="['page-container', $style.page]">
    <div :class="$style.header">
      <div>
        <h1 class="page-title">Лошади</h1>
        <p class="page-subtitle">
          Всего лошадей в приюте: {{ filteredHorses.length }}
        </p>
      </div>

      <AppButton
        v-if="isAdmin"
        icon="add"
        label="Добавить лошадь"
        color="primary"
        unelevated
        :class="$style.addButton"
        @click="openCreateDialog"
      />
    </div>

    <HorsesFilters
      class="q-mt-lg"
      v-model:search="searchQuery"
      v-model:status="selectedStatus"
      v-model:sort="selectedSort"
    />

    <div class="q-mt-xl">
      <div v-if="loading" :class="$style.state">
        Загрузка...
      </div>

      <div v-else-if="error" :class="[$style.state, $style.stateError]">
        Ошибка загрузки: {{ error }}
      </div>

      <div v-else-if="filteredHorses.length === 0" :class="$style.state">
        По выбранным параметрам лошади не найдены.
      </div>

      <template v-else>
        <div :class="$style.grid">
          <router-link
            v-for="horse in paginatedHorses"
            :key="horse.id"
            :to="`/app/horses/${horse.id}`"
            :class="$style.cardLink"
          >
            <HorseCard :horse="horse" />
          </router-link>
        </div>

        <div v-if="totalPages > 1" :class="$style.pagination">
          <AppPagination
            v-model="currentPage"
            :max="totalPages"
          />
        </div>
      </template>
    </div>

    <HorseCreateDialog
      v-model="isCreateDialogOpen"
      :curator-options="curatorOptions"
      :submitting="isCreatingHorse"
      @submit="handleCreateHorse"
    />
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useQuasar } from 'quasar'
import { createHorse } from 'src/api/horses'
import HorseCreateDialog from 'src/components/blocks/HorseCreateDialog/HorseCreateDialog.vue'
import HorseCard from 'src/components/blocks/HorseCard/HorseCard.vue'
import HorsesFilters from 'src/components/blocks/HorsesFilters/HorsesFilters.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppPagination from 'src/components/ui/AppPagination/AppPagination.vue'
import { useCurrentUserStore } from 'src/stores/currentUser'
import { useHorsesStore } from 'src/stores/horses'
import { useUsersStore } from 'src/stores/users'
import { canCreateHorse } from 'src/utils/permissions'

const $q = useQuasar()

const horsesStore = useHorsesStore()
const currentUserStore = useCurrentUserStore()
const usersStore = useUsersStore()

const { items: horses, loading, error } = storeToRefs(horsesStore)
const { user: currentUser } = storeToRefs(currentUserStore)
const { items: users } = storeToRefs(usersStore)

const PAGE_SIZE = 6

const searchQuery = ref('')
const selectedStatus = ref('all')
const selectedSort = ref('name_asc')
const currentPage = ref(1)
const isCreateDialogOpen = ref(false)
const isCreatingHorse = ref(false)

const statusOrder = {
  sick: 1,
  rehabilitation: 2,
  healthy: 3,
  deceased: 4,
}

const isAdmin = computed(() => canCreateHorse(currentUser.value))

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

const filteredHorses = computed(() => {
  let result = [...horses.value]

  const search = searchQuery.value.trim().toLowerCase()

  if (search) {
    result = result.filter((horse) =>
      horse.name?.toLowerCase().includes(search)
    )
  }

  if (selectedStatus.value !== 'all') {
    result = result.filter((horse) => horse.status === selectedStatus.value)
  }

  if (selectedSort.value === 'name_asc') {
    result.sort((a, b) => a.name.localeCompare(b.name, 'ru'))
  }

  if (selectedSort.value === 'arrival_date_desc') {
    result.sort(
      (a, b) => new Date(b.arrival_date) - new Date(a.arrival_date)
    )
  }

  if (selectedSort.value === 'status') {
    result.sort((a, b) => {
      const aOrder = statusOrder[a.status] ?? 999
      const bOrder = statusOrder[b.status] ?? 999
      return aOrder - bOrder
    })
  }

  return result
})

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredHorses.value.length / PAGE_SIZE))
})

const paginatedHorses = computed(() => {
  const startIndex = (currentPage.value - 1) * PAGE_SIZE
  const endIndex = startIndex + PAGE_SIZE
  return filteredHorses.value.slice(startIndex, endIndex)
})

const openCreateDialog = async () => {
  await usersStore.fetchUsers().catch(() => {
    $q.notify({
      type: 'negative',
      message: usersStore.error || 'Не удалось загрузить список кураторов',
    })
  })

  if (!usersStore.error) {
    isCreateDialogOpen.value = true
  }
}

const handleCreateHorse = async (payload) => {
  const formData = new FormData()
  formData.append('name', payload.name)
  formData.append('gender', payload.gender)
  formData.append('age', String(payload.age))
  formData.append('breed', payload.breed)
  formData.append('color', payload.color)
  formData.append('status', payload.status)
  formData.append('description', payload.description)
  formData.append('history', payload.history)
  formData.append('photo', payload.photo)

  if (payload.curator_id !== null && payload.curator_id !== undefined) {
    formData.append('curator_id', String(payload.curator_id))
  }

  isCreatingHorse.value = true

  try {
    const createdHorse = await createHorse(formData)
    horsesStore.prependHorse(createdHorse)
    currentPage.value = 1
    isCreateDialogOpen.value = false

    $q.notify({
      type: 'positive',
      message: 'Лошадь успешно добавлена',
    })
  } catch (err) {
    $q.notify({
      type: 'negative',
      message: err.response?.data?.detail || err.message || 'Не удалось добавить лошадь',
    })
  } finally {
    isCreatingHorse.value = false
  }
}

watch([searchQuery, selectedStatus, selectedSort], () => {
  currentPage.value = 1
})

watch(totalPages, (pages) => {
  if (currentPage.value > pages) {
    currentPage.value = pages
  }
})

onMounted(async () => {
  await Promise.all([
    horsesStore.fetchHorses().catch(() => {}),
    currentUserStore.fetchCurrentUser().catch(() => {}),
  ])
})
</script>

<style module lang="scss" src="./HorsesPage.module.scss"></style>
