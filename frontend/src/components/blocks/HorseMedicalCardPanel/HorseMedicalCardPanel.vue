<template>
  <q-card :class="[$style.root, 'app-card']">
    <div :class="$style.header">
      <div>
        <div :class="$style.title">Медицинская карта</div>
        <div :class="$style.subtitle">История медицинских записей</div>
      </div>

      <AppButton
        color="primary"
        unelevated
        no-caps
        icon="add"
        label="Добавить запись"
        :class="$style.addButton"
      />
    </div>

    <div :class="$style.timeline">
      <div :class="$style.line"></div>

      <div :class="$style.timelineItem">
        <div :class="$style.dot"></div>

        <div :class="$style.timelineContent">
          <div :class="$style.meta">
            <span :class="$style.type">Осмотр</span>
            <span :class="$style.date">15 февраля 2026</span>
          </div>

          <div :class="$style.timelineTitle">
            Профилактический осмотр
          </div>

          <div :class="$style.text">
            Состояние отличное
          </div>

          <div :class="$style.text">
            Ответственный: Дмитрий Соколов
          </div>
        </div>
      </div>
    </div>
  </q-card>
</template>

<script setup>
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
</script>

<style module lang="scss" src="./HorseMedicalCardPanel.module.scss"></style>
