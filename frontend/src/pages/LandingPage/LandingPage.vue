<template>
  <q-page :class="$style.page">
    <section :class="$style.hero">
      <div :class="$style.content">
        <div :class="$style.badge">
          <q-icon name="favorite_border" size="18px" />
          <span>Забота о лошадях с помощью технологий</span>
        </div>

        <h1 :class="$style.title">
          Профессиональная система управления приютом
        </h1>

        <p :class="$style.description">
          Комплексное решение для ведения медицинских карт, планирования процедур,
          управления командой и финансового учёта в приюте для лошадей
        </p>

        <div :class="$style.actions">
          <RouterLink to="/register" :class="$style.primaryButton">
            Начать работу
          </RouterLink>
        </div>
      </div>

      <div :class="$style.imageWrap">
        <img
          :class="$style.image"
          src="https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?auto=format&fit=crop&w=1200&q=80"
          alt="Лошадь"
        />
      </div>
    </section>

    <LandingFeaturesSection />
  </q-page>
</template>

<script setup>
import LandingFeaturesSection from 'src/components/blocks/LandingFeaturesSection/LandingFeaturesSection.vue'
</script>

<style module lang="scss" src="./LandingPage.module.scss"></style>