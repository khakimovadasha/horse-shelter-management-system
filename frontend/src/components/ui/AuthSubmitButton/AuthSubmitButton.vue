<template>
  <AppButton
    type="submit"
    :label="label"
    :loading="loading"
    unelevated
    no-caps
    :class="$style.button"
  />
</template>

<script setup>
import AppButton from 'src/components/ui/AppButton/AppButton.vue'

defineProps({
  label: {
    type: String,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})
</script>

<style module lang="scss" src="./AuthSubmitButton.module.scss"></style>
