<template>
  <q-layout view="hHh lpR fFf">
    <q-header :class="$style.header">
      <q-toolbar :class="$style.toolbar">
        <div :class="$style.headerLeft">
          <q-btn
            v-if="$q.screen.lt.lg"
            flat
            round
            dense
            icon="menu"
            :class="$style.burger"
            aria-label="Открыть меню"
            @click="leftDrawerOpen = !leftDrawerOpen"
          />

          <RouterLink to="/" :class="$style.logo">
            <div :class="$style.logoMark">
              <q-icon name="favorite" size="24px" />
            </div>

            <div :class="$style.logoText">
              <div>Приют для</div>
              <div>лошадей</div>
            </div>
          </RouterLink>
        </div>

        <nav v-if="$q.screen.gt.md" :class="$style.nav">
          <RouterLink
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            :class="[$style.navLink, { [$style.navLinkActive]: isActive(item.to) }]"
          >
            <q-icon :name="item.icon" size="20px" />
            <span>{{ item.label }}</span>
          </RouterLink>
        </nav>

        <div v-if="$q.screen.gt.sm" :class="$style.user">
          <q-avatar :class="$style.userAvatar" size="42px">
            {{ userInitials }}
          </q-avatar>
          <div :class="$style.userName">{{ userDisplayName }}</div>
          <q-btn
            flat
            round
            dense
            icon="logout"
            :class="$style.logoutButton"
            aria-label="Выйти"
            @click="handleLogout"
          />
        </div>

        <div v-else :class="$style.userCompact">
          <q-avatar :class="$style.userAvatar" size="38px">
            {{ userInitials }}
          </q-avatar>
          <q-btn
            flat
            round
            dense
            icon="logout"
            :class="$style.logoutButton"
            aria-label="Выйти"
            @click="handleLogout"
          />
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      side="left"
      overlay
      bordered
      :width="290"
      :class="$style.drawer"
    >
      <div :class="$style.drawerContent">
        <div :class="$style.drawerTop">
          <RouterLink to="/" :class="$style.logo" @click="closeDrawer">
            <div :class="$style.logoMark">
              <q-icon name="favorite" size="24px" />
            </div>

            <div :class="$style.logoText">
              <div>Приют для</div>
              <div>лошадей</div>
            </div>
          </RouterLink>

          <q-btn
            flat
            round
            dense
            icon="close"
            aria-label="Закрыть меню"
            @click="leftDrawerOpen = false"
          />
        </div>

        <q-list :class="$style.drawerNav">
          <q-item
            v-for="item in navItems"
            :key="item.to"
            clickable
            :to="item.to"
            :class="[$style.drawerItem, { [$style.drawerItemActive]: isActive(item.to) }]"
            @click="closeDrawer"
          >
            <q-item-section avatar>
              <q-icon :name="item.icon" size="20px" />
            </q-item-section>

            <q-item-section>
              {{ item.label }}
            </q-item-section>
          </q-item>
        </q-list>

        <div :class="$style.drawerUser">
          <q-avatar :class="$style.userAvatar" size="42px">
            {{ userInitials }}
          </q-avatar>
          <div>
            <div :class="$style.drawerUserName">{{ userDisplayName }}</div>
          </div>
          <q-btn
            flat
            round
            dense
            icon="logout"
            :class="$style.drawerLogoutButton"
            aria-label="Выйти"
            @click="handleLogout"
          />
        </div>
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { getAccessToken, removeAccessToken } from 'src/api/auth'
import { useCurrentUserStore } from 'src/stores/currentUser'

const route = useRoute()
const router = useRouter()
const $q = useQuasar()
const currentUserStore = useCurrentUserStore()

const leftDrawerOpen = ref(false)

const userDisplayName = computed(() => {
  const firstName = currentUserStore.user?.first_name?.trim() || ''
  const lastName = currentUserStore.user?.last_name?.trim() || ''
  const fullName = `${firstName} ${lastName}`.trim()

  return fullName || 'Пользователь'
})

const userInitials = computed(() => {
  const firstInitial = currentUserStore.user?.first_name?.trim()?.[0] || ''
  const lastInitial = currentUserStore.user?.last_name?.trim()?.[0] || ''
  const initials = `${firstInitial}${lastInitial}`.toUpperCase()

  return initials || 'П'
})

const navItems = [
  { label: 'Главная', to: '/app', icon: 'home' },
  { label: 'Лошади', to: '/app/horses', icon: 'favorite_border' },
  { label: 'Процедуры', to: '/app/procedures', icon: 'monitor_heart' },
  { label: 'Задачи', to: '/app/tasks', icon: 'task_alt' },
  // { label: 'Календарь', to: '/app/calendar', icon: 'calendar_month' },
  { label: 'Финансы', to: '/app/finances', icon: 'attach_money' },
  { label: 'Отчёты', to: '/app/reports', icon: 'description' },
  // { label: 'Пользователи', to: '/users', icon: 'group' },
]

const isActive = (path) => {
  if (path === '/app') {
    return route.path === '/app'
  }

  return route.path.startsWith(path)
}

const closeDrawer = () => {
  if ($q.screen.lt.lg) {
    leftDrawerOpen.value = false
  }
}

const handleLogout = async () => {
  removeAccessToken()
  currentUserStore.clearCurrentUser()
  leftDrawerOpen.value = false
  await router.push('/login')
}

onMounted(() => {
  if (!getAccessToken()) {
    return
  }

  currentUserStore.fetchCurrentUser().catch(() => {})
})
</script>

<style module lang="scss" src="./MainLayout.module.scss"></style>
