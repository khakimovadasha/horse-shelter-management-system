<template>
  <AppFormDialog
    :model-value="modelValue"
    title="Новая операция"
    subtitle="Добавьте доход или расход"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <FinanceOperationForm
      :is-open="modelValue"
      :submitting="submitting"
      submit-label="Добавить"
      @cancel="$emit('update:modelValue', false)"
      @submit="$emit('submit', $event)"
    />
  </AppFormDialog>
</template>

<script setup>
import AppFormDialog from 'src/components/blocks/AppFormDialog/AppFormDialog.vue'
import FinanceOperationForm from 'src/components/blocks/FinanceOperationForm/FinanceOperationForm.vue'

defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  submitting: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['update:modelValue', 'submit'])
</script>
