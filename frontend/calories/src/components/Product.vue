<script setup lang="ts">
import type { ProductResponse } from '../api/products'

export interface Props {
  product: ProductResponse
  editable?: boolean
  deleteable?: boolean
}

export interface Emits {
  (e: 'delete', product: ProductResponse): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()

const onDelete = () => {
  emits('delete', props.product)
}

const onWeightInput  = (e: any) => {
  props.product.mass = +e.target.value || 0
}
</script>

<template>
  <div class="product">
    <img :src="props.product.file_url" />
    <div class="product__body">
      <div class="product__title">{{ props.product.title }}</div>
      <div class="product__weight">
        <input :disabled="!props.editable" class="product__weight" type="text" :value="props.product.mass" @input="onWeightInput">
        <span>гр.</span>
      </div>
    </div>
    <div v-show="props.deleteable" class="product__delete" @click="onDelete">
      <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
        <path class="delete_icon" d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/>
      </svg>
    </div>
  </div>
</template>

<style scoped>
.product {
  display: grid;
  grid-template-columns: 50px 1fr 30px;
  gap: .75rem;
  justify-items: start;
  align-items: center;
}

.product__body {
  display: grid;
  grid-template-columns: 1fr;
  gap: .25rem;
}

.product img {
  width: 50px;
  height: 50px;
  border-radius: .5rem;
}

.product__weight {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: .25rem;
}

.product__weight input {
  background-color: var(--black200);
  padding: .25rem .5rem;
  font-size: .75rem;
  border-radius: 10rem;
  width: 50px;
  text-align: center;
  outline: none;
  border: 0;
}

.product__delete {
  background-color: var(--red-transparent);
  width: 30px;
  height: 30px;
  border-radius: 25rem;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.product__delete svg {
  width: 20px;
  height: 20px;
}

.delete_icon {
  fill: var(--red);
}
</style>