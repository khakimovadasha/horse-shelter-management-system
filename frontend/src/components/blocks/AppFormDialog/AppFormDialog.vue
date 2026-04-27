<template>
  <q-dialog
    :class="$style.dialog"
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <div :class="$style.card">
      <div :class="$style.header">
        <div>
          <div :class="$style.title">{{ title }}</div>
          <div v-if="subtitle" :class="$style.subtitle">{{ subtitle }}</div>
        </div>

        <q-btn
          flat
          round
          dense
          icon="close"
          aria-label="Закрыть"
          @click="$emit('update:modelValue', false)"
        />
      </div>

      <div :class="$style.body">
        <slot />
      </div>
    </div>
  </q-dialog>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
})

defineEmits(['update:modelValue'])
</script>

<style module lang="scss" src="./AppFormDialog.module.scss"></style>
