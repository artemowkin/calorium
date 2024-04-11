<script setup lang="ts">
import { reactive, ref } from 'vue';
import type { FormRules, FormInstance, UploadProps } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';

export interface Props {
  modelValue: object
  title: string
  error: string
}

export interface Emits {
  (e: 'save'): void
  (e: 'cancel'): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()

const productFormRef = ref<FormInstance>()

interface ProductForm {
  image: File
  title: string
  kkal: number
}

const productFormRules = reactive<FormRules<ProductForm>>({
  image: [
    { required: false, message: "Необходимо загрузить изображение", trigger: 'blur' },
  ],
  title: [
    { required: true, type: 'string', message: "Необходимо задать название продукта", trigger: 'blur' },
  ],
  kkal: [
    { required: true, type: 'integer', min: 1, max: 10000, message: "Укажите правильную калорийность", trigger: 'blur' }
  ],
})

const imageUrl = ref<string>('')

const onSave = () => {
  productFormRef.value!.validate(valid => {
    if (!valid) return
    else {
      emits('save')
    }
  })
}

const onChange: UploadProps['onChange'] = (file) => {
  if (!file || !file.raw) {
    imageUrl.value = ""
    props.modelValue.image = null
    return
  }

  props.modelValue.image = file.raw
  imageUrl.value = URL.createObjectURL(file.raw)
}
</script>

<template>
  <el-form @submit.prevent="onSave" ref="productFormRef" :model="props.modelValue" :rules="productFormRules" label-position="top">
    <h3>{{ props.title }}</h3>
    <div class="error_message" v-show="props.error">{{ props.error }}</div>
    <el-form-item label="Изображение" prop="image">
      <el-upload
        action="#"
        :auto-upload="false"
        :multiple="false"
        :on-change="onChange"
        :show-file-list="false"
        class="upload-icon"
      >
        <img v-if="imageUrl" :src="imageUrl" alt="" class="avatar" />
        <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
      </el-upload>
    </el-form-item>
    <el-form-item label="Название" prop="title">
      <el-input v-model="props.modelValue.title" />
    </el-form-item>
    <el-form-item label="Калорийность на 100 гр." prop="kkal">
      <el-input-number v-model="props.modelValue.kkal" :min="1" :max="10000" />
    </el-form-item>
    <el-button type="primary" @click="onSave">Сохранить</el-button>
  </el-form>
</template>

<style scoped>
.error_message {
  background-color: var(--red-transparent);
  color: var(--red);
  border: 1px solid var(--red);
  padding: 1rem;
  border-radius: .5rem;
  margin-top: 1rem;
  width: 100%;
}

.avatar {
  width: 100%;
  object-fit: cover;
  aspect-ratio: 1;
}

.upload-icon {
  width: 100%;
}

.avatar-uploader-icon {
  width: 100%;
  height: 100%;
  /* background-color: rgba(255, 255, 255, .025); */
  background-color: #191e25;
  border: 1px solid #383d46;
  border-radius: 4px;
}

form button {
  width: 100%;
  margin-top: 1rem;
}
</style>

<style>
.el-upload {
  width: 100%;
  aspect-ratio: 1;
}
</style>