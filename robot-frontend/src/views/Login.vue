<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="bg-white p-10 rounded-xl shadow-lg w-96 border-t-4 border-blue-500">
      <h2 class="text-2xl font-bold text-center mb-8">Robot System Login</h2>
      <div class="mb-5">
        <label class="block text-gray-600 text-sm mb-2">Username</label>
        <input v-model="form.username" type="text" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400">
      </div>
      <div class="mb-6">
        <label class="block text-gray-600 text-sm mb-2">Password</label>
        <input v-model="form.password" type="password" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400">
      </div>
      <button @click="handleLogin" class="w-full bg-theme text-white py-2 rounded-lg shadow-md hover:bg-blue-700">Login</button>
      <p v-if="error" class="text-red-500 text-sm mt-4 text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({ username: '', password: '' })
const error = ref('')

const handleLogin = async () => {
  try {
    const params = new URLSearchParams()
    params.append('username', form.value.username)
    params.append('password', form.value.password)
    // 注意：如果你的后端登录接口是 /api/user/login，请按需修改
    const res = await api.post('/api/user/login', params)
    localStorage.setItem('token', res.data.access_token)
    localStorage.setItem('username', form.value.username)
    router.push('/dashboard')
  } catch (err) {
    error.value = '用户名或密码错误'
  }
}
</script>