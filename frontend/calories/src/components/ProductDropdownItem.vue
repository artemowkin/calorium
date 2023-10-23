<script setup lang="ts">
import { type ProductResponse } from '../api/products'

export interface Props {
  product: ProductResponse
}

export interface Emits {
  (e: 'select', product: ProductResponse): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()

const onClick = () => {
  emits('select', props.product)
}
</script>

<template>
  <div class="product" @click="onClick">
    <img :src="props.product.file_url" />
    <div class="product__title">{{ props.product.title }}</div>
  </div>
</template>

<style scoped>
.product {
  display: grid;
  grid-template-columns: 50px 1fr;
  gap: .5rem;
  justify-items: start;
  align-items: center;
  cursor: pointer;
  border-radius: .5rem;
}

.product__title {
  padding-right: .5rem;
}

.product:hover {
  background-color: var(--black200);
}

.product img {
  width: 50px;
  height: 50px;
  border-radius: .5rem;
}
</style>