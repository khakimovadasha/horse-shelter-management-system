<template>
  <q-form :class="$style.form" @submit.prevent="handleSubmit">
    <AppFormField label="Роль пользователя">
      <AppSelectField
        v-model="selectedRole"
        hide-bottom-space
        :class="$style.control"
        :options="roleOptions"
        placeholder="Выберите роль"
        :error="Boolean(errorMessage)"
        :error-message="errorMessage"
      />
    </AppFormField>

    <AppFormActions>
      <AppButton
        outline
        no-caps
        label="Отмена"
        type="button"
        :class="$style.secondaryButton"
        :disable="submitting"
        @click="$emit('cancel')"
      />
      <AppButton
        color="primary"
        unelevated
        no-caps
        label="Изменить"
        type="submit"
        :class="$style.primaryButton"
        :loading="submitting"
        :disable="submitting"
      />
    </AppFormActions>
  </q-form>
</template>

<script setup>
import { ref, watch } from 'vue'
import AppFormActions from 'src/components/blocks/AppFormActions/AppFormActions.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppFormField from 'src/components/ui/AppFormField/AppFormField.vue'
import AppSelectField from 'src/components/ui/AppSelectField/AppSelectField.vue'

const roleOptions = [
  { label: 'Администратор', value: 'admin' },
  { label: 'Ветеринар', value: 'veterinarian' },
  { label: 'Волонтёр', value: 'user' },
]

const props = defineProps({
  modelValue: {
    type: String,
    default: null,
  },
  submitting: {
    type: Boolean,
    default: false,
  },
  isOpen: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['cancel', 'submit'])

const selectedRole = ref(props.modelValue)
const errorMessage = ref('')

const resetForm = () => {
  selectedRole.value = props.modelValue
  errorMessage.value = ''
}

const handleSubmit = () => {
  if (!selectedRole.value) {
    errorMessage.value = 'Выберите роль пользователя'
    return
  }

  emit('submit', selectedRole.value)
}

watch(
  () => props.isOpen,
  (isOpen) => {
    if (isOpen) {
      resetForm()
    }
  },
  { immediate: true }
)

watch(
  () => props.modelValue,
  () => {
    if (props.isOpen) {
      resetForm()
    }
  }
)

watch(selectedRole, () => {
  errorMessage.value = ''
})
</script>

<style module lang="scss" src="./UserRoleForm.module.scss"></style>
