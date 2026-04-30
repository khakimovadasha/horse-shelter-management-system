<template>
  <AppFormDialog
    :model-value="modelValue"
    title="Добавить процедуру"
    subtitle="Заполните данные новой медицинской процедуры"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <ProcedureForm
      :is-open="modelValue"
      :horse-options="horseOptions"
      :submitting="submitting"
      submit-label="Добавить"
      @cancel="$emit('update:modelValue', false)"
      @submit="$emit('submit', $event)"
    />
  </AppFormDialog>
</template>

<script setup>
import AppFormDialog from 'src/components/blocks/AppFormDialog/AppFormDialog.vue'
import ProcedureForm from 'src/components/blocks/ProcedureForm/ProcedureForm.vue'

defineProps({
  modelValue: {
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
})

defineEmits(['update:modelValue', 'submit'])
</script>
