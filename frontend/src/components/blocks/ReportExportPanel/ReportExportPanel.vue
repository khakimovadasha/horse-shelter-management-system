<template>
  <AppDataPanel
    title="Экспорт"
    subtitle="Сохраните отчёт в удобном формате"
  >
    <div :class="$style.actions">
      <AppButton
        :class="$style.exportButton"
        outline
        color="primary"
        icon="download"
        label="Экспорт в PDF"
        :loading="pdfLoading"
        :disable="disabled"
        @click="$emit('export', 'pdf')"
      />

      <AppButton
        :class="$style.exportButton"
        outline
        color="primary"
        icon="table_view"
        label="Экспорт в Excel"
        :loading="xlsxLoading"
        :disable="disabled"
        @click="$emit('export', 'xlsx')"
      />
    </div>

    <p :class="$style.note">
      Формат отчёта зависит от выбранного типа и параметров фильтрации
    </p>
  </AppDataPanel>
</template>

<script setup>
import AppDataPanel from 'src/components/blocks/AppDataPanel/AppDataPanel.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'

defineProps({
  disabled: {
    type: Boolean,
    default: true,
  },
  pdfLoading: {
    type: Boolean,
    default: false,
  },
  xlsxLoading: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['export'])
</script>

<style module lang="scss" src="./ReportExportPanel.module.scss"></style>
