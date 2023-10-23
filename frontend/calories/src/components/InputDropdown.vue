<script setup lang="ts">
</script>

<template>
  <div class="dropdown">
    <slot name="dropdown_items"></slot>
  </div>
</template>

<style scoped>
.dropdown {
  position: absolute;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  background-color: var(--black100);
  border-radius: .5rem;
  display: grid;
  grid-template-columns: 1fr;
  gap: .5rem;
  padding: .5rem;
}
</style>