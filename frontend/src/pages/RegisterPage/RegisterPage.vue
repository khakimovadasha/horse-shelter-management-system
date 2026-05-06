<template>
  <q-page :class="$style.page">
    <AuthCard
      title="Регистрация в системе"
      subtitle="Создайте аккаунт для работы с системой управления приютом"
    >
      <AuthForm @submit="handleSubmit">
        <div :class="$style.fieldsRow">
          <AuthField
            v-model="form.first_name"
            label="Имя"
            placeholder="Введите имя"
          />

          <AuthField
            v-model="form.last_name"
            label="Фамилия"
            placeholder="Введите фамилию"
          />
        </div>

        <div :class="$style.fieldsRow">
          <AuthField
            v-model="form.username"
            label="Имя пользователя"
            placeholder="Введите логин"
          />

          <AuthField
            v-model="form.phone"
            label="Телефон"
            placeholder="+7 (___) ___-__-__"
            mask="+7 (###) ###-##-##"
          />
        </div>

        <AuthField
          v-model="form.email"
          label="Email"
          placeholder="user@shelter.ru"
        />

        <AuthField
          v-model="form.password"
          label="Пароль"
          placeholder="Введите пароль"
          type="password"
          password-toggle
        />

        <p v-if="errorMessage" :class="$style.error">
          {{ errorMessage }}
        </p>

        <AuthSubmitButton
          label="Зарегистрироваться"
          :loading="isSubmitting"
        />
      </AuthForm>

      <template #footer>
        <AuthFooter
          text="Уже есть аккаунт?"
          link-label="Войти"
          to="/login"
        />
      </template>
    </AuthCard>
  </q-page>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCurrentUserStore } from 'src/stores/currentUser'
import AuthCard from 'src/components/blocks/AuthCard/AuthCard.vue'
import AuthFooter from 'src/components/blocks/AuthFooter/AuthFooter.vue'
import AuthForm from 'src/components/blocks/AuthForm/AuthForm.vue'
import AuthField from 'src/components/ui/AuthField/AuthField.vue'
import AuthSubmitButton from 'src/components/ui/AuthSubmitButton/AuthSubmitButton.vue'
import { loginUser, registerUser, setAccessToken } from 'src/api/auth'

const router = useRouter()
const currentUserStore = useCurrentUserStore()

const isSubmitting = ref(false)
const errorMessage = ref('')

const form = reactive({
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  phone: '',
})

const handleSubmit = async () => {
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    await registerUser({
      email: form.email,
      username: form.username || null,
      password: form.password,
      first_name: form.first_name,
      last_name: form.last_name,
      phone: form.phone || null,
    })

    const loginData = await loginUser({
      email: form.email,
      password: form.password,
    })

    setAccessToken(loginData.access_token)
    currentUserStore.clearCurrentUser()
    await currentUserStore.fetchCurrentUser(true)
    await router.push('/app')
  } catch (error) {
    errorMessage.value =
      error?.response?.data?.detail || 'Не удалось выполнить регистрацию'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style module lang="scss" src="./RegisterPage.module.scss"></style>
