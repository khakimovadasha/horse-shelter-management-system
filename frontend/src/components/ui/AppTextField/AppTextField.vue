<template>
  <div :class="$style.root">
    <q-input
      v-bind="$attrs"
      :class="$style.field"
      outlined
      dense
      :maxlength="maxLength || undefined"
      :model-value="modelValue"
      :error="displayError"
      :error-message="error ? errorMessage : ''"
      @update:model-value="handleUpdate"
    >
      <template
        v-for="(_, slotName) in $slots"
        #[slotName]="slotProps"
        :key="slotName"
      >
        <slot :name="slotName" v-bind="slotProps || {}" />
      </template>
    </q-input>

    <div v-if="metaText" :class="[$style.meta, metaIsAlert && $style.metaAlert]">
      {{ metaText }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

defineOptions({
  inheritAttrs: false,
})

const props = defineProps({
  modelValue: {
    type: [String, Number, null],
    default: '',
  },
  error: {
    type: Boolean,
    default: false,
  },
  errorMessage: {
    type: String,
    default: '',
  },
  maxLength: {
    type: Number,
    default: null,
  },
  showCounter: {
    type: Boolean,
    default: false,
  },
  showLimitWarning: {
    type: Boolean,
    default: false,
  },
  limitReachedMessage: {
    type: String,
    default: 'Достигнут лимит символов',
  },
})

const emit = defineEmits(['update:modelValue'])

const currentLength = computed(() => String(props.modelValue ?? '').length)
const limitReached = computed(() => {
  return Boolean(props.maxLength) && currentLength.value >= props.maxLength
})

const displayError = computed(() => props.error || limitReached.value)

const metaText = computed(() => {
  if (props.error && props.errorMessage) {
    return props.errorMessage
  }

  if (props.showLimitWarning && limitReached.value) {
    return props.limitReachedMessage
  }

  if (props.showCounter && props.maxLength) {
    return `${currentLength.value}/${props.maxLength}`
  }

  return ''
})

const metaIsAlert = computed(() => {
  return props.error || limitReached.value
})

const handleUpdate = (value) => {
  if (typeof value === 'string' && props.maxLength) {
    emit('update:modelValue', value.slice(0, props.maxLength))
    return
  }

  emit('update:modelValue', value)
}
</script>

<style module lang="scss" src="./AppTextField.module.scss"></style>
