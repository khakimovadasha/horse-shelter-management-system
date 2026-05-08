<template>
  <q-card :class="[$style.root, 'app-card']">
    <div :class="$style.list">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        type="button"
        :class="[$style.item, modelValue === tab.value && $style.itemActive]"
        @click="$emit('update:modelValue', tab.value)"
      >
        {{ tab.label }}
      </button>
    </div>
  </q-card>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: 'medical',
  },
})

defineEmits(['update:modelValue'])

const tabs = [
  { value: 'medical', label: 'Медицинская карта' },
  { value: 'procedures', label: 'Процедуры' },
  { value: 'tasks', label: 'Задачи' },
  { value: 'documents', label: 'Документы' },
]
</script>

<style module lang="scss" src="./HorseDetailTabs.module.scss"></style>
