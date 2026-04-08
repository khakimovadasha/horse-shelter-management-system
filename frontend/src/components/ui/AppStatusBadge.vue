<template>
  <div class="app-status-badge" :class="badgeClass">
    {{ label }}
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  tone: {
    type: String,
    default: 'default',
  },
})

const badgeClass = computed(() => `app-status-badge--${props.tone}`)
</script>

<style scoped>
.app-status-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 32px;
  padding: 0 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  line-height: 1;
}

.app-status-badge--healthy {
  background: rgba(46, 125, 50, 0.14);
  color: #2e7d32;
}

.app-status-badge--sick {
  background: rgba(198, 40, 40, 0.14);
  color: #c62828;
}

.app-status-badge--rehabilitation {
  background: rgba(239, 108, 0, 0.14);
  color: #ef6c00;
}

.app-status-badge--deceased {
  background: rgba(84, 110, 122, 0.16);
  color: #455a64;
}

.app-status-badge--default {
  background: rgba(96, 125, 139, 0.12);
  color: #546e7a;
}
</style>
