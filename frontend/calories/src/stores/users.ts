import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { UserResponse } from '@/api/users'

export const useUsersStore = defineStore('users', () => {
  const currentUser = ref<UserResponse | null>(null)

  const setCurrentUser = (user: UserResponse) => {
    currentUser.value = user
  }

  const clearCurrentUser = () => {
    currentUser.value = null
  }

  return { currentUser, setCurrentUser, clearCurrentUser }
})
