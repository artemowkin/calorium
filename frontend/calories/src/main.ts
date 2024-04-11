import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import '@/styles/element/index.scss'
import ElementPlus from 'element-plus'
import InfiniteLoading from "v3-infinite-loading"

const app = createApp(App)

app.component("infinite-loading", InfiniteLoading)

app.use(createPinia())
app.use(ElementPlus)
app.use(router)

app.mount('#app')
