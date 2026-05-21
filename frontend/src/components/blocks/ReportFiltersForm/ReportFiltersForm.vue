<template>
  <AppFiltersGrid
    :class="$style.form"
    desktop-columns="repeat(2, minmax(0, 1fr))"
    tablet-columns="1fr"
  >
    <template v-for="field in activeDefinition.fields" :key="field">
      <AppFormField v-if="field === 'status'" label="Статус лошади">
        <AppReportFilterField
          field-type="select"
          :model-value="localFilters.status"
          :options="HORSE_STATUS_OPTIONS"
          @update:model-value="updateField('status', $event)"
        />
      </AppFormField>

      <AppFormField v-else-if="field === 'curator_id'" label="Куратор">
        <AppReportFilterField
          field-type="select"
          :model-value="localFilters.curator_id"
          :options="curatorOptions"
          @update:model-value="updateField('curator_id', $event)"
        />
      </AppFormField>

      <AppFormField v-else-if="field === 'horse_id'" label="Лошадь">
        <AppReportFilterField
          field-type="select"
          :model-value="localFilters.horse_id"
          :options="requiredHorseOptions"
          @update:model-value="updateField('horse_id', $event)"
        />
      </AppFormField>

      <AppFormField v-else-if="field === 'horse_id_optional'" label="Лошадь">
        <AppReportFilterField
          field-type="select"
          :model-value="localFilters.horse_id"
          :options="optionalHorseOptions"
          @update:model-value="updateField('horse_id', $event)"
        />
      </AppFormField>

      <AppFormField v-else-if="field === 'procedure_status'" label="Статус процедуры">
        <AppReportFilterField
          field-type="select"
          :model-value="localFilters.status"
          :options="PROCEDURE_STATUS_OPTIONS"
          @update:model-value="updateField('status', $event)"
        />
      </AppFormField>

      <AppFormField v-else-if="field === 'task_status'" label="Статус задачи">
        <AppReportFilterField
          field-type="select"
          :model-value="localFilters.status"
          :options="TASK_STATUS_OPTIONS"
          @update:model-value="updateField('status', $event)"
        />
      </AppFormField>

      <AppFormField v-else-if="field === 'user_task_status'" label="Статус задачи">
        <AppReportFilterField
          field-type="select"
          :model-value="localFilters.status"
          :options="USER_TASK_STATUS_OPTIONS"
          @update:model-value="updateField('status', $event)"
        />
      </AppFormField>

      <AppFormField v-else-if="field === 'user_id'" label="Пользователь">
        <AppReportFilterField
          field-type="select"
          :model-value="localFilters.user_id"
          :options="userOptions"
          @update:model-value="updateField('user_id', $event)"
        />
      </AppFormField>

      <AppFormField v-else-if="field === 'operation_type'" label="Тип операции">
        <AppReportFilterField
          field-type="select"
          :model-value="localFilters.operation_type"
          :options="FINANCE_OPERATION_TYPE_OPTIONS"
          @update:model-value="updateField('operation_type', $event)"
        />
      </AppFormField>

      <AppFormField v-else-if="field === 'category'" label="Категория">
        <AppReportFilterField
          field-type="select"
          :model-value="localFilters.category"
          :options="FINANCE_CATEGORY_OPTIONS"
          @update:model-value="updateField('category', $event)"
        />
      </AppFormField>

      <AppFormField v-else-if="field === 'date_from'" label="Дата начала">
        <AppReportFilterField
          field-type="date"
          :model-value="localFilters.date_from"
          @update:model-value="updateField('date_from', $event)"
        />
      </AppFormField>

      <AppFormField v-else-if="field === 'date_to'" label="Дата окончания">
        <AppReportFilterField
          field-type="date"
          :model-value="localFilters.date_to"
          @update:model-value="updateField('date_to', $event)"
        />
      </AppFormField>

      <label v-else-if="field === 'include_medical_records'" :class="$style.checkboxField">
        <q-checkbox
          :model-value="localFilters.include_medical_records"
          label="Включить медзаписи"
          @update:model-value="updateField('include_medical_records', $event)"
        />
      </label>

      <label v-else-if="field === 'include_procedures'" :class="$style.checkboxField">
        <q-checkbox
          :model-value="localFilters.include_procedures"
          label="Включить процедуры"
          @update:model-value="updateField('include_procedures', $event)"
        />
      </label>

      <label v-else-if="field === 'include_tasks'" :class="$style.checkboxField">
        <q-checkbox
          :model-value="localFilters.include_tasks"
          label="Включить задачи"
          @update:model-value="updateField('include_tasks', $event)"
        />
      </label>

      <label v-else-if="field === 'include_horses'" :class="$style.checkboxField">
        <q-checkbox
          :model-value="localFilters.include_horses"
          label="Включать лошадей"
          @update:model-value="updateField('include_horses', $event)"
        />
      </label>

      <label v-else-if="field === 'include_medicine'" :class="$style.checkboxField">
        <q-checkbox
          :model-value="localFilters.include_medicine"
          label="Включать медицину"
          @update:model-value="updateField('include_medicine', $event)"
        />
      </label>

      <label
        v-else-if="field === 'include_finance' && isAdmin"
        :class="$style.checkboxField"
      >
        <q-checkbox
          :model-value="localFilters.include_finance"
          label="Включать финансы"
          @update:model-value="updateField('include_finance', $event)"
        />
      </label>

      <label
        v-else-if="field === 'include_users' && isAdmin"
        :class="$style.checkboxField"
      >
        <q-checkbox
          :model-value="localFilters.include_users"
          label="Включать пользователей"
          @update:model-value="updateField('include_users', $event)"
        />
      </label>
    </template>
  </AppFiltersGrid>
</template>

<script setup>
import { computed } from 'vue'
import AppFiltersGrid from 'src/components/blocks/AppFiltersGrid/AppFiltersGrid.vue'
import AppFormField from 'src/components/ui/AppFormField/AppFormField.vue'
import AppReportFilterField from 'src/components/ui/AppReportFilterField/AppReportFilterField.vue'
import {
  FINANCE_CATEGORY_OPTIONS,
  FINANCE_OPERATION_TYPE_OPTIONS,
  HORSE_STATUS_OPTIONS,
  PROCEDURE_STATUS_OPTIONS,
  REPORT_TYPE_MAP,
  TASK_STATUS_OPTIONS,
  USER_TASK_STATUS_OPTIONS,
} from 'src/constants/reports'

const props = defineProps({
  reportType: {
    type: String,
    required: true,
  },
  filters: {
    type: Object,
    required: true,
  },
  horsesOptions: {
    type: Array,
    default: () => [],
  },
  usersOptions: {
    type: Array,
    default: () => [],
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:filters'])

const activeDefinition = computed(() => {
  return REPORT_TYPE_MAP[props.reportType]
})

const localFilters = computed(() => props.filters)

const optionalHorseOptions = computed(() => {
  return [{ label: 'Все лошади', value: null }, ...props.horsesOptions]
})

const requiredHorseOptions = computed(() => {
  return props.horsesOptions
})

const userOptions = computed(() => {
  return [{ label: 'Все пользователи', value: null }, ...props.usersOptions]
})

const curatorOptions = computed(() => {
  return [{ label: 'Все кураторы', value: null }, ...props.usersOptions]
})

const updateField = (key, value) => {
  emit('update:filters', {
    ...props.filters,
    [key]: value,
  })
}
</script>

<style module lang="scss" src="./ReportFiltersForm.module.scss"></style>
