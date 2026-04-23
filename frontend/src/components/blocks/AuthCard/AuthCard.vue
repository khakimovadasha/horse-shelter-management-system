<template>
  <section :class="$style.wrapper">
    <div :class="$style.overlay"></div>

    <div :class="$style.card">
      <div :class="$style.logoMark">
        <q-icon name="favorite" size="32px" />
      </div>

      <h1 :class="$style.title">{{ title }}</h1>
      <p :class="$style.subtitle">{{ subtitle }}</p>

      <slot />

      <div :class="$style.footer">
        <slot name="footer" />
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    required: true,
  },
})
</script>

<style module lang="scss" src="./AuthCard.module.scss"></style>
