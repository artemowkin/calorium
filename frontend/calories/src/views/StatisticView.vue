<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useUsersStore } from '@/stores/users';
import { getMe } from '@/api/users';
import { useRouter } from 'vue-router';
import { getAllEatings, getEatingsStatistic } from '@/api/eatings'
import Navigation from '@/components/Navigation.vue';
import EatingsList from '@/components/EatingsList.vue';
import { getProducts } from '@/api/products'
import { useEatingsStore } from '@/stores/eatings'
import { BarChart } from 'vue-chart-3';
import { Chart, registerables } from "chart.js";

Chart.register(...registerables)

const startMonth = ref("")

const stopMonth = ref("")

const plusMonth = (month: string): string => {
  const monthDate = new Date(month)
  const newYear = monthDate.getMonth() == 12 ? monthDate.getFullYear() + 1 : monthDate.getFullYear()
  const newMonth = monthDate.getMonth() == 12 ? 1 : monthDate.getMonth() + 1
  monthDate.setFullYear(newYear)
  monthDate.setMonth(newMonth)
  const newValue = monthDate.toISOString().split("T")[0].slice(0, 7)
  return newValue
}

const minusMonth = (month: string): string => {
  const monthDate = new Date(month)
  const newYear = monthDate.getMonth() == 1 ? monthDate.getFullYear() - 1 : monthDate.getFullYear()
  const newMonth = monthDate.getMonth() == 1 ? 12 : monthDate.getMonth() - 1
  monthDate.setFullYear(newYear)
  monthDate.setMonth(newMonth)
  const newValue = monthDate.toISOString().split("T")[0].slice(0, 7)
  return newValue
}

const onNextMonthClick = () => {
  startMonth.value = plusMonth(startMonth.value)
  stopMonth.value = plusMonth(stopMonth.value)
  loadStatistics()
}

const onPreviousMonthClick = () => {
  startMonth.value = minusMonth(startMonth.value)
  stopMonth.value = minusMonth(stopMonth.value)
  loadStatistics()
}

const testData = reactive({
  labels: ["Янв", "Фев", "Март", "Апр", "Май", "Июн", "Июл", "Авг", "Сент", "Окт", "Ноя", "Дек"],
  datasets: [
    {
      label: "Ккал",
      data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2],
      backgroundColor: ["#1f56bb"],
    }
  ]
})

const usersStore = useUsersStore()

const router = useRouter()

const eatingsStore = useEatingsStore()

const loadStatistics = async () => {
  const token = localStorage.getItem("accessToken")
  if (!token) {
    return
  }

  const statistics = await getEatingsStatistic(token, startMonth.value, stopMonth.value)
  const labels: string[] = []
  const values: number[] = []
  statistics.forEach(s => {
    labels.push(s.date.split("-")[2])
    values.push(s.total_kkals)
  })

  testData.labels = labels
  testData.datasets[0].data = values
}

onMounted(async () => {
  const token = localStorage.getItem('accessToken')

  if (!token) {
    router.push({ name: 'login' })
    return
  }

  const user = await getMe(token)
  usersStore.setCurrentUser(user)

  const loadedEatings = await getAllEatings(token, )
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
    const loadedProducts = await getProducts({ ids: productsIds, token })
    eatingsStore.addProducts(loadedProducts.data)
  }

  const dt = new Date()
  startMonth.value = dt.toISOString().split("T")[0].slice(0, 7)
  dt.setMonth(dt.getMonth() + 1)
  stopMonth.value = dt.toISOString().split("T")[0].slice(0, 7)

  await loadStatistics()
})
</script>

<template>
  <div class="eatings_page">
    <div class="statistic__control">
      <div class="statistic__control__button" @click="onPreviousMonthClick">&lt;</div>
      <div class="statistic__control__value">{{ startMonth }}</div>
      <div class="statistic__control__button" @click="onNextMonthClick">&gt;</div>
    </div>
    <BarChart :chartData="testData" />
    <EatingsList v-if="eatingsStore.eatings.length && eatingsStore.products.length" :eatings="eatingsStore.eatings" :products="eatingsStore.products" />
  </div>
  <Navigation v-if="usersStore.currentUser" :user="usersStore.currentUser" />
</template>

<style scoped>
.statistic__control {
  display: grid;
  grid-template-columns: 40px 1fr 40px;
}

.statistic__control__value {
  display: grid;
  place-content: center;
}

.statistic__control__button {
  background-color: #1f56bb;
  color: white;
  border-radius: .5rem;
  cursor: pointer;
  display: grid;
  place-content: center;
  width: 100%;
  height: 40px;
}

.eatings_page {
  padding: 1rem;
  padding-bottom: 5rem;
}
</style>