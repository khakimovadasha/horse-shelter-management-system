<template>
  <q-card :class="[$style.root, 'app-card']">
    <div :class="$style.top">
      <div :class="$style.avatar">{{ initials }}</div>

      <div :class="$style.titleBlock">
        <h1 :class="$style.name">{{ fullName }}</h1>

        <AppStatusBadge
          :class="$style.roleBadge"
          :label="roleLabel"
          :tone="roleTone"
        />
      </div>
    </div>

    <div :class="$style.infoGrid">
      <div :class="$style.primaryInfo">
        <div :class="$style.contactItem">
          <q-icon name="mail_outline" :class="$style.icon" />
          <span>{{ user.email || 'Не указано' }}</span>
        </div>

        <div :class="$style.contactItem">
          <q-icon name="call" :class="$style.icon" />
          <span>{{ user.phone || 'Не указано' }}</span>
        </div>
      </div>

      <div :class="$style.secondaryInfo">
        <AppInfoItem
          label="Имя пользователя"
          :value="user.username || 'Не указано'"
        />

        <AppInfoItem
          label="Роль"
          :value="roleLabel"
        />
      </div>
    </div>
  </q-card>
</template>

<script setup>
import { computed } from 'vue'

import AppInfoItem from 'src/components/ui/AppInfoItem/AppInfoItem.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
})

const fullName = computed(() => {
  const value = `${props.user.first_name || ''} ${props.user.last_name || ''}`.trim()
  return value || 'Пользователь'
})

const initials = computed(() => {
  const first = (props.user.first_name || '').trim().charAt(0)
  const last = (props.user.last_name || '').trim().charAt(0)
  const value = `${first}${last}`.toUpperCase()

  return value || (props.user.username || 'U').slice(0, 2).toUpperCase()
})

const roleLabel = computed(() => {
  switch (props.user.role) {
    case 'admin':
      return 'Администратор'
    case 'veterinarian':
      return 'Ветеринар'
    default:
      return 'Волонтёр'
  }
})

const roleTone = computed(() => {
  switch (props.user.role) {
    case 'admin':
      return 'admin'
    case 'veterinarian':
      return 'veterinarian'
    default:
      return 'volunteer'
  }
})
</script>

<style module lang="scss" src="./UserProfileCard.module.scss"></style>
