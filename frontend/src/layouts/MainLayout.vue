<template>
  <q-layout view="hHh lpR fFf">
    <q-header class="app-header">
      <q-toolbar class="app-toolbar">
        <div class="app-header__left">
          <q-btn
            v-if="$q.screen.lt.lg"
            flat
            round
            dense
            icon="menu"
            class="app-burger"
            aria-label="Открыть меню"
            @click="leftDrawerOpen = !leftDrawerOpen"
          />

          <RouterLink to="/" class="app-logo">
            <div class="app-logo__mark">
              <q-icon name="favorite" size="24px" />
            </div>

            <div class="app-logo__text">
              <div>Приют для</div>
              <div>лошадей</div>
            </div>
          </RouterLink>
        </div>

        <nav v-if="$q.screen.gt.md" class="app-nav">
          <RouterLink
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            class="app-nav__link"
            :class="{ 'app-nav__link--active': isActive(item.to) }"
          >
            <q-icon :name="item.icon" size="20px" />
            <span>{{ item.label }}</span>
          </RouterLink>
        </nav>

        <div class="app-user" v-if="$q.screen.gt.sm">
          <q-avatar class="app-user__avatar" size="42px">
            АП
          </q-avatar>
          <div class="app-user__name">Анна Петрова</div>
        </div>

        <q-avatar v-else class="app-user__avatar" size="38px">
          АП
        </q-avatar>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      side="left"
      overlay
      bordered
      :width="290"
      class="app-drawer"
    >
      <div class="app-drawer__content">
        <div class="app-drawer__top">
          <RouterLink to="/" class="app-logo" @click="closeDrawer">
            <div class="app-logo__mark">
              <q-icon name="favorite" size="24px" />
            </div>

            <div class="app-logo__text">
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

        <q-list class="app-drawer__nav">
          <q-item
            v-for="item in navItems"
            :key="item.to"
            clickable
            :to="item.to"
            class="app-drawer__item"
            :class="{ 'app-drawer__item--active': isActive(item.to) }"
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

        <div class="app-drawer__user">
          <q-avatar class="app-user__avatar" size="42px">
            АП
          </q-avatar>
          <div>
            <div class="app-drawer__user-name">Анна Петрова</div>
          </div>
        </div>
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useQuasar } from 'quasar'

const route = useRoute()
const $q = useQuasar()

const leftDrawerOpen = ref(false)

const navItems = [
  { label: 'Главная', to: '/', icon: 'home' },
  { label: 'Лошади', to: '/horses', icon: 'favorite_border' },
  { label: 'Процедуры', to: '/procedures', icon: 'monitor_heart' },
  { label: 'Задачи', to: '/tasks', icon: 'task_alt' },
  { label: 'Календарь', to: '/calendar', icon: 'calendar_month' },
  { label: 'Финансы', to: '/finances', icon: 'attach_money' },
  { label: 'Отчёты', to: '/reports', icon: 'description' },
  // { label: 'Пользователи', to: '/users', icon: 'group' },
]

const isActive = (path) => {
  if (path === '/') {
    return route.path === '/'
  }

  return route.path.startsWith(path)
}

const closeDrawer = () => {
  if ($q.screen.lt.lg) {
    leftDrawerOpen.value = false
  }
}
</script>