<template>
  <AppDashboardSection
    title="Ближайшие процедуры"
    subtitle="Запланированные медицинские мероприятия"
    action-label="Все"
    :action-to="actionTo"
  >
    <div :class="$style.list">
      <UpcomingProcedureItem
        v-for="item in items"
        :key="item.id"
        :horse-name="item.horseName"
        :procedure-name="item.procedureName"
        :scheduled-at="item.scheduledAt"
        :status-label="item.statusLabel"
        :status-tone="item.statusTone"
      />
    </div>
  </AppDashboardSection>
</template>

<script setup>
import AppDashboardSection from 'src/components/ui/AppDashboardSection/AppDashboardSection.vue'
import UpcomingProcedureItem from 'src/components/blocks/UpcomingProcedureItem/UpcomingProcedureItem.vue'

defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  actionTo: {
    type: String,
    default: '/app/procedures',
  },
})
</script>

<style module lang="scss" src="./DashboardUpcomingProceduresSection.module.scss"></style>
