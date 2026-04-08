<template>
  <div class="app-info-item">
    <div class="app-info-item__label">{{ label }}</div>
    <div class="app-info-item__value">{{ value }}</div>
  </div>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: String,
    default: '',
  },
})
</script>

<style scoped>
.app-info-item__label {
  margin-bottom: 4px;
  color: #7a869a;
  font-size: 13px;
  font-weight: 600;
}

.app-info-item__value {
  color: #233044;
  font-size: 15px;
  line-height: 1.5;
}
</style>
