<template>
  <div class="max-w-2xl bg-white p-8 rounded-lg shadow-sm border border-blue-100">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">User Profile</h2>
    
    <div class="space-y-4 mb-8">
      <div><label class="text-gray-500 text-sm">Username</label><p class="font-medium text-gray-800">{{ user.username }}</p></div>
      <div><label class="text-gray-500 text-sm">Email</label><p class="font-medium text-gray-800">{{ user.email }}</p></div>
      <div><label class="text-gray-500 text-sm">Role</label><p class="font-medium text-theme uppercase">{{ user.role_name }}</p></div>
    </div>

    <hr class="mb-6">

    <h3 class="text-lg font-bold text-gray-700 mb-4">Change Password</h3>
    <div class="space-y-4">
      <input v-model="pwdForm.old_password" type="password" placeholder="Old Password" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400">
      <input v-model="pwdForm.new_password" type="password" placeholder="New Password" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400">
      <button @click="changePwd" class="theme-blue px-6 py-2 rounded-lg shadow">Update Password</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref({})
const pwdForm = ref({ old_password: '', new_password: '' })

onMounted(async () => {
  try {
    const res = await api.get('/api/user/info')
    user.value = res.data
  } catch (err) { console.error(err) }
})

const changePwd = async () => {
  try {
    await api.put('/api/user/password', pwdForm.value)
    alert('密码修改成功，请重新登录！')
    localStorage.clear()
    router.push('/login')
  } catch (err) {
    alert(err.response?.data?.detail || '修改失败')
  }
}
</script>