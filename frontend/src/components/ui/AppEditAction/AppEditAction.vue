<template>
  <AppButton
    color="white"
    text-color="primary"
    outline
    no-caps
    icon="edit"
    label=""
    :dense="dense"
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
  dense: {
    type: Boolean,
    default: false,
  },
})
</script>

<style module lang="scss" src="./AppEditAction.module.scss"></style>
