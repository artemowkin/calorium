<script setup lang="ts">
import type { ProductResponse } from '../api/products'

export interface Props {
  product: ProductResponse
}

const props = defineProps<Props>()
</script>

<template>
  <div class="product">
    <img :src="props.product.file_url" />
    <div class="product__body">
      <div class="product__title">{{ props.product.title }}</div>
      <div class="product__info">
        <span class="product__kkal">{{ props.product.kkal }}</span>
        <span>Ккал. на 100 гр.</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.product {
  display: grid;
  grid-template-columns: 1fr;
  overflow: hidden;
  border-radius: 1rem;
}

.product__body {
  display: grid;
  grid-template-columns: 1fr;
  gap: .75rem;
  background-color: var(--black100);
  padding: 1rem;
}

.product__title {
  font-size: 2rem;
}

.product img {
  width: 100%;
  aspect-ratio: 1;
  height: auto;
  object-fit: cover;
}

.product__info {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: .5rem;
}

.product__kkal {
  background-color: var(--black200);
  padding: .25rem .5rem;
  border-radius: 10rem;
  width: 50px;
  text-align: center;
  outline: none;
  border: 0;
}
</style>