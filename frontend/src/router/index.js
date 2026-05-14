import { defineRouter } from '#q-app/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import { clearAuthSession, getAccessToken } from 'src/api/auth'
import { useCurrentUserStore } from 'src/stores/currentUser'
import { canViewFinances } from 'src/utils/permissions'
import routes from './routes'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default defineRouter(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  Router.beforeEach(async (to) => {
    const isPrivateRoute = to.path.startsWith('/app')
    const isAuthRoute = to.name === 'login' || to.name === 'register'
    const hasToken = Boolean(getAccessToken())
    const currentUserStore = useCurrentUserStore()

    if (isPrivateRoute && !hasToken) {
      clearAuthSession(currentUserStore)
      return { name: 'login' }
    }

    if (isPrivateRoute && hasToken) {
      try {
        if (!currentUserStore.loaded || !currentUserStore.user) {
          await currentUserStore.fetchCurrentUser(true)
        }
      } catch {
        clearAuthSession(currentUserStore)
        return { name: 'login' }
      }
    }

    if (isAuthRoute && hasToken) {
      try {
        if (!currentUserStore.loaded || !currentUserStore.user) {
          await currentUserStore.fetchCurrentUser(true)
        }
        return { name: 'dashboard' }
      } catch {
        clearAuthSession(currentUserStore)
        return true
      }
    }

    if (to.meta.requiresAdmin && hasToken) {
      if (!canViewFinances(currentUserStore.user)) {
        return { name: 'dashboard' }
      }
    }

    return true
  })

  return Router
})
