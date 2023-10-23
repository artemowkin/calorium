import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { EatingResponse } from '@/api/eatings'
import type { ProductResponse } from '@/api/products'

export const useEatingsStore = defineStore('eatings', () => {
  const products = ref<ProductResponse[]>([])
  const eatings = ref<EatingResponse[]>([])

  const addEatings = (addingEatings: EatingResponse[]) => {
    for (const eating of addingEatings) {
      if (!eatings.value.map(e => e.id).includes(eating.id)) {
        eatings.value.push(eating)
      }
    }
  }

  const addProducts = (addingProducts: ProductResponse[]) => {
    for (const product of addingProducts) {
      if (!products.value.map(p => p.id).includes(product.id)) {
        products.value.push(product)
      }
    }
  }

  return { products, eatings, addEatings, addProducts }
})
