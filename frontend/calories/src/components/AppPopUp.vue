<script setup lang="ts">
export interface Emits {
  (e: 'close'): void
}

const emits = defineEmits<Emits>()
</script>

<template>
  <div class="popup">
    <div class="popup_close_background" @click="emits('close')"></div>
    <div class="popup_inner">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.popup {
  width: 100%;
  height: 100%;
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  display: grid;
  grid-template-columns: 1.5fr;
  place-content: center;
  padding: 1rem;
  background-color: rgba(0, 0, 0, .5);
  backdrop-filter: blur(5px);
}

.popup_close_background {
  width: 100%;
  height: 100%;
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 3;
}

.popup_inner {
  background-color: var(--black);
  border-radius: 1rem;
  z-index: 4;
  width: 100%;
  padding: 1rem;
}
</style>