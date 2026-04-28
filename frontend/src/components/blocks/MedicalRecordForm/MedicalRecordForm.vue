<template>
  <q-form :class="$style.form" @submit.prevent="handleSubmit">
    <div :class="$style.fieldsRow">
      <AppFormField label="Тип записи">
        <AppSelectField
          v-model="form.recordType"
          hide-bottom-space
          :class="$style.control"
          :options="recordTypeOptions"
          placeholder="Выберите тип записи"
          :error="Boolean(errors.recordType)"
          :error-message="errors.recordType"
        />
      </AppFormField>

      <AppFormField label="Следующая процедура">
        <AppTextField
          v-model="form.nextProcedureDate"
          hide-bottom-space
          :class="$style.control"
          type="date"
          :error="Boolean(errors.nextProcedureDate)"
          :error-message="errors.nextProcedureDate"
        />
      </AppFormField>
    </div>

    <AppFormField label="Заголовок">
      <AppTextField
        v-model="form.title"
        hide-bottom-space
        :class="$style.control"
        placeholder="Введите заголовок"
        :max-length="100"
        show-limit-warning
        :error="Boolean(errors.title)"
        :error-message="errors.title"
      />
    </AppFormField>

    <AppFormField label="Описание">
      <AppTextField
        v-model="form.description"
        hide-bottom-space
        :class="[$style.control, $style.controlTextarea]"
        type="textarea"
        autogrow
        placeholder="Опишите запись"
        :error="Boolean(errors.description)"
        :error-message="errors.description"
      />
    </AppFormField>

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
import AppFormField from 'src/components/ui/AppFormField/AppFormField.vue'
import AppSelectField from 'src/components/ui/AppSelectField/AppSelectField.vue'
import AppTextField from 'src/components/ui/AppTextField/AppTextField.vue'

const recordTypeOptions = [
  { label: 'Осмотр', value: 'inspection' },
  { label: 'Диагноз', value: 'diagnosis' },
  { label: 'Лечение', value: 'treatment' },
  { label: 'Анализ', value: 'analysis' },
  { label: 'Процедура', value: 'procedure' },
  { label: 'Заметка', value: 'note' },
]

const createInitialForm = () => ({
  recordType: null,
  title: '',
  description: '',
  nextProcedureDate: '',
})

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
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

const resetForm = () => {
  form.value = createInitialForm()
  errors.value = {}
}

const validateForm = () => {
  const nextErrors = {}

  if (!form.value.recordType) nextErrors.recordType = 'Выберите тип записи'
  if (!form.value.title.trim()) nextErrors.title = 'Укажите заголовок'
  if (!form.value.description.trim()) nextErrors.description = 'Добавьте описание'

  errors.value = nextErrors

  return Object.keys(nextErrors).length === 0
}

const handleSubmit = () => {
  if (!validateForm()) {
    return
  }

  emit('submit', {
    record_type: form.value.recordType,
    title: form.value.title.trim(),
    description: form.value.description.trim(),
    next_procedure_date: form.value.nextProcedureDate || null,
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
  },
  { immediate: true }
)
</script>

<style module lang="scss" src="./MedicalRecordForm.module.scss"></style>
