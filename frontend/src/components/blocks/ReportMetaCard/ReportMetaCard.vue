<template>
  <div :class="$style.card">
    <div :class="$style.title">{{ title }}</div>

    <div :class="$style.list">
      <div
        v-for="entry in entries"
        :key="entry.label"
        :class="$style.row"
      >
        <span>{{ entry.label }}</span>
        <strong>{{ entry.value }}</strong>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  entries: {
    type: Array,
    default: () => [],
  },
})
</script>

<style module lang="scss" src="./ReportMetaCard.module.scss"></style>
