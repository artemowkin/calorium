<script setup lang="ts">
import { reactive, computed, ref } from 'vue';
import type { FormRules, FormInstance } from 'element-plus';
import type { UpdateData } from '@/api/users';

export interface Props {
  modelValue: UpdateData
  title: string
  error: string
}

export interface Emits {
  (e: 'save'): void
}

const props = defineProps<Props>()

const emits = defineEmits<Emits>()

const updateFormRef = ref<FormInstance>()

interface AuthenticateForm {
  height: number
  weight: number
  age: number
  sex: 'male' | 'female'
  activity: 'lowest' | 'low' | 'middle' | 'high' | 'highest'
}

const authenticateFormRules = reactive<FormRules<AuthenticateForm>>({
  height: [
    { required: true, type: 'integer', min: 10, max: 400, message: "Укажите правильный рост", trigger: 'blur' },
  ],
  weight: [
    { required: true, type: 'integer', min: 1, max: 500, message: "Укажите правильный вес", trigger: 'blur' },
  ],
  age: [
    { required: true, type: 'integer', min: 1, max: 100, message: "Укажите правильный возраст", trigger: 'blur' }
  ],
  sex: [
    { required: true, trigger: 'blur' },
  ],
  activity: [
    { required: true, trigger: 'blur' },
  ],
})

const activitiesKoefficients = {
  lowest: 1.2,
  low: 1.375,
  middle: 1.55,
  high: 1.7,
  highest: 1.9
}

const kkalsNorm = computed<number>(() => {
  if (props.modelValue.sex === 'male') {
    return Math.round((10 * props.modelValue.weight + 6.25 * props.modelValue.height - 5 * props.modelValue.age + 5) * activitiesKoefficients[props.modelValue.activity])
  } else {
    return Math.round((10 * props.modelValue.weight + 6.25 * props.modelValue.height - 5 * props.modelValue.age - 161) * activitiesKoefficients[props.modelValue.activity])
  }
})

const onSave = () => {
  updateFormRef.value!.validate(valid => {
    if (!valid) return
    else {
      emits('save')
    }
  })
}
</script>

<template>
  <el-form @submit.prevent="onSave" ref="updateFormRef" :model="props.modelValue" :rules="authenticateFormRules" label-position="top">
    <h2>{{ props.title }}</h2>
    <div class="error_message" v-show="props.error">{{ props.error }}</div>
    <el-form-item label="Возраст" prop="age">
      <el-input-number :min="1" :max="100" v-model="props.modelValue.age" />
    </el-form-item>
    <el-form-item label="Рост" prop="height">
      <el-input-number :min="10" :max="400" v-model="props.modelValue.height" />
    </el-form-item>
    <el-form-item label="Вес" prop="weight">
      <el-input-number :min="1" :max="500" v-model="props.modelValue.weight" />
    </el-form-item>
    <el-form-item label="Пол" group="sex">
      <el-radio-group v-model="props.modelValue.sex" label="sex">
        <el-radio-button label="male">Мужчина</el-radio-button>
        <el-radio-button label="female">Женщина</el-radio-button>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="Активность" group="activity">
      <el-radio-group v-model="props.modelValue.activity" label="activity">
        <el-radio-button label="lowest">Минимальная</el-radio-button>
        <el-radio-button label="low">Низкая</el-radio-button>
        <el-radio-button label="middle">Средняя</el-radio-button>
        <el-radio-button label="high">Высокая</el-radio-button>
        <el-radio-button label="highest">Тяжелая</el-radio-button>
      </el-radio-group>
    </el-form-item>
    <div class="kkals_norm">Норма ккал в сутки: {{ kkalsNorm }}</div>
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

form button {
  width: 100%;
  margin-top: 1rem;
}
</style>