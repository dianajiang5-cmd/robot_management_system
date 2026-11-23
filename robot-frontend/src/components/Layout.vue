<template>
  <div class="flex min-h-screen bg-slate-50">
    <!-- 深色侧边栏 -->
    <div class="w-64 bg-slate-900 text-white flex flex-col fixed h-full shadow-xl z-20">
      <!-- Logo 区域 -->
      <div class="h-20 flex items-center px-6 border-b border-slate-800">
        <i class="fa-solid fa-robot text-3xl text-blue-500 mr-3"></i>
        <h1 class="text-xl font-bold tracking-wider">Robot OS</h1>
      </div>

      <!-- 导航菜单 -->
      <nav class="flex-1 p-4 space-y-2 mt-4">
        <router-link to="/dashboard" class="flex items-center px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors" active-class="bg-blue-600 text-white font-semibold shadow-md">
          <i class="fa-solid fa-chart-pie w-6"></i><span>Dashboard</span>
        </router-link>
        
        <router-link to="/robots" class="flex items-center px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors" active-class="bg-blue-600 text-white font-semibold shadow-md">
          <i class="fa-solid fa-server w-6"></i><span>Robots & Sites</span>
        </router-link>
        
        <router-link to="/monitor" class="flex items-center px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors" active-class="bg-blue-600 text-white font-semibold shadow-md">
          <i class="fa-solid fa-tachometer-alt w-6"></i><span>Monitoring</span>
        </router-link>
        
        <router-link to="/alerts" class="flex items-center px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors" active-class="bg-blue-600 text-white font-semibold shadow-md">
          <i class="fa-solid fa-bell w-6"></i><span>Alerts & Maint</span>
        </router-link>
        
        <router-link to="/profile" class="flex items-center px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors" active-class="bg-blue-600 text-white font-semibold shadow-md">
          <i class="fa-solid fa-user-gear w-6"></i><span>Profile</span>
        </router-link>
      </nav>

      <!-- 底部用户信息 -->
      <div class="p-4 border-t border-slate-800">
        <div class="flex items-center justify-between bg-slate-800 p-3 rounded-lg">
          <div class="flex items-center">
            <i class="fa-solid fa-circle-user text-2xl text-blue-400 mr-2"></i>
            <span class="text-sm font-medium">{{ username }}</span>
          </div>
          <button @click="logout" class="text-red-400 hover:text-red-300" title="Logout">
            <i class="fa-solid fa-power-off"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="ml-64 flex-1 p-8">
      <!-- 顶部欢迎栏 (类似图2) -->
      <div class="bg-white p-4 rounded-lg shadow-sm mb-6 flex justify-between items-center border-l-4 border-blue-500">
        <h2 class="text-xl font-bold text-gray-800">Welcome to the robot management system</h2>
        <div class="text-sm text-gray-500 flex items-center">
          <i class="fa-solid fa-user-shield mr-2 text-blue-500"></i> {{ username }}
        </div>
      </div>

      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref(localStorage.getItem('username') || 'User')

const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>