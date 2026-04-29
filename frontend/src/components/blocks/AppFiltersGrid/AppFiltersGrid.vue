<template>
  <div
    :class="$style.root"
    :style="{
      '--filters-grid-columns': desktopColumns,
      '--filters-grid-tablet-columns': tabletColumns,
    }"
  >
    <slot />
  </div>
</template>

<script setup>
defineProps({
  desktopColumns: {
    type: String,
    default: 'repeat(3, minmax(0, 1fr))',
  },
  tabletColumns: {
    type: String,
    default: 'repeat(2, minmax(0, 1fr))',
  },
})
</script>

<style module lang="scss" src="./AppFiltersGrid.module.scss"></style>
