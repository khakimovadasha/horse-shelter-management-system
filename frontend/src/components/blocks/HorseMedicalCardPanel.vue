<template>
  <q-card class="app-card horse-medical-panel">
    <div class="horse-medical-panel__header">
      <div>
        <div class="horse-medical-panel__title">Медицинская карта</div>
        <div class="horse-medical-panel__subtitle">История медицинских записей</div>
      </div>

      <AppButton
        color="primary"
        unelevated
        no-caps
        icon="add"
        label="Добавить запись"
        class="horse-medical-panel__add-btn"
      />
    </div>

    <div class="horse-medical-timeline">
      <div class="horse-medical-timeline__line"></div>

      <div class="horse-medical-timeline__item">
        <div class="horse-medical-timeline__dot"></div>

        <div class="horse-medical-timeline__content">
          <div class="horse-medical-timeline__meta">
            <span class="horse-medical-timeline__type">Осмотр</span>
            <span class="horse-medical-timeline__date">15 февраля 2026</span>
          </div>

          <div class="horse-medical-timeline__title">
            Профилактический осмотр
          </div>

          <div class="horse-medical-timeline__text">
            Состояние отличное
          </div>

          <div class="horse-medical-timeline__text">
            Ответственный: Дмитрий Соколов
          </div>
        </div>
      </div>
    </div>
  </q-card>
</template>

<script setup>
import AppButton from 'src/components/ui/AppButton.vue'
</script>
