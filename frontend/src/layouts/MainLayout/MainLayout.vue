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
            АП
          </q-avatar>
          <div :class="$style.userName">Анна Петрова</div>
        </div>

        <q-avatar v-else :class="$style.userAvatar" size="38px">
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
            АП
          </q-avatar>
          <div>
            <div :class="$style.drawerUserName">Анна Петрова</div>
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

<style module lang="scss" src="./MainLayout.module.scss"></style>
