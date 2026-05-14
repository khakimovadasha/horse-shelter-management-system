<template>
  <AppFormDialog
    :model-value="modelValue"
    title="Изменить роль пользователя"
    subtitle="Выберите новую роль для пользователя"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <UserRoleForm
      :is-open="modelValue"
      :model-value="initialRole"
      :submitting="submitting"
      @cancel="$emit('update:modelValue', false)"
      @submit="$emit('submit', $event)"
    />
  </AppFormDialog>
</template>

<script setup>
import AppFormDialog from 'src/components/blocks/AppFormDialog/AppFormDialog.vue'
import UserRoleForm from 'src/components/blocks/UserRoleForm/UserRoleForm.vue'

defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  initialRole: {
    type: String,
    default: null,
  },
  submitting: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['update:modelValue', 'submit'])
</script>
