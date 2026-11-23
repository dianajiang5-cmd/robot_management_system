<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Device Monitoring</h2>
      <!-- 保留快捷模拟按钮 -->
      <button @click="mockUpload" class="bg-gray-100 text-gray-700 hover:bg-gray-200 px-4 py-2 rounded-lg text-sm shadow transition">
        <i class="fa-solid fa-bolt mr-1 text-yellow-500"></i> Quick Mock Upload
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- 左侧：参数上报表单 -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h3 class="text-lg font-bold text-gray-700 mb-4 border-b pb-2">
          <i class="fa-solid fa-upload text-blue-500 mr-2"></i>Manual Parameter Upload
        </h3>
        
        <form @submit.prevent="submitParam" class="space-y-4">
          <!-- 机器人 ID -->
          <div>
            <label class="block text-sm font-semibold text-gray-600 mb-1">Robot ID</label>
            <input v-model="robotId" type="number" required placeholder="e.g. 1" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none">
          </div>

          <!-- 参数名称与数值 -->
          <div class="flex space-x-4">
            <div class="flex-1">
              <label class="block text-sm font-semibold text-gray-600 mb-1">Parameter Name</label>
              <input v-model="paramForm.name" type="text" required placeholder="e.g. temperature" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none">
            </div>
            <div class="flex-1">
              <label class="block text-sm font-semibold text-gray-600 mb-1">Current Value</label>
              <input v-model="paramForm.value" type="number" step="0.1" required placeholder="e.g. 85.5" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none">
            </div>
          </div>

          <!-- 单位 -->
          <div>
            <label class="block text-sm font-semibold text-gray-600 mb-1">Unit</label>
            <input v-model="paramForm.unit" type="text" required placeholder="e.g. ℃" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none">
          </div>

          <!-- 阈值上下限 -->
          <div class="flex space-x-4">
            <div class="flex-1">
              <label class="block text-sm font-semibold text-gray-600 mb-1">Min Threshold</label>
              <input v-model="paramForm.min_threshold" type="number" step="0.1" required placeholder="e.g. 20" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none">
            </div>
            <div class="flex-1">
              <label class="block text-sm font-semibold text-gray-600 mb-1">Max Threshold</label>
              <input v-model="paramForm.max_threshold" type="number" step="0.1" required placeholder="e.g. 80" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none">
            </div>
          </div>

          <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg shadow-md transition mt-4">
            <i class="fa-solid fa-paper-plane mr-2"></i>Submit Parameter
          </button>
        </form>
      </div>

      <!-- 右侧：业务流转提示与结果面板 -->
      <div class="bg-blue-50 p-6 rounded-xl border border-blue-100 flex flex-col">
        <h3 class="text-lg font-bold text-blue-800 mb-4"><i class="fa-solid fa-circle-info mr-2"></i>How it works</h3>
        
        <div class="space-y-4 flex-1">
          <div class="flex items-start">
            <div class="bg-white rounded-full p-2 mt-1 mr-3 text-blue-500 shadow-sm"><i class="fa-solid fa-1"></i></div>
            <p class="text-sm text-gray-700">Fill in <b>Robot ID</b>（please fill in robot ID）。</p>
          </div>
          <div class="flex items-start">
            <div class="bg-white rounded-full p-2 mt-1 mr-3 text-blue-500 shadow-sm"><i class="fa-solid fa-2"></i></div>
            <p class="text-sm text-gray-700">Please write robot parameter values,<code class="bg-gray-200 px-1 rounded">Value</code> goes beyond <code class="bg-gray-200 px-1 rounded">Min</code> or <code class="bg-gray-200 px-1 rounded">Max</code> scope, backend will automatically treat it as an exception。</p>
          </div>
          <div class="flex items-start">
            <div class="bg-white rounded-full p-2 mt-1 mr-3 text-yellow-500 shadow-sm"><i class="fa-solid fa-triangle-exclamation"></i></div>
            <p class="text-sm text-gray-700">If exception，backend will<b>automation have a abnormal</b>you can have look menu <b>Alerts</b> check the abnormal and handle</p>
          </div>
        </div>

        <!-- 实时结果反馈 -->
        <div v-if="lastResult" class="mt-6 p-4 bg-white rounded-lg border shadow-sm">
          <p class="text-sm font-bold text-gray-700 mb-1">Latest Result:</p>
          <div v-if="lastResult.is_abnormal" class="text-red-600 flex items-center font-semibold">
            <i class="fa-solid fa-circle-exclamation mr-2 text-lg"></i> Abnormal! Alert Generated.
          </div>
          <div v-else class="text-green-600 flex items-center font-semibold">
            <i class="fa-solid fa-circle-check mr-2 text-lg"></i> Normal Parameter.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const robotId = ref(1)
const paramForm = ref({
  name: 'temperature',
  value: 85.5,
  unit: '℃',
  min_threshold: 20.0,
  max_threshold: 80.0
})
const lastResult = ref(null)

// 提交表单逻辑
const submitParam = async () => {
  try {
    lastResult.value = null
    // 替换后端路径中的 {id}
    const res = await api.post(`/api/monitor/robot/${robotId.value}/param`, paramForm.value)
    
    lastResult.value = res.data
    if (res.data.is_abnormal) {
      alert(`⚠️ 上报成功！但参数异常，已自动生成告警！去 Alerts 页面看看吧。`)
    } else {
      alert(`✅ 上报成功！参数在正常阈值范围内。`)
    }
  } catch (err) {
    alert("上报失败: " + (err.response?.data?.detail || err.message))
    console.error(err)
  }
}

// 快捷测试逻辑（保留原来的）
const mockUpload = async () => {
  try {
    const res = await api.post('/api/monitor/robot/1/param', {
      name: "temperature",
      value: 85.5,
      unit: "℃",
      min_threshold: 20.0,
      max_threshold: 80.0
    })
    alert(`上报成功！是否异常: ${res.data.is_abnormal}`)
  } catch (err) {
    alert("上报失败，请确保后端机器人 ID 1 存在")
    console.error(err)
  }
}
</script>
