<template>
  <q-layout view="hHh lpR fFf">
    <q-header class="app-header">
      <q-toolbar class="app-toolbar">
        <RouterLink to="/" class="app-logo">
          <div class="app-logo__mark">
            <q-icon name="favorite" size="24px" />
          </div>

          <div class="app-logo__text">
            <div>Приют для</div>
            <div>лошадей</div>
          </div>
        </RouterLink>

        <nav class="app-nav">
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

        <div class="app-user">
          <q-avatar class="app-user__avatar" size="42px">
            АП
          </q-avatar>
          <div class="app-user__name">Анна Петрова</div>
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

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
</script>