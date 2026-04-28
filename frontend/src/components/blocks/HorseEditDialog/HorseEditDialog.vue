<template>
  <AppFormDialog
    :model-value="modelValue"
    title="Редактировать лошадь"
    subtitle="Измените информацию о лошади"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <HorseForm
      :is-open="modelValue"
      :horse="horse"
      :curator-options="curatorOptions"
      :submitting="submitting"
      submit-label="Сохранить"
      photo-label="Выберите новое изображение"
      show-arrival-date
      @cancel="$emit('update:modelValue', false)"
      @submit="$emit('submit', $event)"
    />
  </AppFormDialog>
</template>

<script setup>
import AppFormDialog from 'src/components/blocks/AppFormDialog/AppFormDialog.vue'
import HorseForm from 'src/components/blocks/HorseForm/HorseForm.vue'

defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  horse: {
    type: Object,
    default: null,
  },
  curatorOptions: {
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
