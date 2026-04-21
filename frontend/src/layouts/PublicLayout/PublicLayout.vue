<template>
  <q-layout view="hHh lpR fFf">
    <q-header :class="$style.header">
      <q-toolbar :class="$style.toolbar">
        <RouterLink to="/" :class="$style.logo">
          <div :class="$style.logoMark">
            <q-icon name="favorite" size="24px" />
          </div>

          <div :class="$style.logoText">
            <div>Приют лошадей</div>
            <div :class="$style.logoSubtext">Система управления</div>
          </div>
        </RouterLink>

        <div :class="$style.actions">
          <RouterLink to="/login" :class="$style.loginLink">
            Вход
          </RouterLink>

          <RouterLink to="/register" :class="$style.registerButton">
            Регистрация
          </RouterLink>
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup></script>

<style module lang="scss" src="./PublicLayout.module.scss"></style>