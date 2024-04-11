<script setup lang="ts">
import { ref } from 'vue'
import type { ProductResponse } from '@/api/products'
import ProductListItem from './ProductListItem.vue'
import InfiniteLoading from "v3-infinite-loading"
import "v3-infinite-loading/lib/style.css"

export interface Props {
  products: ProductResponse[]
  full: boolean
}

export interface Emits {
  (e: 'load'): Promise<void>
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()

const productsContainer = ref()

const loadMore = async ($state) => {
  console.log("Load more. Full = ", props.full)
  await emits('load')

  if (props.full) {
    $state.complete()
    return
  }

  $state.error()
}
</script>

<template>
  <div class="products_list" ref="productsContainer">
    <ProductListItem v-if="props.products.length" v-for="product in props.products" :product="product" :key="product.id"></ProductListItem>
    <div v-else>Тут пока что нет продуктов. Самое время их добавить!</div>
  </div>
  <InfiniteLoading @infinite="loadMore" :firstload="false">
    <template #complete>
      <div></div>
    </template>
    <template #error>
      <div></div>
    </template>
  </InfiniteLoading>
</template>

<style scoped>
.products_list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}
</style>