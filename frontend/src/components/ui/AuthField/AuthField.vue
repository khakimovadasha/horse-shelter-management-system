<template>
  <div :class="$style.fieldGroup">
    <label v-if="label" :class="$style.label">
      {{ label }}
    </label>

    <AppTextField
      :model-value="modelValue"
      :type="currentType"
      :placeholder="placeholder"
      :mask="mask"
      outlined
      dense
      hide-bottom-space
      bg-color="white"
      :class="$style.input"
      @update:model-value="emit('update:modelValue', $event)"
    >
      <template v-if="passwordToggle" #append>
        <q-icon
          :name="isPasswordVisible ? 'visibility_off' : 'visibility'"
          :class="$style.eyeIcon"
          @click="togglePassword"
        />
      </template>
    </AppTextField>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import AppTextField from 'src/components/ui/AppTextField/AppTextField.vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'text',
  },
  mask: {
    type: String,
    default: '',
  },
  passwordToggle: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue'])

const isPasswordVisible = ref(false)

const currentType = computed(() => {
  if (!props.passwordToggle) {
    return props.type
  }

  return isPasswordVisible.value ? 'text' : 'password'
})

const togglePassword = () => {
  isPasswordVisible.value = !isPasswordVisible.value
}
</script>

<style module lang="scss" src="./AuthField.module.scss"></style>