import { defineStore } from 'pinia'
import { exportReport, getReportFilterOptions, getReportPreview } from 'src/api/reports'
import { createInitialFiltersByType, REPORT_TYPE_DEFINITIONS, REPORT_TYPES } from 'src/constants/reports'

const createEmptyOptions = () => ({
  horses: [],
  users: [],
})

const createEmptyExportLoading = () => ({
  pdf: false,
  xlsx: false,
})

const createInitialPreviews = () =>
  Object.fromEntries(REPORT_TYPE_DEFINITIONS.map(({ value }) => [value, null]))

const createInitialBuiltParams = () =>
  Object.fromEntries(REPORT_TYPE_DEFINITIONS.map(({ value }) => [value, null]))

export const useReportsStore = defineStore('reports', {
  state: () => ({
    selectedReportType: REPORT_TYPE_DEFINITIONS[0]?.value || REPORT_TYPES.all_horses,
    filtersByType: createInitialFiltersByType(),
    previewByType: createInitialPreviews(),
    lastBuiltParamsByType: createInitialBuiltParams(),
    reportOptions: createEmptyOptions(),
    loadingOptions: false,
    loadingPreview: false,
    exportLoading: createEmptyExportLoading(),
    optionsLoaded: false,
    error: '',
  }),

  getters: {
    activeFilters(state) {
      return state.filtersByType[state.selectedReportType]
    },

    activePreview(state) {
      return state.previewByType[state.selectedReportType]
    },

    horseOptions(state) {
      return state.reportOptions.horses.map((horse) => ({
        label: horse.name,
        value: horse.id,
      }))
    },

    userOptions(state) {
      return state.reportOptions.users.map((user) => ({
        label: user.full_name,
        value: user.id,
      }))
    },
  },

  actions: {
    clearReports() {
      this.selectedReportType = REPORT_TYPE_DEFINITIONS[0]?.value || REPORT_TYPES.all_horses
      this.filtersByType = createInitialFiltersByType()
      this.previewByType = createInitialPreviews()
      this.lastBuiltParamsByType = createInitialBuiltParams()
      this.reportOptions = createEmptyOptions()
      this.loadingOptions = false
      this.loadingPreview = false
      this.exportLoading = createEmptyExportLoading()
      this.optionsLoaded = false
      this.error = ''
    },

    ensureSelectedReportType(availableTypes) {
      const availableValues = availableTypes.map((item) => item.value)

      if (!availableValues.includes(this.selectedReportType)) {
        this.selectedReportType = availableValues[0] || REPORT_TYPE_DEFINITIONS[0]?.value || REPORT_TYPES.all_horses
      }
    },

    setReportType(value) {
      this.selectedReportType = value
    },

    updateActiveFilters(value) {
      this.filtersByType = {
        ...this.filtersByType,
        [this.selectedReportType]: value,
      }
    },

    buildParams(reportType, isAdminUser) {
      const params = { ...(this.filtersByType[reportType] || {}) }

      if (!isAdminUser && reportType === REPORT_TYPES.shelter_summary) {
        params.include_finance = false
        params.include_users = false
      }

      return params
    },

    getFriendlyReportError(error, fallbackMessage) {
      const detail = error?.response?.data?.detail

      if (detail === 'Для диапазона нужно передать и date_from, и date_to') {
        return 'Для отчёта нужно заполнить и дату начала, и дату окончания.'
      }

      if (detail === 'Дата начала не может быть больше даты окончания') {
        return 'Дата начала не может быть позже даты окончания.'
      }

      if (detail === 'Лошадь не найдена') {
        return 'Выбранная лошадь не найдена.'
      }

      if (detail === 'Пользователь не найден') {
        return 'Выбранный пользователь не найден.'
      }

      if (detail === 'Нет доступа') {
        return 'У вас нет доступа к этому отчёту.'
      }

      if (typeof detail === 'string' && detail.trim()) {
        return detail
      }

      return fallbackMessage
    },

    validateFilters(reportType) {
      const filters = this.filtersByType[reportType] || {}

      if (
        [
          REPORT_TYPES.medical_procedures,
          REPORT_TYPES.all_tasks,
          REPORT_TYPES.finance,
          REPORT_TYPES.shelter_summary,
        ].includes(reportType)
      ) {
        if ((filters.date_from && !filters.date_to) || (!filters.date_from && filters.date_to)) {
          return 'Для отчёта нужно заполнить и дату начала, и дату окончания.'
        }

        if (
          filters.date_from &&
          filters.date_to &&
          new Date(filters.date_from).getTime() > new Date(filters.date_to).getTime()
        ) {
          return 'Дата начала не может быть позже даты окончания.'
        }
      }

      if (reportType === REPORT_TYPES.horse_detail && !filters.horse_id) {
        return 'Для этого отчёта нужно выбрать лошадь.'
      }

      return ''
    },

    async loadOptions(force = false) {
      if (this.loadingOptions) {
        return this.reportOptions
      }

      if (this.optionsLoaded && !force) {
        return this.reportOptions
      }

      this.loadingOptions = true
      this.error = ''

      try {
        this.reportOptions = await getReportFilterOptions()
        this.optionsLoaded = true
        return this.reportOptions
      } catch (error) {
        this.error = this.getFriendlyReportError(error, 'Не удалось загрузить параметры отчётов.')
        throw new Error(this.error)
      } finally {
        this.loadingOptions = false
      }
    },

    async buildReport(isAdminUser) {
      const reportType = this.selectedReportType
      const validationError = this.validateFilters(reportType)

      if (validationError) {
        throw new Error(validationError)
      }

      this.loadingPreview = true
      this.error = ''

      try {
        const params = this.buildParams(reportType, isAdminUser)
        const preview = await getReportPreview(reportType, params)

        this.previewByType = {
          ...this.previewByType,
          [reportType]: preview,
        }
        this.lastBuiltParamsByType = {
          ...this.lastBuiltParamsByType,
          [reportType]: params,
        }

        return preview
      } catch (error) {
        this.error = this.getFriendlyReportError(error, 'Не удалось сформировать отчёт.')
        throw new Error(this.error)
      } finally {
        this.loadingPreview = false
      }
    },

    async exportCurrentReport(format, isAdminUser) {
      const reportType = this.selectedReportType
      const validationError = this.validateFilters(reportType)

      if (validationError) {
        throw new Error(validationError)
      }

      this.exportLoading = {
        ...this.exportLoading,
        [format]: true,
      }
      this.error = ''

      try {
        const params = this.lastBuiltParamsByType[reportType] || this.buildParams(reportType, isAdminUser)
        const result = await exportReport(reportType, params, format)

        return result
      } catch (error) {
        this.error = this.getFriendlyReportError(error, 'Не удалось экспортировать отчёт.')
        throw new Error(this.error)
      } finally {
        this.exportLoading = {
          ...this.exportLoading,
          [format]: false,
        }
      }
    },
  },
})
