<template>
  <AppDataPanel
    title="Список пользователей"
    subtitle="Управление учетными записями и правами доступа"
  >
    <div v-if="loading" :class="$style.state">
      Загрузка пользователей...
    </div>

    <div v-else-if="error" :class="[$style.state, $style.stateError]">
      Ошибка загрузки: {{ error }}
    </div>

    <AppDataTable
      v-else-if="!isMobile"
      :columns="columns"
      :rows="rows"
      row-key="id"
    >
      <template #empty>
        Нет пользователей.
      </template>

      <template #cell-name="{ row }">
        <div :class="$style.userCell">
          <div :class="$style.avatar">{{ row.initials }}</div>
          <div :class="$style.fullName">{{ row.name }}</div>
        </div>
      </template>

      <template #cell-email="{ row }">
        <div :class="$style.email">{{ row.email }}</div>
      </template>

      <template #cell-role="{ row }">
        <AppStatusBadge
          :label="row.roleLabel"
          :tone="row.roleTone"
        />
      </template>

      <template #cell-status="{ row }">
        <AppStatusBadge
          :label="row.statusLabel"
          :tone="row.statusTone"
        />
      </template>

      <template #cell-actions="{ row }">
        <div :class="$style.actions">
          <AppTableAction
            :label="isProcessing(row.id) ? 'Обновляется...' : (row.isActive ? 'Заблокировать' : 'Активировать')"
            :loading="isProcessing(row.id)"
            :disable="isProcessing(row.id)"
            @click="emit('toggle-active', row)"
          />

          <AppEditAction
            dense
            :disable="isProcessing(row.id)"
            :class="$style.menuButton"
            @click="emit('edit-role', row)"
          />
        </div>
      </template>
    </AppDataTable>

    <div v-else :class="$style.mobileList">
      <div v-if="rows.length === 0" :class="$style.state">
        Нет пользователей.
      </div>

      <article
        v-for="row in rows"
        v-else
        :key="row.id"
        :class="$style.mobileCard"
      >
        <div :class="$style.mobileHeader">
          <div :class="$style.userCell">
            <div :class="$style.avatar">{{ row.initials }}</div>
            <div>
              <div :class="$style.fullName">{{ row.name }}</div>
              <div :class="$style.email">{{ row.email }}</div>
            </div>
          </div>

          <AppEditAction
            dense
            :disable="isProcessing(row.id)"
            :class="$style.mobileEditAction"
            @click="emit('edit-role', row)"
          />
        </div>

        <div :class="$style.mobileBadges">
          <AppStatusBadge
            :label="row.roleLabel"
            :tone="row.roleTone"
          />
          <AppStatusBadge
            :label="row.statusLabel"
            :tone="row.statusTone"
          />
        </div>

        <div :class="$style.mobileActions">
          <AppTableAction
            :label="isProcessing(row.id) ? 'Обновляется...' : (row.isActive ? 'Заблокировать' : 'Активировать')"
            :loading="isProcessing(row.id)"
            :disable="isProcessing(row.id)"
            @click="emit('toggle-active', row)"
          />
        </div>
      </article>
    </div>
  </AppDataPanel>
</template>

<script setup>
import { computed } from 'vue'
import { useQuasar } from 'quasar'
import AppDataPanel from 'src/components/blocks/AppDataPanel/AppDataPanel.vue'
import AppDataTable from 'src/components/blocks/AppDataTable/AppDataTable.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'
import AppTableAction from 'src/components/ui/AppTableAction/AppTableAction.vue'
import AppEditAction from 'src/components/ui/AppEditAction/AppEditAction.vue'

const props = defineProps({
  rows: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
  processingIds: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['edit-role', 'toggle-active'])

const $q = useQuasar()
const isMobile = computed(() => $q.screen.lt.md)

const columns = computed(() => [
  { key: 'name', label: 'Имя' },
  { key: 'email', label: 'Email' },
  { key: 'role', label: 'Роль' },
  { key: 'status', label: 'Статус' },
  { key: 'actions', label: 'Действия', align: 'right' },
])

const isProcessing = (id) => props.processingIds.includes(id)
</script>

<style module lang="scss" src="./UsersTable.module.scss"></style>
