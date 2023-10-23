<script lang="ts" setup>
export interface Emits {
  (e: 'close'): void
}

const emits = defineEmits<Emits>()
</script>

<template>
  <div class="popup">
    <div class="popup_background" @click="emits('close')"></div>
    <div class="popup_body">
      <slot name="popup_body"></slot>
    </div>
  </div>
</template>

<style scoped>
.popup {
  position: fixed;
  width: 100%;
  height: 100vh;
  display: grid;
  place-items: center;
  z-index: 20;
  padding: 2rem;
}

.popup_background {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background-color: var(--popup-background);
  backdrop-filter: blur(10px);
  z-index: 30;
}

.popup_body {
  z-index: 40;
  background-color: var(--black100);
  padding: 2rem;
  border-radius: 1rem;
  width: 100%;
  max-width: 350px;
}
</style>