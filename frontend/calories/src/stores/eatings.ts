import { ref, reactive } from 'vue'
import { defineStore } from 'pinia'
import type { EatingResponse } from '@/api/eatings'
import type { ProductResponse } from '@/api/products'
import type { PaginatedResponse } from '@/utils/types'

export const useEatingsStore = defineStore('eatings', () => {
  const products = ref<ProductResponse[]>([])
  const eatings = ref<EatingResponse[]>([])
  const paginatedProducts = reactive<PaginatedResponse<ProductResponse>>({
    page: 0,
    per_page: 0,
    pages_count: 0,
    total: 0,
    data: [],
  })
  const myPaginatedProducts = reactive<PaginatedResponse<ProductResponse>>({
    page: 0,
    per_page: 0,
    pages_count: 0,
    total: 0,
    data: [],
  })

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

  const addMyPaginatedProduct = (product: ProductResponse) => {
    myPaginatedProducts.data.push(product)
  }

  const addMyPaginatedProducts = (products: PaginatedResponse<ProductResponse>) => {
    if (products.page > myPaginatedProducts.page) {
      myPaginatedProducts.page = products.page
    }

    for (const product of products.data) {
      if (myPaginatedProducts.data.map(p => p.id).includes(product.id)) {
        continue
      }

      myPaginatedProducts.data.push(product)
    }
  }

  const addPaginatedProducts = (products: PaginatedResponse<ProductResponse>) => {
    paginatedProducts.pages_count = products.pages_count
    if (products.page > paginatedProducts.page) {
      paginatedProducts.page = products.page
    }

    for (const product of products.data) {
      if (paginatedProducts.data.map(p => p.id).includes(product.id)) {
        continue
      }

      paginatedProducts.data.push(product)
    }
  }

  return {
    products,
    paginatedProducts,
    myPaginatedProducts,
    eatings,
    addEatings,
    addProducts,
    addMyPaginatedProduct,
    addMyPaginatedProducts,
    addPaginatedProducts,
  }
})
