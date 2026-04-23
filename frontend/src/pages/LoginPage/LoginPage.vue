<template>
  <q-page :class="$style.page">
    <AuthCard
      title="Система управления приютом"
      subtitle="Войдите в систему для продолжения"
    >
      <AuthForm @submit="handleSubmit">
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
          label="Войти"
          :loading="isSubmitting"
        />
      </AuthForm>

      <template #footer>
        <AuthFooter
          text="Ещё нет аккаунта?"
          link-label="Зарегистрироваться"
          to="/register"
        />
      </template>
    </AuthCard>
  </q-page>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthCard from 'src/components/blocks/AuthCard/AuthCard.vue'
import AuthForm from 'src/components/blocks/AuthForm/AuthForm.vue'
import AuthFooter from 'src/components/blocks/AuthFooter/AuthFooter.vue'
import AuthField from 'src/components/ui/AuthField/AuthField.vue'
import AuthSubmitButton from 'src/components/ui/AuthSubmitButton/AuthSubmitButton.vue'
import { loginUser, setAccessToken } from 'src/api/auth'

const router = useRouter()

const isSubmitting = ref(false)
const errorMessage = ref('')

const form = reactive({
  email: '',
  password: '',
})

const handleSubmit = async () => {
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    const data = await loginUser({
      email: form.email,
      password: form.password,
    })

    setAccessToken(data.access_token)
    await router.push('/app')
  } catch (error) {
    errorMessage.value =
      error?.response?.data?.detail || 'Не удалось выполнить вход'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style module lang="scss" src="./LoginPage.module.scss"></style>
