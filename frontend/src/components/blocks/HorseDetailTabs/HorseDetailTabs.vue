<template>
  <q-card :class="[$style.root, 'app-card']">
    <div :class="$style.list">
      <button :class="[$style.item, $style.itemActive]">
        Медицинская карта
      </button>

      <button :class="$style.item">
        Процедуры
      </button>

      <button :class="$style.item">
        Задачи
      </button>

      <button :class="$style.item">
        Документы
      </button>
    </div>
  </q-card>
</template>

<script setup>
</script>

<style module lang="scss" src="./HorseDetailTabs.module.scss"></style>
