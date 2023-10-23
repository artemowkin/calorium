<script setup lang="ts">
import { useRouter } from 'vue-router';
import { ref, reactive } from 'vue'
import { sendVerificationCode, validateVerificationCode, getMe, updateMe } from '@/api/users'
import { useUsersStore } from '@/stores/users'
import type { FormInstance, FormRules } from 'element-plus';
import UserUpdateForm from '@/components/UserUpdateForm.vue';

const currentStep = ref<number>(1)

const formError = ref<string>("")

const canResendCode = ref<boolean>(true)

const resendCodeTimer = ref<number>(0)

interface AuthenticateForm {
  height: number
  weight: number
  age: number
  sex: 'male' | 'female'
  activity: 'lowest' | 'low' | 'middle' | 'high' | 'highest'
}

interface EmailForm {
  email: string
}

interface VerificationForm {
  code: string
}

const emailFormRef = ref<FormInstance>()

const verificationCodeRef = ref<FormInstance>()

const emailFormRules = reactive<FormRules<EmailForm>>({
  email: [
    { required: true, type: 'email', message: 'Укажите правильный email', trigger: 'blur' }
  ]
})

const verificationFormRules = reactive<FormRules<VerificationForm>>({
  code: [
    { required: true, type: 'string', message: "Введен неправильный код верификации. Проверьте сообщение" }
  ]
})

const usersStore = useUsersStore()

const emailInfo = reactive<EmailForm>({
  email: "",
})

const verificationInfo = reactive<VerificationForm>({
  code: "",
})

const userInfo = reactive<AuthenticateForm>({
  age: 18,
  height: 170,
  weight: 60,
  sex: 'male',
  activity: 'middle',
})

const router = useRouter()

const onSendCode = async () => {
  emailFormRef.value!.validate(async (valid) => {
    if (!valid) return

    try {
      await sendVerificationCode(emailInfo.email)
      currentStep.value = 2
    } catch (e: any) {
      formError.value = e.message
    }
  })
}

const updateResendCode = () => {
  resendCodeTimer.value -= 1

  if (resendCodeTimer.value > 0) {
    setTimeout(updateResendCode, 1000)
  } else {
    canResendCode.value = true
  }
}

const onCodeResend = async () => {
  await sendVerificationCode(emailInfo.email)
  canResendCode.value = false
  resendCodeTimer.value = 30
  updateResendCode()
}

const onAuthenticate = () => {
  verificationCodeRef.value!.validate(async (valid) => {
    if (!valid) return

    try {
      const tokens = await validateVerificationCode(emailInfo.email, verificationInfo.code)

      localStorage.setItem('accessToken', tokens.access_token)
      localStorage.setItem('refreshToken', tokens.refresh_token)

      const user = await getMe(tokens.access_token)

      if (!user.age) {
        currentStep.value = 3
      } else {
        usersStore.setCurrentUser(user)
        router.push({ name: 'home' })
      }
    } catch (e: any) {
      formError.value = e.message
    }
  })
}

const onUpdate = async () => {
  try {
    const token = localStorage.getItem('accessToken')!

    const updatedUser = await updateMe(token, userInfo)

    usersStore.setCurrentUser(updatedUser)

    router.push({ name: 'home' })
  } catch (e: any) {
    formError.value = e.message
  }
}
</script>

<template>
  <div class="authentication_container">
    <el-form @submit.prevent="onSendCode" ref="emailFormRef" :model="emailInfo" :rules="emailFormRules" label-position="top" v-if="currentStep === 1">
      <h2>Аутентификация</h2>
      <div class="error_message" v-show="formError">{{ formError }}</div>
      <el-form-item label="Email" prop="email">
        <el-input type="text" v-model="emailInfo.email" placeholder="email" />
      </el-form-item>
      <el-button type="primary" @click="onSendCode">Отправить код</el-button>
    </el-form>
    <el-form @submit.prevent="onAuthenticate" ref="verificationCodeRef" :model="verificationInfo" :rules="verificationFormRules" label-position="top" v-else-if="currentStep === 2">
      <h2>Код верификации</h2>
      <div class="error_message" v-show="formError">{{ formError }}</div>
      <el-form-item label="Код верификации" prop="code">
        <el-input type="text" v-model="verificationInfo.code" placeholder="Код верификации" />
      </el-form-item>
      <div class="resend_code_container">
        <div class="resend_code_link" v-if="canResendCode" @click="onCodeResend">Отправить код заново</div>
        <div class="resend_code_message" v-else>Отправить заново через {{ resendCodeTimer }} с.</div>
      </div>
      <div class="buttons_container">
        <el-button type="primary" @click="onAuthenticate">Аутентификация</el-button>
        <el-button @click="currentStep = 1">Назад</el-button>
      </div>
    </el-form>
    <UserUpdateForm v-else-if="currentStep === 3" title="Расскажите о себе" v-model="userInfo" @save="onUpdate" :error="formError" />
  </div>
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

.buttons_container {
  display: grid;
  gap: .5rem;
}

.resend_code_container {
  margin: 1rem 0;
}

.resend_code_link {
  color: var(--blue);
  cursor: pointer;
}

.resend_code_message {
  color: var(--gray100);
}

.error_message {
  background-color: var(--red-transparent);
  color: var(--red);
  border: 1px solid var(--red);
  padding: 1rem;
  border-radius: .5rem;
}

.kkals_norm {
  margin: 1rem 0;
  color: var(--white);
  font-size: 1.2rem;
  font-weight: bold;
  text-align: center;
}

.authentication_container {
  width: 100%;
  height: 100vh;
  display: grid;
  place-items: center;
  padding: 2rem;
}

.authentication_container form {
  background-color: var(--black100);
  border-radius: 1rem;
  padding: 2rem;
  width: 100%;
  max-width: 300px;
}

.authentication_container form .el-form-item {
  margin: 1rem 0;
}

.authentication_container form button {
  width: 100%;
  margin: 0;
}

.authentication_container form h2 {
  text-align: center;
  color: var(--white);
}

.point_selector {
  display: grid;
  grid-template-columns: 1fr;
  gap: .5rem;
}

.point_selector__title {
  color: var(--gray100);
}

.point_selector__container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}

.point_selector__item, .point_selector__item_current {
  padding: .5rem;
  text-align: center;
  border-radius: .5rem;
  cursor: pointer;
}

.point_selector__item:hover {
  background-color: var(--blue-transparent);
}

.point_selector__item_current {
  background-color: var(--blue100);
}

.counter {
  display: grid;
  grid-template-columns: 1fr;
  gap: .5rem;
}

.counter__title {
  color: var(--gray100);
}

.counter__container {
  display: grid;
  grid-template-columns: 20px 50px 20px;
  gap: .5rem;
  place-content: center;
}

.counter__value {
  background-color: var(--black200);
  text-align: center;
  padding: .25rem;
  border-radius: 10rem;
  border: 0;
}

.counter__icon {
  display: grid;
  place-items: center;
  font-size: 1.5rem;
  cursor: pointer;
  user-select: none;
}
</style>