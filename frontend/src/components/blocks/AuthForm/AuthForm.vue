<template>
  <form :class="$style.form" @submit.prevent="$emit('submit')">
    <slot />
  </form>
</template>

<script setup>
defineEmits(['submit'])
</script>

<style module lang="scss" src="./AuthForm.module.scss"></style>
