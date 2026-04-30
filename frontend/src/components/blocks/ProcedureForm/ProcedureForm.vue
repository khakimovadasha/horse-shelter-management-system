<template>
  <q-form :class="$style.form" @submit.prevent="handleSubmit">
    <div :class="$style.fieldsRow">
      <AppFormField label="Лошадь">
        <AppSelectField
          v-model="form.horseId"
          hide-bottom-space
          :class="$style.control"
          :options="horseOptions"
          placeholder="Выберите лошадь"
          :error="Boolean(errors.horseId)"
          :error-message="errors.horseId"
        />
      </AppFormField>

      <AppFormField label="Дата процедуры">
        <AppTextField
          v-model="form.plannedDate"
          hide-bottom-space
          :class="$style.control"
          type="date"
          :error="Boolean(errors.plannedDate)"
          :error-message="errors.plannedDate"
        />
      </AppFormField>
    </div>

    <AppFormField label="Название процедуры">
      <AppSelectField
        v-model="form.procedureName"
        hide-bottom-space
        :class="$style.control"
        :options="filteredProcedureOptions"
        placeholder="Выберите или введите процедуру"
        use-input
        fill-input
        hide-selected
        input-debounce="0"
        new-value-mode="add-unique"
        :error="Boolean(errors.procedureName)"
        :error-message="errors.procedureName"
        @filter="filterProcedureOptions"
        @new-value="handleProcedureNameNewValue"
      />
    </AppFormField>

    <AppFormField label="Описание">
      <AppTextField
        v-model="form.notes"
        hide-bottom-space
        :class="[$style.control, $style.controlTextarea]"
        type="textarea"
        autogrow
        placeholder="Кратко опишите, что нужно сделать"
        :error="Boolean(errors.notes)"
        :error-message="errors.notes"
      />
    </AppFormField>

    <div :class="$style.checkboxRow">
      <AppCheckboxField v-model="form.addToMedicalRecord">
        Добавить в медкарту после выполнения
      </AppCheckboxField>
    </div>

    <AppFormActions>
      <AppButton
        outline
        no-caps
        label="Отмена"
        type="button"
        :class="$style.secondaryButton"
        :disable="submitting"
        @click="$emit('cancel')"
      />
      <AppButton
        color="primary"
        unelevated
        no-caps
        :label="submitLabel"
        type="submit"
        :class="$style.primaryButton"
        :loading="submitting"
        :disable="submitting"
      />
    </AppFormActions>
  </q-form>
</template>

<script setup>
import { ref, watch } from 'vue'
import AppFormActions from 'src/components/blocks/AppFormActions/AppFormActions.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppCheckboxField from 'src/components/ui/AppCheckboxField/AppCheckboxField.vue'
import AppFormField from 'src/components/ui/AppFormField/AppFormField.vue'
import AppSelectField from 'src/components/ui/AppSelectField/AppSelectField.vue'
import AppTextField from 'src/components/ui/AppTextField/AppTextField.vue'

const BASE_PROCEDURE_OPTIONS = [
  'Вакцинация',
  'Дегельминтизация',
  'Осмотр',
  'Инъекция',
  'Капельница',
  'Перевязка',
  'Обработка раны',
  'Физиотерапия',
  'Расчистка копыт',
  'Другое...',
].map((name) => ({
  label: name,
  value: name,
}))

const createInitialForm = () => ({
  horseId: null,
  procedureName: '',
  notes: '',
  plannedDate: '',
  addToMedicalRecord: false,
})

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  horseOptions: {
    type: Array,
    default: () => [],
  },
  submitting: {
    type: Boolean,
    default: false,
  },
  submitLabel: {
    type: String,
    default: 'Сохранить',
  },
})

const emit = defineEmits(['submit', 'cancel'])

const form = ref(createInitialForm())
const errors = ref({})
const customProcedureOption = ref(null)
const filteredProcedureOptions = ref([...BASE_PROCEDURE_OPTIONS])

const getProcedureOptions = (search = '') => {
  const normalizedSearch = search.trim().toLowerCase()
  const baseOptions = normalizedSearch
    ? BASE_PROCEDURE_OPTIONS.filter((option) =>
        option.label.toLowerCase().includes(normalizedSearch)
      )
    : [...BASE_PROCEDURE_OPTIONS]

  if (
    customProcedureOption.value &&
    !baseOptions.some((option) => option.value === customProcedureOption.value.value)
  ) {
    return [customProcedureOption.value, ...baseOptions]
  }

  return baseOptions
}

const resetForm = () => {
  form.value = createInitialForm()
  errors.value = {}
  customProcedureOption.value = null
  filteredProcedureOptions.value = getProcedureOptions()
}

const filterProcedureOptions = (value, update) => {
  update(() => {
    filteredProcedureOptions.value = getProcedureOptions(value)
  })
}

const handleProcedureNameNewValue = (value, done) => {
  const normalized = value.trim()

  if (!normalized) {
    done()
    return
  }

  customProcedureOption.value = {
    label: normalized,
    value: normalized,
  }
  filteredProcedureOptions.value = getProcedureOptions()
  done(normalized, 'add-unique')
}

const validateForm = () => {
  const nextErrors = {}

  if (!form.value.horseId) nextErrors.horseId = 'Выберите лошадь'

  const procedureName = form.value.procedureName.trim()
  if (!procedureName) {
    nextErrors.procedureName = 'Укажите название процедуры'
  } else if (procedureName === 'Другое...') {
    nextErrors.procedureName = 'Введите собственное название процедуры'
  } else if (procedureName.length > 100) {
    nextErrors.procedureName = 'Название процедуры не должно превышать 100 символов'
  }

  if (!form.value.plannedDate) nextErrors.plannedDate = 'Укажите дату процедуры'
  if (!form.value.notes.trim()) nextErrors.notes = 'Добавьте краткое описание процедуры'

  errors.value = nextErrors

  return Object.keys(nextErrors).length === 0
}

const handleSubmit = () => {
  if (!validateForm()) {
    return
  }

  emit('submit', {
    horse_id: form.value.horseId,
    procedure_name: form.value.procedureName.trim(),
    notes: form.value.notes.trim(),
    planned_date: `${form.value.plannedDate}T00:00:00`,
    add_to_medical_record: form.value.addToMedicalRecord,
  })
}

watch(
  () => props.isOpen,
  (isOpen) => {
    if (isOpen) {
      resetForm()
      return
    }

    errors.value = {}
    filteredProcedureOptions.value = getProcedureOptions()
  },
  { immediate: true }
)

watch(
  () => form.value.procedureName,
  (value) => {
    const normalized = value.trim()

    if (!normalized || BASE_PROCEDURE_OPTIONS.some((option) => option.value === normalized)) {
      customProcedureOption.value = null
      filteredProcedureOptions.value = getProcedureOptions()
      return
    }

    customProcedureOption.value = {
      label: normalized,
      value: normalized,
    }
    filteredProcedureOptions.value = getProcedureOptions()
  }
)
</script>

<style module lang="scss" src="./ProcedureForm.module.scss"></style>
