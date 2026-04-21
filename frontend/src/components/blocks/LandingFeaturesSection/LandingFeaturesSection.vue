<template>
  <section :class="$style.section">
    <div :class="$style.container">
      <div :class="$style.badge">Возможности</div>

      <h2 :class="$style.title">Всё необходимое для управления приютом</h2>

      <p :class="$style.description">
        Комплексный набор функций для ежедневной работы с животными, командой
        и документацией
      </p>

      <div :class="$style.grid">
        <article
          v-for="item in features"
          :key="item.title"
          :class="$style.card"
        >
          <div :class="$style.iconWrap">
            <q-icon :name="item.icon" size="30px" />
          </div>

          <h3 :class="$style.cardTitle">{{ item.title }}</h3>

          <p :class="$style.cardText">
            {{ item.description }}
          </p>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
const features = [
  {
    icon: 'favorite_border',
    title: 'Карточки лошадей',
    description:
      'Полная информация о каждой лошади: характеристики, история, фотографии и медицинские данные',
  },
  {
    icon: 'assignment',
    title: 'Медицинские записи',
    description:
      'Ведение истории процедур, вакцинаций, осмотров и лечения с автоматическими напоминаниями',
  },
  {
    icon: 'description',
    title: 'Документооборот',
    description:
      'Централизованное хранение документов, договоров и регистрационных данных',
  },
  {
    icon: 'group',
    title: 'Управление ролями',
    description:
      'Гибкая система прав доступа для администраторов, ветеринаров, кураторов и волонтёров',
  },
  {
    icon: 'calendar_month',
    title: 'Задачи и события',
    description:
      'Планирование процедур, кормлений, тренировок и других мероприятий с календарём',
  },
  {
    icon: 'shield',
    title: 'Финансовый учёт',
    description:
      'Отслеживание расходов, пожертвований и формирование финансовых отчётов',
  },
]
</script>

<style module lang="scss" src="./LandingFeaturesSection.module.scss"></style>