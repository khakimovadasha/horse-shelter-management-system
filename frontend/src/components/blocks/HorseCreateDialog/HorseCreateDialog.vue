<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="handleDialogToggle"
  >
    <q-card :class="$style.dialog">
      <div :class="$style.header">
        <div>
          <div :class="$style.title">Добавить лошадь</div>
          <div :class="$style.subtitle">Заполните информацию о новой лошади</div>
        </div>

        <q-btn
          flat
          round
          dense
          icon="close"
          aria-label="Закрыть"
          @click="closeDialog"
        />
      </div>

      <q-form :class="$style.form" @submit.prevent="handleSubmit">
        <div :class="$style.gridMain">
          <div :class="$style.field">
            <label :class="$style.label">Кличка</label>
            <AppTextField
              v-model="form.name"
              :class="$style.control"
              placeholder="Введите кличку"
              :error="Boolean(errors.name)"
              :error-message="errors.name"
            />
          </div>

          <div :class="$style.field">
            <label :class="$style.label">Порода</label>
            <AppTextField
              v-model="form.breed"
              :class="$style.control"
              placeholder="Введите породу"
              :error="Boolean(errors.breed)"
              :error-message="errors.breed"
            />
          </div>

          <div :class="$style.field">
            <label :class="$style.label">Возраст</label>
            <AppTextField
              v-model="form.age"
              :class="$style.control"
              type="number"
              min="0"
              max="50"
              placeholder="Возраст (лет)"
              :error="Boolean(errors.age)"
              :error-message="errors.age"
            />
          </div>

          <div :class="$style.field">
            <label :class="$style.label">Пол</label>
            <AppSelectField
              v-model="form.gender"
              :class="$style.control"
              :options="genderOptions"
              placeholder="Выберите пол"
              :error="Boolean(errors.gender)"
              :error-message="errors.gender"
            />
          </div>

          <div :class="$style.field">
            <label :class="$style.label">Статус</label>
            <AppSelectField
              v-model="form.status"
              :class="$style.control"
              :options="statusOptions"
              placeholder="Выберите статус"
              :error="Boolean(errors.status)"
              :error-message="errors.status"
            />
          </div>

          <div :class="$style.field">
            <label :class="$style.label">Куратор</label>
            <AppSelectField
              v-model="form.curatorId"
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
          </div>
        </div>

        <div :class="$style.gridTwo">
          <div :class="$style.field">
            <label :class="$style.label">Масть</label>
            <AppTextField
              v-model="form.color"
              :class="$style.control"
              placeholder="Введите масть"
              :error="Boolean(errors.color)"
              :error-message="errors.color"
            />
          </div>

          <div :class="$style.field">
            <label :class="$style.label">Фото</label>
            <AppFileField
              v-model="form.photo"
              :class="$style.control"
              accept="image/*"
              clearable
              :error="Boolean(errors.photo)"
              :error-message="errors.photo"
              label="Выберите изображение"
            />
          </div>

          <div :class="$style.field">
            <label :class="$style.label">Описание</label>
            <AppTextField
              v-model="form.description"
              :class="[$style.control, $style.controlTextarea]"
              type="textarea"
              autogrow
              placeholder="Краткое описание"
            :error="Boolean(errors.description)"
              :error-message="errors.description"
            />
          </div>

          <div :class="$style.field">
            <label :class="$style.label">История</label>
            <AppTextField
              v-model="form.history"
              :class="[$style.control, $style.controlTextarea]"
              type="textarea"
              autogrow
              placeholder="История лошади"
            :error="Boolean(errors.history)"
              :error-message="errors.history"
            />
          </div>
        </div>

        <div :class="$style.actions">
          <AppButton
            outline
            no-caps
            label="Отмена"
            type="button"
            :disable="submitting"
            @click="closeDialog"
          />
          <AppButton
            color="primary"
            unelevated
            no-caps
            label="Добавить"
            type="submit"
            :loading="submitting"
            :disable="submitting"
          />
        </div>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppFileField from 'src/components/ui/AppFileField/AppFileField.vue'
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
