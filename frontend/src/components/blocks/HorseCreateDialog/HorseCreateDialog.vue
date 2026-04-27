<template>
  <AppFormDialog
    :model-value="modelValue"
    title="Добавить лошадь"
    subtitle="Заполните информацию о новой лошади"
    @update:model-value="handleDialogToggle"
  >
    <q-form :class="$style.form" @submit.prevent="handleSubmit">
      <div :class="$style.fieldsRow">
        <AppFormField label="Кличка">
          <AppTextField
            v-model="form.name"
            hide-bottom-space
            :class="$style.control"
            placeholder="Введите кличку"
            :error="Boolean(errors.name)"
            :error-message="errors.name"
          />
        </AppFormField>

        <AppFormField label="Порода">
          <AppTextField
            v-model="form.breed"
            hide-bottom-space
            :class="$style.control"
            placeholder="Введите породу"
            :error="Boolean(errors.breed)"
            :error-message="errors.breed"
          />
        </AppFormField>
      </div>

      <div :class="$style.fieldsRow">
        <AppFormField label="Возраст">
          <AppTextField
            v-model="form.age"
            hide-bottom-space
            :class="$style.control"
            type="number"
            min="0"
            max="50"
            placeholder="Возраст (лет)"
            :error="Boolean(errors.age)"
            :error-message="errors.age"
          />
        </AppFormField>

        <AppFormField label="Пол">
          <AppSelectField
            v-model="form.gender"
            hide-bottom-space
            :class="$style.control"
            :options="genderOptions"
            placeholder="Выберите пол"
            :error="Boolean(errors.gender)"
            :error-message="errors.gender"
          />
        </AppFormField>
      </div>

      <div :class="$style.fieldsRow">
        <AppFormField label="Статус">
          <AppSelectField
            v-model="form.status"
            hide-bottom-space
            :class="$style.control"
            :options="statusOptions"
            placeholder="Выберите статус"
            :error="Boolean(errors.status)"
            :error-message="errors.status"
          />
        </AppFormField>

        <AppFormField label="Куратор">
          <AppSelectField
            v-model="form.curatorId"
            hide-bottom-space
            :class="$style.control"
            :options="filteredCuratorOptions"
            placeholder="Выберите куратора"
            clearable
            use-input
            fill-input
            hide-selected
            input-debounce="0"
            @filter="filterCurators"
          />
        </AppFormField>
      </div>

      <div :class="$style.fieldsRow">
        <AppFormField label="Масть">
          <AppTextField
            v-model="form.color"
            hide-bottom-space
            :class="$style.control"
            placeholder="Введите масть"
            :error="Boolean(errors.color)"
            :error-message="errors.color"
          />
        </AppFormField>

        <AppFormField label="Фото">
          <AppFileField
            v-model="form.photo"
            hide-bottom-space
            :class="$style.control"
            accept="image/*"
            clearable
            label="Выберите изображение"
            :error="Boolean(errors.photo)"
            :error-message="errors.photo"
          />
        </AppFormField>
      </div>

      <AppFormField label="Описание">
        <AppTextField
          v-model="form.description"
          hide-bottom-space
          :class="[$style.control, $style.controlTextarea]"
          type="textarea"
          autogrow
          placeholder="Краткое описание"
          :error="Boolean(errors.description)"
          :error-message="errors.description"
        />
      </AppFormField>

      <AppFormField label="История">
        <AppTextField
          v-model="form.history"
          hide-bottom-space
          :class="[$style.control, $style.controlTextarea]"
          type="textarea"
          autogrow
          placeholder="История лошади"
          :error="Boolean(errors.history)"
          :error-message="errors.history"
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
          @click="closeDialog"
        />
        <AppButton
          color="primary"
          unelevated
          no-caps
          label="Добавить"
          type="submit"
          :class="$style.primaryButton"
          :loading="submitting"
          :disable="submitting"
        />
      </AppFormActions>
    </q-form>
  </AppFormDialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import AppFormActions from 'src/components/blocks/AppFormActions/AppFormActions.vue'
import AppFormDialog from 'src/components/blocks/AppFormDialog/AppFormDialog.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppFileField from 'src/components/ui/AppFileField/AppFileField.vue'
import AppFormField from 'src/components/ui/AppFormField/AppFormField.vue'
import AppSelectField from 'src/components/ui/AppSelectField/AppSelectField.vue'
import AppTextField from 'src/components/ui/AppTextField/AppTextField.vue'

const genderOptions = [
  { label: 'Женский', value: 'female' },
  { label: 'Мужской', value: 'male' },
]

const statusOptions = [
  { label: 'Здоров', value: 'healthy' },
  { label: 'Болен', value: 'sick' },
  { label: 'Реабилитация', value: 'rehabilitation' },
  { label: 'Выбыл', value: 'deceased' },
]

const createInitialForm = () => ({
  name: '',
  breed: '',
  age: '',
  gender: null,
  status: 'healthy',
  color: '',
  curatorId: null,
  description: '',
  history: '',
  photo: null,
})

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  curatorOptions: {
    type: Array,
    default: () => [],
  },
  submitting: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'submit'])

const form = ref(createInitialForm())
const errors = ref({})
const filteredCuratorOptions = ref([])

const resetForm = () => {
  form.value = createInitialForm()
  errors.value = {}
  filteredCuratorOptions.value = [...props.curatorOptions]
}

const closeDialog = () => {
  emit('update:modelValue', false)
}

const handleDialogToggle = (value) => {
  emit('update:modelValue', value)
}

const filterCurators = (value, update) => {
  update(() => {
    const search = value.trim().toLowerCase()

    filteredCuratorOptions.value = search
      ? props.curatorOptions.filter((option) =>
          option.label.toLowerCase().includes(search)
        )
      : [...props.curatorOptions]
  })
}

const validateForm = () => {
  const nextErrors = {}

  if (!form.value.name.trim()) nextErrors.name = 'Укажите кличку'
  if (!form.value.breed.trim()) nextErrors.breed = 'Укажите породу'

  const age = Number(form.value.age)
  if (form.value.age === '' || Number.isNaN(age)) {
    nextErrors.age = 'Укажите возраст'
  } else if (age < 0 || age > 50) {
    nextErrors.age = 'Возраст должен быть от 0 до 50'
  }

  if (!form.value.gender) nextErrors.gender = 'Выберите пол'
  if (!form.value.status) nextErrors.status = 'Выберите статус'
  if (!form.value.color.trim()) nextErrors.color = 'Укажите масть'
  if (!form.value.description.trim()) nextErrors.description = 'Добавьте описание'
  if (!form.value.history.trim()) nextErrors.history = 'Добавьте историю'
  if (!form.value.photo) nextErrors.photo = 'Загрузите фотографию'

  errors.value = nextErrors

  return Object.keys(nextErrors).length === 0
}

const handleSubmit = () => {
  if (!validateForm()) {
    return
  }

  emit('submit', {
    name: form.value.name.trim(),
    breed: form.value.breed.trim(),
    age: Number(form.value.age),
    gender: form.value.gender,
    status: form.value.status,
    color: form.value.color.trim(),
    curator_id: form.value.curatorId,
    description: form.value.description.trim(),
    history: form.value.history.trim(),
    photo: form.value.photo,
  })
}

watch(
  () => props.curatorOptions,
  (options) => {
    filteredCuratorOptions.value = [...options]
  },
  { immediate: true }
)

watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      filteredCuratorOptions.value = [...props.curatorOptions]
      errors.value = {}
      return
    }

    resetForm()
  }
)
</script>

<style module lang="scss" src="./HorseCreateDialog.module.scss"></style>
