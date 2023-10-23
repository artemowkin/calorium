<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getMe, updateMe } from '@/api/users';
import type { UpdateData } from '@/api/users'
import { useUsersStore } from '@/stores/users';
import Navigation from '@/components/Navigation.vue';
import PopUp from '@/components/PopUp.vue';
import UserUpdateForm from '@/components/UserUpdateForm.vue';

const router = useRouter()

const usersStore = useUsersStore()

const currentPopUp = ref<'update' | null>(null)

const formError = ref<string>("")

const userUpdateData = reactive<UpdateData>({
  age: 0,
  height: 0,
  weight: 0,
  sex: 'male',
  activity: 'middle',
})

const activityAliases = {
  lowest: 'Минимальная',
  low: 'Низкая',
  middle: 'Средняя',
  high: 'Высокая',
  highest: 'Тяжелая',
}

onMounted(async () => {
  const token = localStorage.getItem('accessToken')

  if (!token) {
    router.push({ name: 'login' })
    return
  }

  const user = await getMe(token)
  usersStore.setCurrentUser(user)
  userUpdateData.age = user.age!
  userUpdateData.height = user.height!
  userUpdateData.weight = user.weight!
  userUpdateData.sex = user.sex!
  userUpdateData.activity = user.activity!
})

const activitiesKoefficients = {
  lowest: 1.2,
  low: 1.375,
  middle: 1.55,
  high: 1.7,
  highest: 1.9
}

const kkalsNorm = computed(() => {
  if (usersStore.currentUser!.sex === 'male') {
    return Math.round((10 * usersStore.currentUser!.weight! + 6.25 * usersStore.currentUser!.height! - 5 * usersStore.currentUser!.age! + 5) * activitiesKoefficients[usersStore.currentUser!.activity!])
  } else {
    return Math.round((10 * usersStore.currentUser!.weight! + 6.25 * usersStore.currentUser!.height! - 5 * usersStore.currentUser!.age! - 161) * activitiesKoefficients[usersStore.currentUser!.activity!])
  }
})

const onLogout = () => {
  localStorage.clear()
  usersStore.clearCurrentUser()
  router.push({ name: 'home' })
}

const onPopUpClose = () => {
  userUpdateData.age = usersStore.currentUser!.age!
  userUpdateData.height = usersStore.currentUser!.height!
  userUpdateData.weight = usersStore.currentUser!.weight!
  userUpdateData.sex = usersStore.currentUser!.sex!
  userUpdateData.activity = usersStore.currentUser!.activity!
  currentPopUp.value = null
}

const onUpdate = async () => {
  try {
    const token = localStorage.getItem('accessToken')

    const user = await updateMe(token!, userUpdateData)
    usersStore.setCurrentUser(user)
    onPopUpClose()
  } catch (e: any) {
    formError.value = e.message
  }
}

const onUpdateClick = () => {
  currentPopUp.value = 'update'
}
</script>

<template>
  <PopUp v-show="currentPopUp === 'update'" @close="onPopUpClose">
    <template #popup_body>
      <UserUpdateForm v-model="userUpdateData" @save="onUpdate" :error="formError" title="Изменить данные" />
    </template>
  </PopUp>
  <div v-if="usersStore.currentUser" class="user_info">
    <div class="user_info__email">{{ usersStore.currentUser.email }}</div>
    <div class="user_info__fields">
      <div class="user_info__field">
        <div class="user_info__field__label">Возраст</div>
        <div class="user_info__field__value">{{ usersStore.currentUser.age }}</div>
      </div>
      <div class="user_info__field">
        <div class="user_info__field__label">Рост</div>
        <div class="user_info__field__value">{{ usersStore.currentUser.height }}</div>
      </div>
      <div class="user_info__field">
        <div class="user_info__field__label">Вес</div>
        <div class="user_info__field__value">{{ usersStore.currentUser.weight }}</div>
      </div>
      <div class="user_info__field">
        <div class="user_info__field__label">Нагрузка</div>
        <div class="user_info__field__value">{{ activityAliases[usersStore.currentUser.activity!] }}</div>
      </div>
    </div>
    <div class="user_info__total_calories">
      <div class="user_info__total_calories__label">Норма калорий в день</div>
      <div class="user_info__total_calories__value">{{ kkalsNorm }}</div>
    </div>
    <div class="user_info__buttons_container">
      <el-button type="primary" @click="onUpdateClick">Изменить</el-button>
      <el-button @click="onLogout" type="danger">Выйти</el-button>
    </div>
  </div>
  <Navigation v-if="usersStore.currentUser" :user="usersStore.currentUser" />
</template>

<style scoped>
.user_info {
  padding: 1rem;
  padding-bottom: 5rem;
}

.user_info__email {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.user_info__fields {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 1rem;
}

.user_info__field {
  padding: 1rem;
  background-color: var(--black100);
  border-radius: 1rem;
  display: grid;
  grid-template-columns: 1fr;
  gap: .5rem;
}

.user_info__field__label {
  color: var(--gray100);
  font-size: .8rem;
}

.user_info__field__value {
  text-align: center;
  font-size: 1.25rem;
}

.user_info__total_calories {
  padding: 1rem;
  background-color: var(--black100);
  border-radius: 1rem;
  display: grid;
  grid-template-columns: 1fr;
  gap: .5rem;
  margin-top: 1rem;
}

.user_info__total_calories__label {
  color: var(--gray100);
  font-size: .8rem;
}

.user_info__total_calories__value {
  text-align: center;
  font-size: 1.25rem;
}

.user_info__buttons_container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-top: 1rem;
}

.user_info__buttons_container button {
  margin: 0;
}
</style>