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
        />
      </AppFormField>

      <AppFormField label="Дата и время">
        <AppTextField
          v-model="form.dueDate"
          hide-bottom-space
          :class="$style.control"
          type="datetime-local"
          :error="Boolean(errors.dueDate)"
          :error-message="errors.dueDate"
        />
      </AppFormField>
    </div>

    <AppFormField label="Название задачи">
      <AppTextField
        v-model="form.title"
        hide-bottom-space
        :class="$style.control"
        placeholder="Введите название задачи"
        :max-length="TITLE_MAX_LENGTH"
        show-counter
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
        placeholder="Опишите задачу"
        :max-length="DESCRIPTION_MAX_LENGTH"
        show-counter
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

const TITLE_MAX_LENGTH = 100
const DESCRIPTION_MAX_LENGTH = 255

const createInitialForm = () => ({
  horseId: null,
  title: '',
  description: '',
  dueDate: '',
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

const resetForm = () => {
  form.value = createInitialForm()
  errors.value = {}
}

const validateForm = () => {
  const nextErrors = {}

  if (!form.value.title.trim()) {
    nextErrors.title = 'Укажите название задачи'
  }

  if (!form.value.description.trim()) {
    nextErrors.description = 'Добавьте описание задачи'
  }

  if (!form.value.dueDate) {
    nextErrors.dueDate = 'Укажите дату и время задачи'
  }

  errors.value = nextErrors

  return Object.keys(nextErrors).length === 0
}

const normalizeDueDate = (value) => {
  if (value.length === 16) {
    return `${value}:00`
  }

  return value
}

const handleSubmit = () => {
  if (!validateForm()) {
    return
  }

  emit('submit', {
    title: form.value.title.trim(),
    description: form.value.description.trim(),
    horse_id: form.value.horseId || null,
    due_date: normalizeDueDate(form.value.dueDate),
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

<style module lang="scss" src="./TaskForm.module.scss"></style>
