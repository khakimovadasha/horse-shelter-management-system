<template>
  <AppDataPanel
    title="Журнал операций"
    subtitle="История финансовых транзакций"
  >
    <div v-if="loading" :class="$style.state">
      Загрузка операций...
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
        Нет финансовых операций.
      </template>

      <template #cell-date="{ row }">
        {{ row.date }}
      </template>

      <template #cell-operationType="{ row }">
        <div :class="[$style.typeBadge, row.operationType === 'income' ? $style.typeBadgeIncome : $style.typeBadgeExpense]">
          <q-icon
            :name="row.operationType === 'income' ? 'trending_up' : 'trending_down'"
            size="16px"
          />
          <span>{{ row.operationTypeLabel }}</span>
        </div>
      </template>

      <template #cell-category="{ row }">
        <div :class="$style.categoryBadge">
          {{ row.categoryLabel }}
        </div>
      </template>

      <template #cell-description="{ row }">
        <div :class="$style.descriptionCell">{{ row.description }}</div>
      </template>

      <template #cell-amount="{ row }">
        <span :class="[row.operationType === 'income' ? $style.amountIncome : $style.amountExpense]">
          {{ row.amount }}
        </span>
      </template>
    </AppDataTable>

    <div v-else :class="$style.mobileList">
      <div v-if="rows.length === 0" :class="$style.state">
        Нет финансовых операций.
      </div>

      <article
        v-for="row in rows"
        v-else
        :key="row.id"
        :class="$style.mobileCard"
      >
        <div :class="$style.mobileHeader">
          <div :class="$style.mobileDate">{{ row.date }}</div>
          <div :class="[row.operationType === 'income' ? $style.amountIncome : $style.amountExpense, $style.mobileAmount]">
            {{ row.amount }}
          </div>
        </div>

        <div :class="$style.mobileBadges">
          <div :class="[$style.typeBadge, row.operationType === 'income' ? $style.typeBadgeIncome : $style.typeBadgeExpense]">
            <q-icon
              :name="row.operationType === 'income' ? 'trending_up' : 'trending_down'"
              size="16px"
            />
            <span>{{ row.operationTypeLabel }}</span>
          </div>

          <div :class="$style.categoryBadge">
            {{ row.categoryLabel }}
          </div>
        </div>

        <div :class="$style.mobileDescription">
          {{ row.description }}
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

defineProps({
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
})

const $q = useQuasar()
const isMobile = computed(() => $q.screen.lt.md)

const columns = computed(() => [
  { key: 'date', label: 'Дата' },
  { key: 'operationType', label: 'Тип' },
  { key: 'category', label: 'Категория' },
  { key: 'description', label: 'Описание' },
  { key: 'amount', label: 'Сумма', align: 'right' },
])
</script>

<style module lang="scss" src="./FinanceOperationsTable.module.scss"></style>
