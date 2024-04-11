<script setup lang="ts">
export interface Props {
    currentPage: 'my' | 'generic'
}

export interface Emits {
    (e: 'set-current-page', newCurrentPage: 'my' | 'generic'): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()
</script>

<template>
  <div class="products_list_navigation">
    <button :class="props.currentPage == 'generic' ? 'active' : null" @click="emits('set-current-page', 'generic')">Общие</button>
    <button :class="props.currentPage == 'my' ? 'active' : null" @click="emits('set-current-page', 'my')">Мои</button>
  </div>
</template>

<style scoped>
.products_list_navigation {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  background-color: var(--black);
}

.products_list_navigation button {
  background-color: transparent;
  border: 0;
  font-size: 1rem;
  padding: 1rem;
  cursor: pointer;
  border-bottom: 2px solid var(--black);
}

.products_list_navigation button.active {
  border-bottom: 2px solid var(--blue);
}
</style>