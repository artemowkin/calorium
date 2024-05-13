<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import PopUp from '../components/PopUp.vue'
import ProductDropdownItem from '../components/ProductDropdownItem.vue'
import { type ProductResponse, searchProducts } from '../api/products'
import Product from '@/components/Product.vue'
import { useUsersStore } from '@/stores/users'
import { getMe } from '@/api/users'
import InputDropdown from '@/components/InputDropdown.vue'
import Navigation from '@/components/Navigation.vue'
import type { FormInstance, FormRules } from 'element-plus'
import { saveEating } from '@/api/eatings'
import type { EatingData } from '@/api/eatings'

const currentPopUp = ref<'addProduct' | 'loginPrompt' | null>(null)

const deferredPrompt = ref<any | null>(null)

const onPopUpClose = () => {
  document.body.style.overflow = 'auto'
  currentPopUp.value = null
  productQuery.value = ""
}

const usersStore = useUsersStore()

interface EatingForm {
  timestamp: Date
}

const createForm = reactive<EatingForm>({
  timestamp: new Date()
})

const createFormRules = reactive<FormRules<EatingForm>>({
  timestamp: [
    { required: true, message: "Укажите дату и время према пищи", trigger: 'blur' }
  ]
})

const createFormRef = ref<FormInstance>()

const productQuery = ref<string>("")

const searchedProducts = ref<ProductResponse[]>([])

const selectedProducts = ref<ProductResponse[]>([])

const summaryCalories = computed<number>(() => {
  let summary = 0

  for (let product of selectedProducts.value) {
    summary += (product.mass * product.kkal) / 100
  }

  return Math.round(summary)
})

const onProductQueryInput = async (value: string) => {
  productQuery.value = value
  const products = await searchProducts(value)
  const selectedProductsIds: number[] = selectedProducts.value.map(p => p.id)
  searchedProducts.value = products.filter(p => !selectedProductsIds.includes(p.id))
}

const showAddProduct = () => {
  document.body.style.overflow = 'hidden'
  currentPopUp.value = 'addProduct'
}

const onProductSelect = (product: ProductResponse) => {
  product.mass = 100
  selectedProducts.value.push(product)
  searchedProducts.value = []
  currentPopUp.value = null
  productQuery.value = ""
  document.body.style.overflow = 'auto'
}

const onProductDelete = (product: ProductResponse) => {
  selectedProducts.value = selectedProducts.value.filter(p => p.id !== product.id)
}

const saveClick = () => {
  createFormRef.value!.validate(async (valid) => {
    if (!valid) {
      return
    }

    if (!usersStore.currentUser) {
      currentPopUp.value = 'loginPrompt'
    }

    const token = localStorage.getItem('accessToken')

    if (!token) {
      return
    }

    const data: EatingData = {
      timestamp: createForm.timestamp,
      products: selectedProducts.value.map(p => ({ id: p.id, mass: p.mass }))
    }
    console.log(data)

    try {
      await saveEating(token, data)
      resetCalculator()
    } catch (e) {
      return
    }
  })
}

const resetCalculator = () => {
  selectedProducts.value = []
  createForm.timestamp = new Date()
}

const onInstallClose = () => {
  deferredPrompt.value = null
}

const installClick = () => {
  deferredPrompt.value!.prompt()
  deferredPrompt.value = null
}

onMounted(async () => {
  const token = localStorage.getItem('accessToken')

  if (!token || usersStore.currentUser) return

  const user = await getMe(token)
  usersStore.setCurrentUser(user)
})

window.addEventListener('beforeinstallprompt', e => {
  deferredPrompt.value = e
})
</script>

<template>
  <PopUp v-if="currentPopUp === 'addProduct'" @close="onPopUpClose">
    <template v-slot:popup_body>
      <div class="add_product_form">
        <h2>Добавить продукт</h2>
        <div class="product_input_container">
          <el-input autofocus placeholder="Продукт" v-model="productQuery" @input="onProductQueryInput" />
          <InputDropdown>
            <template v-slot:dropdown_items>
              <ProductDropdownItem v-for="(product, _) in searchedProducts" :product="product" @select="onProductSelect" />
            </template>
          </InputDropdown>
        </div>
      </div>
    </template>
  </PopUp>
  <PopUp v-show="currentPopUp === 'loginPrompt'" @close="onPopUpClose">
    <template v-slot:popup_body>
      <div class="login_prompt_form">
        <div class="login_prompt_form__header">
          <img src="/icon48.png">
          <h2>Calorium</h2>
        </div>
        <p>Откройте больше функционала, рассказав нам немного о себе :)</p>
        <RouterLink to="/login">Войти</RouterLink>
      </div>
    </template>
  </PopUp>
  <PopUp v-show="deferredPrompt" @close="onInstallClose">
    <template #popup_body>
      <div class="install_form">
        <h2>Установите приложение</h2>
        <div class="buttons_container">
          <el-button type="primary" @click="installClick">Установить</el-button>
          <el-button @click="onInstallClose">Отмена</el-button>
        </div>
      </div>
    </template>
  </PopUp>
  <div>
    <div class="content">
      <div class="calculator">
        <h1>Калькулятор</h1>
        <div class="selected_products" v-if="selectedProducts.length">
          <div class="products_list">
            <Product v-for="(product, _) in selectedProducts" :product="product" @delete="onProductDelete" :editable="true" :deleteable="true" :showProductKkals="true" />
          </div>
        </div>
        <button class="add_button" @click="showAddProduct">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
            <path class="add_icon" d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z"/>
          </svg>
        </button>
        <div v-show="selectedProducts.length">
          <div class="summary_calories">{{ summaryCalories }} Ккал.</div>
          <el-form ref="createFormRef" :model="createForm" :rules="createFormRules">
            <el-form-item prop="timestamp">
              <el-date-picker v-model="createForm.timestamp" type="datetime" placeholder="Дата и время приема пищи" />
            </el-form-item>
          </el-form>
          <el-button type="primary" @click="saveClick">Сохранить</el-button>
        </div>
      </div>
    </div>
  </div>
  <Navigation v-if="usersStore.currentUser" :user="usersStore.currentUser" />
</template>

<style scoped>
.install_form {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.install_form .buttons_container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
}

.install_form .buttons_container .install {
  background-color: var(--blue);
  color: var(--white);
}

.el-button {
  width: 100%;
}

.content {
  display: grid;
  place-items: center;
  height: fit-content;
  min-height: 100vh;
  padding: 1rem;
  padding-bottom: 5rem;
}

.content h1 {
  text-align: center;
}

.calculator {
  background-color: var(--black100);
  padding: 1rem;
  border-radius: 1rem;
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  width: 100%;
  max-width: 300px;
}

@media (max-width: 700px) {
  .calculator {
    max-width: 700px;
  }
}

.calculator h1 {
  text-align: center;
}

.add_button {
  cursor: pointer;
  width: fit-content;
  display: grid;
  place-items: center;
  padding: .5rem 1rem;
  place-self: center;
  background-color: var(--blue-transparent);
  border: 0;
  border-radius: .5rem;
}

.add_icon {
  fill: var(--blue);
}

.product_input_container {
  position: relative;
}

.add_product_form {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.add_product_form h2 {
  text-align: center;
}

.products_list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.summary_items {
  display: grid;
  grid-template-columns: 1fr;
  gap: .5rem;
}

.summary_calories {
  text-align: center;
  font-size: 1.5rem;
  margin-bottom: .75rem;
}

.save_button {
  width: 100%;
  padding: .5rem;
  background-color: var(--blue);
  color: var(--white);
  border: 0;
  border-radius: .25rem;
  font-size: 1rem;
  cursor: pointer;
}

.login_prompt_form {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.login_prompt_form p {
  text-align: justify;
}

.login_prompt_form a {
  width: 100%;
  padding: .5rem;
  background-color: var(--blue);
  color: var(--white);
  border: 0;
  border-radius: .25rem;
  font-size: 1rem;
  text-align: center;
  text-decoration: none;
}

.login_prompt_form__header {
  display: grid;
  grid-template-columns: 48px 1fr;
  gap: .25rem;
  justify-items: start;
  align-items: center;
}

.login_prompt_form__header h2 {
  display: grid;
  grid-template-columns: 48px 1fr;
  gap: .25rem;
}
</style>