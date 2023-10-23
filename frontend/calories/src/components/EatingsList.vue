<script setup lang="ts">
import { computed } from 'vue';
import type { EatingProductResponse, EatingResponse } from '@/api/eatings';
import type { ProductResponse } from '@/api/products';
import Product from './Product.vue';

export interface Props {
  eatings: EatingResponse[]
  products: ProductResponse[]
}

const props = defineProps<Props>()

const eatingsDates = computed<Date[]>(() => {
  const dates: number[] = []

  for (const eating of props.eatings) {
    console.log(new Date(eating.timestamp).toDateString())
    const date = new Date(new Date(eating.timestamp).toDateString())

    if (dates.includes(+date)) continue

    dates.push(+date)
  }

  return dates.sort((a, b) => b - a).map(d => new Date(d))
})

const getDateEatings = (date: Date) => {
  return props.eatings.filter(eating => {
    return +date === +new Date(new Date(eating.timestamp).toDateString())
  }).sort((a, b) => +new Date(b.timestamp) - +new Date(a.timestamp))
}

const getProduct = (eatingProduct: EatingProductResponse) => {
  const product = props.products.find(p => p.id === eatingProduct.product_id)!
  product.mass = eatingProduct.mass
  return product
}

const getTotalKkals = (eatingProducts: EatingProductResponse[]) => {
  let summary = 0

  for (let eatingProduct of eatingProducts) {
    const product = props.products.find(p => p.id === eatingProduct.product_id)!
    summary += (eatingProduct.mass * product.kkal) / 100
  }

  return Math.round(summary)
}

const getTotalKkalsForDate = (date: Date) => {
  const eatings = getDateEatings(date)
  let totalKkals = 0

  for (const eating of eatings) {
    totalKkals += getTotalKkals(eating.products)
  }

  return totalKkals
}
</script>

<template>
  <div class="eatings_list">
    <div class="eatings_date" v-for="(eatingDate, _) in eatingsDates" :key="eatingDate.toISOString()">
      <div class="eatings_date_header">
        <div class="eatings_date_value">{{ eatingDate.toLocaleDateString('ru', { year: 'numeric', month: 'long', day: 'numeric' }) }}</div>
        <div class="eatings_date_total_kkals">{{ getTotalKkalsForDate(eatingDate) }} Ккал.</div>
      </div>
      <div class="eatings_container">
        <div class="eating" v-for="(eating, _) in getDateEatings(eatingDate)" :key="eating.id">
          <div class="eating_header">
            <div class="product_time">Прием пищи в {{ new Date(eating.timestamp).toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' }) }}</div>
            <div class="eating_total_kkals">{{ getTotalKkals(eating.products) }} ккал.</div>
          </div>
          <div class="products_container">
            <Product v-for="(product, _) in eating.products" :key="product.product_id" :product="getProduct(product)" :editable="false" :deleteable="false" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.eatings_list, .eatings_date {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.eatings_date_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.eating_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.eatings_date_value, .eatings_date_total_kkals {
  color: var(--gray100);
}

.eatings_container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.eating {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  background-color: var(--black100);
  border-radius: 1rem;
  padding: 1rem;
}

.products_container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}
</style>