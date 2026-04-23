<template>
  <q-btn
    v-bind="$attrs"
    :color="color"
    :label="label"
    :icon="icon || undefined"
    :outline="outline"
    :unelevated="unelevated"
    :no-caps="noCaps"
    :dense="dense"
  />
</template>

<script setup>
defineOptions({
  inheritAttrs: false,
})

defineProps({
  color: {
    type: String,
    default: 'primary',
  },
  label: {
    type: String,
    default: '',
  },
  icon: {
    type: String,
    default: '',
  },
  outline: {
    type: Boolean,
    default: false,
  },
  unelevated: {
    type: Boolean,
    default: false,
  },
  noCaps: {
    type: Boolean,
    default: true,
  },
  dense: {
    type: Boolean,
    default: false,
  },
})
</script>

<style module lang="scss" src="./AppButton.module.scss"></style>
