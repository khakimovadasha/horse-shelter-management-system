<template>
  <AppButton
    color="white"
    text-color="dark"
    outline
    no-caps
    :label="label"
    :class="$style.button"
    v-bind="$attrs"
  />
</template>

<script setup>
import AppButton from 'src/components/ui/AppButton/AppButton.vue'

defineOptions({
  inheritAttrs: false,
})

defineProps({
  label: {
    type: String,
    required: true,
  },
})
</script>

<style module lang="scss" src="./AppTableAction.module.scss"></style>
