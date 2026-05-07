<template>
  <AppFormDialog
    :model-value="modelValue"
    title="Создать задачу"
    subtitle="Заполните данные новой задачи"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <TaskForm
      :is-open="modelValue"
      :horse-options="horseOptions"
      :submitting="submitting"
      submit-label="Создать"
      @cancel="$emit('update:modelValue', false)"
      @submit="$emit('submit', $event)"
    />
  </AppFormDialog>
</template>

<script setup>
import AppFormDialog from 'src/components/blocks/AppFormDialog/AppFormDialog.vue'
import TaskForm from 'src/components/blocks/TaskForm/TaskForm.vue'

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
