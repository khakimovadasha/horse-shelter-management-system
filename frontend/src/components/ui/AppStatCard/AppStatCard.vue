<template>
  <article :class="$style.card">
    <h3 :class="$style.title">{{ title }}</h3>

    <div :class="$style.content">
      <div>
        <div :class="[$style.value, valueToneClass]">{{ value }}</div>
        <p v-if="subtitle" :class="$style.subtitle">{{ subtitle }}</p>
      </div>

      <div :class="[$style.iconBox, iconToneClass]">
        <q-icon :name="icon" :class="$style.icon" />
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed, useCssModule } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
  icon: {
    type: String,
    required: true,
  },
  tone: {
    type: String,
    default: 'neutral',
  },
  valueTone: {
    type: String,
    default: 'default',
  },
})

const $style = useCssModule()

const iconToneClass = computed(() => {
  switch (props.tone) {
    case 'success':
      return $style.iconBoxSuccess
    case 'danger':
      return $style.iconBoxDanger
    case 'info':
      return $style.iconBoxInfo
    default:
      return $style.iconBoxNeutral
  }
})

const valueToneClass = computed(() => {
  switch (props.valueTone) {
    case 'success':
      return $style.valueSuccess
    case 'danger':
      return $style.valueDanger
    default:
      return $style.valueDefault
  }
})
</script>

<style module lang="scss" src="./AppStatCard.module.scss"></style>
