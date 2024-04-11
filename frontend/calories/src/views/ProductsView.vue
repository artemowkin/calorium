<script setup lang="ts">
import { onMounted, ref, computed, reactive } from 'vue'
import { useUsersStore } from '@/stores/users';
import { getMe } from '@/api/users';
import { useRouter } from 'vue-router';
import { getAllEatings } from '@/api/eatings'
import Navigation from '@/components/Navigation.vue';
import ProductsList from '@/components/ProductsList.vue';
import ProductsListNavigation from '@/components/ProductsListNavigation.vue';
import AppPopUp from '@/components/AppPopUp.vue';
import ProductForm from '@/components/ProductForm.vue';
import { type ProductResponse, type CreateProductData, getProducts, createProduct } from '@/api/products'
import { useEatingsStore } from '@/stores/eatings'
import type { PaginatedResponse } from '@/utils/types';

const usersStore = useUsersStore()

const router = useRouter()

const eatingsStore = useEatingsStore()

const currentPage = ref<'my' | 'generic'>('generic')

const currentPopUp = ref<'add-product' | null>(null)

const currentPageProducts = computed<PaginatedResponse<ProductResponse>>(() => {
  if (currentPage.value == 'my') {
    return eatingsStore.myPaginatedProducts
  }

  return eatingsStore.paginatedProducts
})

const productData = reactive<CreateProductData>({
  title: "",
  kkal: 1,
  image: null,
})

const fullLoaded = computed(() => {
  if (currentPage.value == 'my') {
    return eatingsStore.myPaginatedProducts.page >= eatingsStore.myPaginatedProducts.pages_count
  } else {
    console.log(eatingsStore.paginatedProducts.page, eatingsStore.paginatedProducts.pages_count)
    return eatingsStore.paginatedProducts.page >= eatingsStore.paginatedProducts.pages_count
  }
})

const onSaveProduct = async () => {
  const token = localStorage.getItem('accessToken')

  if (!token) {
    router.push({ name: 'login' })
    return
  }

  const createdProduct = await createProduct(token, productData)

  productData.image = null
  productData.title = ""
  productData.kkal = 1

  eatingsStore.addMyPaginatedProduct(createdProduct)
  currentPopUp.value = null
}

onMounted(async () => {
  const token = localStorage.getItem('accessToken')

  if (!token) {
    router.push({ name: 'login' })
    return
  }

  const user = await getMe(token)
  usersStore.setCurrentUser(user)

  const loadedEatings = await getAllEatings(token)
  eatingsStore.addEatings(loadedEatings)
  const productsIds: number[] = []
  eatingsStore.eatings.forEach(e => {
    e.products.forEach(prod => {
      if (productsIds.includes(prod.product_id)) {
        return
      }

      productsIds.push(prod.product_id)
    })
  })

  if (productsIds.length) {
    const loadedProducts = await getProducts({ ids: productsIds, perPage: productsIds.length })
    eatingsStore.addProducts(loadedProducts.data)
  }

  const paginatedMyProducts = await getProducts({ my: true, token })
  const paginatedProducts = await getProducts({})
  eatingsStore.addMyPaginatedProducts(paginatedMyProducts)
  eatingsStore.addPaginatedProducts(paginatedProducts)
})

const loadMoreProducts = async () => {
  const token = localStorage.getItem('accessToken')

  if (!token) {
    router.push({ name: 'login' })
    return
  }

  if (currentPage.value == 'generic') {
    if (eatingsStore.paginatedProducts.page == eatingsStore.paginatedProducts.pages_count) {
      return
    }

    const page = eatingsStore.paginatedProducts.page + 1
    console.log("Loading generic products page =", page)
    const paginatedProducts = await getProducts({ page })

    eatingsStore.addPaginatedProducts(paginatedProducts)
  } else {
    if (eatingsStore.myPaginatedProducts.page >= eatingsStore.myPaginatedProducts.pages_count) {
      return
    }

    const page = eatingsStore.myPaginatedProducts.page + 1

    console.log("Loading my products page =", page)
    const paginatedMyProducts = await getProducts({ my: true, token, page })
    eatingsStore.addMyPaginatedProducts(paginatedMyProducts)
  }
}
</script>

<template>
  <AppPopUp v-if="currentPopUp == 'add-product'" @close="currentPopUp = null">
    <div class="add_product_popup_inner">
      <ProductForm v-model="productData" title="Добавить продукт" @save="onSaveProduct" @cancel="currentPopUp = null" />
    </div>
  </AppPopUp>
  <ProductsListNavigation :current-page="currentPage" @set-current-page="(newPage: 'my' | 'generic') => currentPage = newPage" />
  <div class="products_page">
    <ProductsList
      @load="loadMoreProducts"
      :full="fullLoaded"
      :products="currentPageProducts.data" />
  </div>
  <button v-if="currentPage == 'my'" class="add_button" @click="currentPopUp = 'add-product'">+</button>
  <Navigation v-if="usersStore.currentUser" :user="usersStore.currentUser" />
</template>

<style scoped>
.products_page {
  padding: 1rem;
  padding-bottom: 5rem;
}

.add_button {
  position: fixed;
  bottom: 6rem;
  right: 1.5rem;
  background-color: var(--blue);
  color: var(--white);
  font-size: 3rem;
  width: 60px;
  height: 60px;
  display: grid;
  place-items: center;
  border-radius: 1000px;
  border: 0;
  cursor: pointer;
}
</style>