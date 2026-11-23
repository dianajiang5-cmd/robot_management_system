<template>
  <div>
    <!-- 顶部大机器人图标 -->
    <div class="bg-white rounded-xl shadow-sm p-8 mb-6 text-center relative overflow-hidden">
      <div class="absolute inset-0 bg-blue-50 opacity-30"></div>
      <i class="fa-solid fa-robot text-7xl text-blue-500 mb-4 relative z-10 animate-bounce"></i>
      <h1 class="text-3xl font-bold text-gray-800 relative z-10">Welcome to the Robot Site Information Management System</h1>
      <p class="text-gray-500 mt-2 relative z-10">This is a professional robot equipment monitoring and management system.</p>
      
      <div class="mt-6 flex justify-center space-x-4 relative z-10">
        <router-link to="/robots" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-full font-medium transition shadow-lg shadow-blue-500/30">
          <i class="fa-solid fa-play mr-2"></i> Go to robots and sites 
        </router-link>
        <router-link to="/monitor" class="bg-white text-blue-600 border border-blue-200 hover:border-blue-400 px-6 py-2 rounded-full font-medium transition shadow-sm">
          <i class="fa-solid fa-satellite-dish mr-2"></i> Check out the bots monitor 
        </router-link>
      </div>
    </div>

    <!-- 数据卡片 (统计) -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <!-- Total Robots -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center hover:shadow-md transition">
        <div class="w-14 h-14 rounded-full bg-blue-100 flex items-center justify-center mr-4">
          <i class="fa-solid fa-robot text-2xl text-blue-600"></i>
        </div>
        <div>
          <p class="text-gray-500 text-sm font-semibold">Total Robots</p>
          <h3 class="text-2xl font-bold text-gray-800">{{ data.total_robots || 0 }}</h3>
        </div>
      </div>

      <!-- Online Rate -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center hover:shadow-md transition">
        <div class="w-14 h-14 rounded-full bg-green-100 flex items-center justify-center mr-4">
          <i class="fa-solid fa-wifi text-2xl text-green-600"></i>
        </div>
        <div>
          <p class="text-gray-500 text-sm font-semibold">Online Rate</p>
          <h3 class="text-2xl font-bold text-gray-800">{{ data.online_rate || '0%' }}</h3>
        </div>
      </div>

      <!-- Active Alerts -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center hover:shadow-md transition">
        <div class="w-14 h-14 rounded-full bg-yellow-100 flex items-center justify-center mr-4 animate-pulse">
          <i class="fa-solid fa-triangle-exclamation text-2xl text-yellow-600"></i>
        </div>
        <div>
          <p class="text-gray-500 text-sm font-semibold">Active Alerts</p>
          <h3 class="text-2xl font-bold text-gray-800 text-yellow-600">{{ data.active_alerts || 0 }}</h3>
        </div>
      </div>

      <!-- Abnormal Params Rate -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center hover:shadow-md transition">
        <div class="w-14 h-14 rounded-full bg-red-100 flex items-center justify-center mr-4">
          <i class="fa-solid fa-heart-pulse text-2xl text-red-600"></i>
        </div>
        <div>
          <p class="text-gray-500 text-sm font-semibold">Abnormal Params</p>
          
          <h3 class="text-2xl font-bold text-red-600">{{ data.abnormal_params_rate || '0%' }}</h3>
        </div>
      </div>
    </div>
    
    <!-- 调试用的刷新按钮 -->
    <div class="mt-6 text-center">
      <button @click="fetchData" class="text-sm text-blue-500 hover:underline">
        <i class="fa-solid fa-rotate-right mr-1"></i> Refresh Data
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const data = ref({})

const fetchData = async () => {
  try {
    const res = await api.get('/api/dashboard/')
    data.value = res.data
    console.log("Dashboard Data loaded:", data.value) // 打印数据到控制台看看
  } catch (err) {
    console.error(err)
    alert("获取仪表盘数据失败: " + (err.response?.data?.detail || err.message))
  }
}

onMounted(fetchData)
</script>
