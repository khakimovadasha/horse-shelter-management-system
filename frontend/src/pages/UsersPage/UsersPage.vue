<template>
  <q-page class="page-container">
    <div :class="$style.header">
      <h1 class="page-title">Управление пользователями</h1>
      <p class="page-subtitle">Всего пользователей: {{ users.length }}</p>
    </div>

    <div :class="$style.filtersSection">
      <UsersFilters
        v-model:role="roleFilter"
        v-model:status="statusFilter"
      />
    </div>

    <div :class="$style.tableSection">
      <UsersTable
        :rows="paginatedRows"
        :loading="loading"
        :error="error"
        :processing-ids="processingIds"
        @edit-role="openRoleDialog"
        @toggle-active="handleToggleActive"
      />
    </div>

    <div :class="$style.pagination">
      <AppPagination
        v-model="currentPage"
        :max="totalPages"
      />
    </div>

    <UserRoleEditDialog
      v-model="isRoleDialogOpen"
      :initial-role="editingUser?.role ?? null"
      :submitting="isRoleSubmitting"
      @submit="handleSubmitRole"
    />
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { Notify } from 'quasar'
import UserRoleEditDialog from 'src/components/blocks/UserRoleEditDialog/UserRoleEditDialog.vue'
import UsersFilters from 'src/components/blocks/UsersFilters/UsersFilters.vue'
import UsersTable from 'src/components/blocks/UsersTable/UsersTable.vue'
import AppPagination from 'src/components/ui/AppPagination/AppPagination.vue'
import { updateUserActive, updateUserRole } from 'src/api/users'
import { useUsersStore } from 'src/stores/users'
import { notifySuccess } from 'src/utils/notifySuccess'

const PAGE_SIZE = 8

const usersStore = useUsersStore()
const { items: users, loading, error } = storeToRefs(usersStore)

const roleFilter = ref('all')
const statusFilter = ref('all')
const currentPage = ref(1)
const processingIds = ref([])
const isRoleDialogOpen = ref(false)
const editingUser = ref(null)

const rolePresentation = {
  admin: { label: 'Администратор', tone: 'admin' },
  veterinarian: { label: 'Ветеринар', tone: 'veterinarian' },
  user: { label: 'Волонтёр', tone: 'volunteer' },
}

const filteredUsers = computed(() => {
  return users.value.filter((user) => {
    const matchesRole = roleFilter.value === 'all' || user.role === roleFilter.value
    const matchesStatus = statusFilter.value === 'all'
      || (statusFilter.value === 'active' && user.is_active)
      || (statusFilter.value === 'blocked' && !user.is_active)

    return matchesRole && matchesStatus
  })
})

const tableRows = computed(() => {
  return filteredUsers.value.map((user) => {
    const roleData = rolePresentation[user.role] || { label: user.role, tone: 'default' }
    const firstInitial = user.first_name?.trim()?.[0] || ''
    const lastInitial = user.last_name?.trim()?.[0] || ''

    return {
      id: user.id,
      name: `${user.first_name} ${user.last_name}`.trim(),
      initials: `${firstInitial}${lastInitial}`.toUpperCase() || 'П',
      email: user.email,
      role: user.role,
      roleLabel: roleData.label,
      roleTone: roleData.tone,
      isActive: user.is_active,
      statusLabel: user.is_active ? 'Активен' : 'Заблокирован',
      statusTone: user.is_active ? 'active' : 'blocked',
    }
  })
})

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(tableRows.value.length / PAGE_SIZE))
})

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  const end = start + PAGE_SIZE

  return tableRows.value.slice(start, end)
})

const isRoleSubmitting = computed(() => {
  return editingUser.value ? processingIds.value.includes(editingUser.value.id) : false
})

const markProcessing = (userId, isProcessing) => {
  if (isProcessing) {
    processingIds.value = [...new Set([...processingIds.value, userId])]
    return
  }

  processingIds.value = processingIds.value.filter((id) => id !== userId)
}

const openRoleDialog = (row) => {
  editingUser.value = row
  isRoleDialogOpen.value = true
}

const closeRoleDialog = () => {
  isRoleDialogOpen.value = false
  editingUser.value = null
}

const handleSubmitRole = async (nextRole) => {
  if (!editingUser.value) {
    return
  }

  const userId = editingUser.value.id

  markProcessing(userId, true)

  try {
    const updatedUser = await updateUserRole(userId, nextRole)
    usersStore.replaceUser(updatedUser)
    notifySuccess('Роль пользователя успешно обновлена')
    closeRoleDialog()
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось изменить роль пользователя',
    })
  } finally {
    markProcessing(userId, false)
  }
}

const handleToggleActive = async (row) => {
  markProcessing(row.id, true)

  try {
    const updatedUser = await updateUserActive(row.id, !row.isActive)
    usersStore.replaceUser(updatedUser)
    notifySuccess(
      updatedUser.is_active
        ? 'Пользователь успешно разблокирован'
        : 'Пользователь успешно заблокирован'
    )
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось изменить статус пользователя',
    })
  } finally {
    markProcessing(row.id, false)
  }
}

watch([roleFilter, statusFilter], () => {
  currentPage.value = 1
})

watch(totalPages, (nextTotalPages) => {
  if (currentPage.value > nextTotalPages) {
    currentPage.value = nextTotalPages
  }
})

onMounted(() => {
  usersStore.fetchUsers(true).catch(() => {})
})
</script>

<style module lang="scss" src="./UsersPage.module.scss"></style>
