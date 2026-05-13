<template>
  <q-form :class="$style.form" @submit.prevent="handleSubmit">
    <AppFormField label="Тип операции">
      <AppSelectField
        v-model="form.operationType"
        hide-bottom-space
        :class="$style.control"
        :options="typeOptions"
        placeholder="Выберите тип"
        :error="Boolean(errors.operationType)"
        :error-message="errors.operationType"
      />
    </AppFormField>

    <AppFormField label="Категория">
      <AppSelectField
        v-model="form.category"
        hide-bottom-space
        :class="$style.control"
        :options="filteredCategoryOptions"
        placeholder="Выберите категорию"
        :disable="!form.operationType"
        :error="Boolean(errors.category)"
        :error-message="errors.category"
      />
    </AppFormField>

    <AppFormField label="Сумма">
      <AppTextField
        v-model="form.amount"
        hide-bottom-space
        :class="$style.control"
        type="number"
        min="0"
        step="0.01"
        placeholder="0"
        :error="Boolean(errors.amount)"
        :error-message="errors.amount"
      />
    </AppFormField>

    <AppFormField label="Описание">
      <AppTextField
        v-model="form.description"
        hide-bottom-space
        :class="[$style.control, $style.controlTextarea]"
        type="textarea"
        autogrow
        placeholder="Краткое описание"
        :max-length="DESCRIPTION_MAX_LENGTH"
        show-counter
        :error="Boolean(errors.description)"
        :error-message="errors.description"
      />
    </AppFormField>

    <AppFormField label="Дата">
      <AppTextField
        v-model="form.date"
        hide-bottom-space
        :class="$style.control"
        type="date"
        :error="Boolean(errors.date)"
        :error-message="errors.date"
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
import { computed, ref, watch } from 'vue'
import AppFormActions from 'src/components/blocks/AppFormActions/AppFormActions.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppFormField from 'src/components/ui/AppFormField/AppFormField.vue'
import AppSelectField from 'src/components/ui/AppSelectField/AppSelectField.vue'
import AppTextField from 'src/components/ui/AppTextField/AppTextField.vue'

const DESCRIPTION_MAX_LENGTH = 255

const typeOptions = [
  { label: 'Доход', value: 'income' },
  { label: 'Расход', value: 'expense' },
]

const incomeCategoryOptions = [
  { label: 'Пожертвования', value: 'donations' },
  { label: 'Спонсорство', value: 'sponsorship' },
  { label: 'Гранты', value: 'grants' },
  { label: 'Продажи', value: 'sales' },
  { label: 'Прочие поступления', value: 'other_income' },
]

const expenseCategoryOptions = [
  { label: 'Медикаменты', value: 'medications' },
  { label: 'Корма', value: 'feed' },
  { label: 'Уход и содержание', value: 'care' },
  { label: 'Инвентарь и оборудование', value: 'equipment' },
  { label: 'Транспорт', value: 'transport' },
  { label: 'Ремонт', value: 'repair' },
  { label: 'Коммунальные расходы', value: 'utilities' },
  { label: 'Прочие расходы', value: 'other_expense' },
]

const getTodayDate = () => {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

const formatDateForInput = (value) => {
  if (!value) {
    return getTodayDate()
  }

  return new Date(value).toISOString().slice(0, 10)
}

const createInitialForm = (initialData = null) => ({
  operationType: initialData?.operation_type ?? null,
  category: initialData?.category ?? null,
  amount: initialData?.amount != null ? String(initialData.amount) : '',
  description: initialData?.description ?? '',
  date: formatDateForInput(initialData?.date),
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
    default: 'Добавить',
  },
  initialData: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['submit', 'cancel'])

const form = ref(createInitialForm())
const errors = ref({})

const filteredCategoryOptions = computed(() => {
  if (form.value.operationType === 'income') {
    return incomeCategoryOptions
  }

  if (form.value.operationType === 'expense') {
    return expenseCategoryOptions
  }

  return []
})

const resetForm = () => {
  form.value = createInitialForm(props.initialData)
  errors.value = {}
}

const validateForm = () => {
  const nextErrors = {}
  const amount = Number(form.value.amount)

  if (!form.value.operationType) {
    nextErrors.operationType = 'Выберите тип операции'
  }

  if (!form.value.category) {
    nextErrors.category = 'Выберите категорию'
  }

  if (!form.value.amount || Number.isNaN(amount) || amount <= 0) {
    nextErrors.amount = 'Введите сумму больше нуля'
  }

  if (!form.value.description.trim()) {
    nextErrors.description = 'Добавьте описание операции'
  }

  if (!form.value.date) {
    nextErrors.date = 'Укажите дату операции'
  }

  errors.value = nextErrors

  return Object.keys(nextErrors).length === 0
}

const handleSubmit = () => {
  if (!validateForm()) {
    return
  }

  emit('submit', {
    operation_type: form.value.operationType,
    category: form.value.category,
    amount: Number(form.value.amount),
    description: form.value.description.trim(),
    date: `${form.value.date}T00:00:00`,
    horse_id: null,
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

watch(
  () => props.initialData,
  () => {
    if (props.isOpen) {
      resetForm()
    }
  }
)

watch(
  () => form.value.operationType,
  (nextType) => {
    if (!form.value.category) {
      return
    }

    const allowedCategories = nextType === 'income'
      ? incomeCategoryOptions
      : nextType === 'expense'
        ? expenseCategoryOptions
        : []

    const isCurrentCategoryAllowed = allowedCategories.some((option) => option.value === form.value.category)

    if (!isCurrentCategoryAllowed) {
      form.value.category = null
    }
  }
)
</script>

<style module lang="scss" src="./FinanceOperationForm.module.scss"></style>
