<template>
  <AppFormDialog
    :model-value="modelValue"
    title="Добавить запись"
    subtitle="Заполните данные новой медицинской записи"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <MedicalRecordForm
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
import MedicalRecordForm from 'src/components/blocks/MedicalRecordForm/MedicalRecordForm.vue'

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
