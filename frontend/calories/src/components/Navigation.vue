<script setup lang="ts">
import type { UserResponse } from '@/api/users';
import { RouterLink } from 'vue-router';

export interface Props {
  user: UserResponse
}

const props = defineProps<Props>()
</script>

<template>
  <div class="navigation">
    <RouterLink :to="{ name: 'home' }">
      <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M320-240h60v-80h80v-60h-80v-80h-60v80h-80v60h80v80Zm200-30h200v-60H520v60Zm0-100h200v-60H520v60Zm44-152 56-56 56 56 42-42-56-58 56-56-42-42-56 56-56-56-42 42 56 56-56 58 42 42Zm-314-70h200v-60H250v60Zm-50 472q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z"/></svg>
      <div class="link__title">Калькулятор</div>
    </RouterLink>
    <RouterLink :to="{ name: 'statistic' }">
      <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M560-564v-68q33-14 67.5-21t72.5-7q26 0 51 4t49 10v64q-24-9-48.5-13.5T700-600q-38 0-73 9.5T560-564Zm0 220v-68q33-14 67.5-21t72.5-7q26 0 51 4t49 10v64q-24-9-48.5-13.5T700-380q-38 0-73 9t-67 27Zm0-110v-68q33-14 67.5-21t72.5-7q26 0 51 4t49 10v64q-24-9-48.5-13.5T700-490q-38 0-73 9.5T560-454ZM260-320q47 0 91.5 10.5T440-278v-394q-41-24-87-36t-93-12q-36 0-71.5 7T120-692v396q35-12 69.5-18t70.5-6Zm260 42q44-21 88.5-31.5T700-320q36 0 70.5 6t69.5 18v-396q-33-14-68.5-21t-71.5-7q-47 0-93 12t-87 36v394Zm-40 118q-48-38-104-59t-116-21q-42 0-82.5 11T100-198q-21 11-40.5-1T40-234v-482q0-11 5.5-21T62-752q46-24 96-36t102-12q58 0 113.5 15T480-740q51-30 106.5-45T700-800q52 0 102 12t96 36q11 5 16.5 15t5.5 21v482q0 23-19.5 35t-40.5 1q-37-20-77.5-31T700-240q-60 0-116 21t-104 59ZM280-494Z"/></svg>
      <div class="link__title">Статистика</div>
    </RouterLink>
    <RouterLink :to="{ name: 'products' }">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 16L7.27627 17.6576C7.54232 19.2539 7.67535 20.0521 8.23484 20.526C8.79433 21 9.6035 21 11.2218 21H12.7782C14.3965 21 15.2057 21 15.7652 20.526C16.3247 20.0521 16.4577 19.2539 16.7237 17.6576L17 16" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M13.5 4.5C14 3.5 15 3 16 3" stroke-width="2" stroke-linecap="round"/>
        <circle cx="12" cy="6" r="2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M10 7.53503C9.26376 7.96082 8.67546 8.6147 8.33205 9.40116C8.17639 9.75764 7.82814 9.99151 7.43926 10.0007C6.08688 10.0327 5 11.1396 5 12.5C5 13.8807 6.11929 15 7.5 15C8.04262 15 8.54217 14.8283 8.95113 14.5361C9.26819 14.3095 9.68796 14.2878 10.0267 14.4804C10.6081 14.8109 11.2804 15 12 15C12.7196 15 13.3919 14.8109 13.9733 14.4804C14.312 14.2878 14.7318 14.3095 15.0489 14.5361C15.4578 14.8283 15.9574 15 16.5 15C17.8807 15 19 13.8807 19 12.5C19 11.1396 17.9131 10.0327 16.5607 10.0007C16.1719 9.99151 15.8236 9.75764 15.668 9.40116C15.3245 8.6147 14.7362 7.96082 14 7.53503V5.34143C15.3777 5.82843 16.5238 6.80421 17.2308 8.05908C19.3687 8.40833 21 10.2635 21 12.5C21 14.9853 18.9853 17 16.5 17C15.7509 17 15.0429 16.8163 14.4205 16.4915C13.6793 16.8185 12.8599 17 12 17C11.1401 17 10.3207 16.8185 9.57953 16.4915C8.95709 16.8163 8.24912 17 7.5 17C5.01472 17 3 14.9853 3 12.5C3 10.2635 4.63129 8.40833 6.76921 8.05908C7.47619 6.80421 8.62233 5.82843 10 5.34143V7.53503Z" />
      </svg>
      <div class="link__title">Продукты</div>
    </RouterLink>
    <RouterLink :to="{ name: 'user' }">
      <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24"><path d="M234-276q51-39 114-61.5T480-360q69 0 132 22.5T726-276q35-41 54.5-93T800-480q0-133-93.5-226.5T480-800q-133 0-226.5 93.5T160-480q0 59 19.5 111t54.5 93Zm246-164q-59 0-99.5-40.5T340-580q0-59 40.5-99.5T480-720q59 0 99.5 40.5T620-580q0 59-40.5 99.5T480-440Zm0 360q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q53 0 100-15.5t86-44.5q-39-29-86-44.5T480-280q-53 0-100 15.5T294-220q39 29 86 44.5T480-160Zm0-360q26 0 43-17t17-43q0-26-17-43t-43-17q-26 0-43 17t-17 43q0 26 17 43t43 17Zm0-60Zm0 360Z"/></svg>
      <div class="link__title">Аккаунт</div>
    </RouterLink>
  </div>
</template>

<style scoped>
.navigation {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--black100-transparent);
  backdrop-filter: blur(1rem);
  display: grid;
  place-content: center;
  grid-auto-flow: column;
  grid-auto-columns: 1fr;
  padding: .5rem;
  gap: 1rem;
}

.navigation a {
  text-decoration: none;
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: repeat(2, 1fr);
  place-items: center;
  padding: .25rem;
  border-radius: .5rem;
}

.navigation a svg {
  fill: var(--gray100);
}

.navigation a:hover {
  background-color: var(--black100-transparent);
}

.navigation .link__title {
  font-size: .75rem;
  color: var(--gray100);
}
</style>