<template>
  <AppFormDialog
    :model-value="modelValue"
    :title="title"
    :subtitle="subtitle"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <FinanceOperationForm
      :is-open="modelValue"
      :submitting="submitting"
      :submit-label="submitLabel"
      :initial-data="initialData"
      @cancel="$emit('update:modelValue', false)"
      @submit="$emit('submit', $event)"
    />
  </AppFormDialog>
</template>

<script setup>
import { computed } from 'vue'
import AppFormDialog from 'src/components/blocks/AppFormDialog/AppFormDialog.vue'
import FinanceOperationForm from 'src/components/blocks/FinanceOperationForm/FinanceOperationForm.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  submitting: {
    type: Boolean,
    default: false,
  },
  initialData: {
    type: Object,
    default: null,
  },
})

defineEmits(['update:modelValue', 'submit'])

const isEditMode = computed(() => Boolean(props.initialData?.id))
const title = computed(() => (isEditMode.value ? 'Редактировать операцию' : 'Новая операция'))
const subtitle = computed(() => (isEditMode.value ? 'Обновите данные финансовой операции' : 'Добавьте доход или расход'))
const submitLabel = computed(() => (isEditMode.value ? 'Сохранить' : 'Добавить'))
</script>
