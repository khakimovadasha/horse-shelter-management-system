import { defineBoot } from '#q-app/wrappers'
import axios from 'axios'
import { clearAuthSession, getAccessToken } from 'src/api/auth'
import { useCurrentUserStore } from 'src/stores/currentUser'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const api = axios.create({ baseURL: `${API_BASE_URL}/api` })

export default defineBoot(({ app, router }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API

  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status === 401 && getAccessToken()) {
        const currentUserStore = useCurrentUserStore()
        clearAuthSession(currentUserStore)

        const currentRoute = router.currentRoute.value
        if (currentRoute.path.startsWith('/app')) {
          await router.replace('/login')
        }
      }

      return Promise.reject(error)
    }
  )
})

export { api }
