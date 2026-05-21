<template>
  <AppDataPanel
    title="Параметры отчёта"
    subtitle="Настройте параметры для формирования отчёта"
  >
    <div :class="$style.form">
      <AppFormField label="Тип отчёта">
        <AppReportFilterField
          field-type="select"
          :model-value="reportType"
          :options="reportTypeOptions"
          @update:model-value="$emit('update:reportType', $event)"
        />
      </AppFormField>

      <ReportFiltersForm
        :report-type="reportType"
        :filters="filters"
        :horses-options="horsesOptions"
        :users-options="usersOptions"
        :is-admin="isAdmin"
        @update:filters="$emit('update:filters', $event)"
      />

      <AppButton
        color="primary"
        icon="description"
        label="Сформировать отчёт"
        unelevated
        :loading="loading"
        :disable="disableSubmit"
        @click="$emit('submit')"
      />
    </div>
  </AppDataPanel>
</template>

<script setup>
import AppDataPanel from 'src/components/blocks/AppDataPanel/AppDataPanel.vue'
import ReportFiltersForm from 'src/components/blocks/ReportFiltersForm/ReportFiltersForm.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppFormField from 'src/components/ui/AppFormField/AppFormField.vue'
import AppReportFilterField from 'src/components/ui/AppReportFilterField/AppReportFilterField.vue'

defineProps({
  reportType: {
    type: String,
    required: true,
  },
  reportTypeOptions: {
    type: Array,
    default: () => [],
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
  loading: {
    type: Boolean,
    default: false,
  },
  disableSubmit: {
    type: Boolean,
    default: false,
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['update:reportType', 'update:filters', 'submit'])
</script>

<style module lang="scss" src="./ReportBuilderPanel.module.scss"></style>

