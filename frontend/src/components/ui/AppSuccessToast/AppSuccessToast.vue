<template>
  <div :class="$style.root">
    <q-icon
      name="check_circle"
      size="24px"
      :class="$style.icon"
    />
    <div :class="$style.message">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    required: true,
  },
})
</script>

<style module lang="scss" src="./AppSuccessToast.module.scss"></style>
