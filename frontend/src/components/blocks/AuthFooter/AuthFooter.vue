<template>
  <p :class="$style.footerText">
    {{ text }}
    <RouterLink :to="to" :class="$style.footerLink">
      {{ linkLabel }}
    </RouterLink>
  </p>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    required: true,
  },
  linkLabel: {
    type: String,
    required: true,
  },
  to: {
    type: String,
    required: true,
  },
})
</script>

<style module lang="scss" src="./AuthFooter.module.scss"></style>
