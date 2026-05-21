<template>
  <q-page class="page-container">
    <section :class="$style.header">
      <h1 :class="$style.title">Отчёты и выгрузки</h1>
      <p :class="$style.subtitle">Формирование отчётов для анализа данных</p>
    </section>

    <section :class="$style.topPanels">
      <ReportBuilderPanel
        :report-type="reportsStore.selectedReportType"
        :report-type-options="reportTypeOptions"
        :filters="reportsStore.activeFilters"
        :horses-options="reportsStore.horseOptions"
        :users-options="reportsStore.userOptions"
        :loading="reportsStore.loadingPreview"
        :disable-submit="reportsStore.loadingOptions"
        :is-admin="isAdminUser"
        @update:report-type="reportsStore.setReportType"
        @update:filters="reportsStore.updateActiveFilters"
        @submit="handleBuildReport"
      />

      <ReportExportPanel
        :disabled="!reportsStore.activePreview"
        :pdf-loading="reportsStore.exportLoading.pdf"
        :xlsx-loading="reportsStore.exportLoading.xlsx"
        @export="handleExport"
      />
    </section>

    <ReportPreviewPanel
      v-if="reportsStore.activePreview"
      :report="reportsStore.activePreview"
      :horses-options="reportsStore.horseOptions"
      :users-options="reportsStore.userOptions"
      :is-admin="isAdminUser"
    />
  </q-page>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useQuasar } from 'quasar'
import ReportBuilderPanel from 'src/components/blocks/ReportBuilderPanel/ReportBuilderPanel.vue'
import ReportExportPanel from 'src/components/blocks/ReportExportPanel/ReportExportPanel.vue'
import ReportPreviewPanel from 'src/components/blocks/ReportPreviewPanel/ReportPreviewPanel.vue'
import { getAvailableReportTypes } from 'src/constants/reports'
import { useCurrentUserStore } from 'src/stores/currentUser'
import { useReportsStore } from 'src/stores/reports'
import { isAdmin } from 'src/utils/permissions'

const $q = useQuasar()
const currentUserStore = useCurrentUserStore()
const reportsStore = useReportsStore()

const isAdminUser = computed(() => isAdmin(currentUserStore.user))

const reportTypeOptions = computed(() => {
  return getAvailableReportTypes(isAdminUser.value)
})

const parseFilename = (contentDisposition, fallback) => {
  const match = /filename="?([^";]+)"?/i.exec(contentDisposition || '')
  return match?.[1] || fallback
}

const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

const handleBuildReport = async () => {
  try {
    await reportsStore.buildReport(isAdminUser.value)
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.message || 'Не удалось сформировать отчёт.',
    })
  }
}

const handleExport = async (format) => {
  try {
    const { blob, contentDisposition } = await reportsStore.exportCurrentReport(
      format,
      isAdminUser.value,
    )

    const fallback = `report.${format === 'xlsx' ? 'xlsx' : 'pdf'}`
    downloadBlob(blob, parseFilename(contentDisposition, fallback))
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.message || 'Не удалось экспортировать отчёт.',
    })
  }
}

watch(
  reportTypeOptions,
  (value) => {
    reportsStore.ensureSelectedReportType(value)
  },
  { immediate: true },
)

onMounted(async () => {
  try {
    await reportsStore.loadOptions()
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.message || 'Не удалось загрузить параметры отчётов.',
    })
  }
})
</script>

<style module lang="scss" src="./ReportsPage.module.scss"></style>
