<script setup lang="ts">
import { onMounted } from 'vue'
import { useUsersStore } from '@/stores/users';
import { getMe } from '@/api/users';
import { useRouter } from 'vue-router';
import { getAllEatings } from '@/api/eatings'
import Navigation from '@/components/Navigation.vue';
import EatingsList from '@/components/EatingsList.vue';
import { getProducts } from '@/api/products'
import { useEatingsStore } from '@/stores/eatings'

const usersStore = useUsersStore()

const router = useRouter()

const eatingsStore = useEatingsStore()

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
    const loadedProducts = await getProducts({ ids: productsIds })
    eatingsStore.addProducts(loadedProducts.data)
  }
})
</script>

<template>
  <div class="eatings_page">
    <EatingsList v-if="eatingsStore.eatings.length && eatingsStore.products.length" :eatings="eatingsStore.eatings" :products="eatingsStore.products" />
  </div>
  <Navigation v-if="usersStore.currentUser" :user="usersStore.currentUser" />
</template>

<style scoped>
.eatings_page {
  padding: 1rem;
  padding-bottom: 5rem;
}
</style>