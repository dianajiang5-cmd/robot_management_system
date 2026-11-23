<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative min-h-[600px]">
    <!-- 顶部 Tab 和 新增按钮 -->
    <div class="flex border-b border-gray-200 bg-gray-50 justify-between items-center pr-6">
      <div class="flex">
        <button @click="activeTab = 'alerts'" :class="['py-4 px-8 font-semibold flex items-center transition-colors', activeTab === 'alerts' ? 'text-blue-600 border-b-2 border-blue-600 bg-white' : 'text-gray-500 hover:text-gray-700']">
          <i class="fa-solid fa-bell text-yellow-500 mr-2"></i> Active Alerts
        </button>
        <button @click="activeTab = 'maintenance'" :class="['py-4 px-8 font-semibold flex items-center transition-colors', activeTab === 'maintenance' ? 'text-blue-600 border-b-2 border-blue-600 bg-white' : 'text-gray-500 hover:text-gray-700']">
          <i class="fa-solid fa-screwdriver-wrench text-gray-600 mr-2"></i> Maintenance Records
        </button>
      </div>
      <button v-if="activeTab === 'maintenance'" @click="openMaintModal" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm shadow transition">
        <i class="fa-solid fa-plus mr-1"></i> Add Record
      </button>
    </div>

    <!-- 告警列表 -->
    <div v-show="activeTab === 'alerts'" class="p-6 overflow-x-auto">
      <div v-if="alerts.length === 0" class="text-center text-gray-400 py-10">
        <i class="fa-solid fa-check-circle text-4xl mb-2 text-green-400"></i>
        <p>All clear! No alerts found.</p>
      </div>
      <table v-else class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 text-gray-600 text-sm border-b">
            <th class="p-4 font-semibold">Robot ID</th>
            <th class="p-4 font-semibold">Alert Message</th>
            <th class="p-4 font-semibold">Status</th>
            <th class="p-4 font-semibold text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alert in alerts" :key="alert.id" class="hover:bg-gray-50 border-b last:border-b-0" :class="{'bg-yellow-50/50': !alert.is_resolved}">
            <td class="p-4 text-gray-600 font-medium">{{ alert.robot_id }}</td>
            <td class="p-4 text-sm">
              <div class="flex items-start">
                <i v-if="!alert.is_resolved" class="fa-solid fa-triangle-exclamation text-yellow-500 mt-1 mr-3 text-lg animate-pulse"></i>
                <i v-else class="fa-solid fa-circle-check text-green-500 mt-1 mr-3 text-lg"></i>
                <span :class="alert.is_resolved ? 'text-gray-400 line-through' : 'text-gray-800 font-medium'">{{ alert.message }}</span>
              </div>
              <p v-if="alert.resolve_note" class="text-xs text-blue-500 mt-1 ml-8">Note: {{ alert.resolve_note }}</p>
            </td>
            <td class="p-4">
              <span :class="alert.is_resolved ? 'text-green-600 bg-green-50' : 'text-yellow-700 bg-yellow-100'" class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
                {{ alert.is_resolved ? 'Resolved' : 'Active' }}
              </span>
            </td>
            <td class="p-4 text-right">
              <button v-if="!alert.is_resolved" @click="openResolveModal(alert)" class="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-1.5 rounded shadow text-sm transition">
                Mark Resolved
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 维修记录列表与统计 -->
    <div v-show="activeTab === 'maintenance'" class="p-6">
<!-- 统计卡片 -->
      <div class="grid grid-cols-3 gap-6 mb-6">
        <!-- 1. 维修总数 (Total Count) -->
        <div class="bg-blue-50 p-4 rounded-lg border border-blue-100 text-center">
          <p class="text-sm text-blue-600 font-semibold">Total Count</p>
          <p class="text-2xl font-bold text-gray-800">{{ stats.total_count || 0 }}</p>
        </div>
        
        <!-- 2. 维修总费用 (Total Cost) -->
        <div class="bg-green-50 p-4 rounded-lg border border-green-100 text-center">
          <p class="text-sm text-green-600 font-semibold">Total Cost</p>
          <p class="text-2xl font-bold text-gray-800">¥ {{ stats.total_cost || 0 }}</p>
        </div>
        
        <!-- 3. 维修总时长 (Total Duration) -->
        <div class="bg-purple-50 p-4 rounded-lg border border-purple-100 text-center">
          <p class="text-sm text-purple-600 font-semibold">Total Duration</p>
          <p class="text-2xl font-bold text-gray-800">{{ stats.total_duration || 0 }} min</p>
        </div>
      </div>
      

      <div v-if="maintenanceList.length === 0" class="text-center text-gray-400 py-10">
        <p>No maintenance records found.</p>
      </div>
      <table v-else class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 text-gray-600 text-sm border-b">
            <th class="p-4 font-semibold">Robot ID</th>
            <th class="p-4 font-semibold">Type</th>
            <th class="p-4 font-semibold">Description</th>
            <th class="p-4 font-semibold">Cost</th>
            <th class="p-4 font-semibold">Duration</th>
            <th class="p-4 font-semibold">Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in maintenanceList" :key="m.id" class="hover:bg-gray-50 border-b last:border-b-0">
            <td class="p-4 text-gray-600">{{ m.robot_id }}</td>
            <td class="p-4"><span class="bg-gray-200 text-gray-700 px-2 py-1 rounded text-xs">{{ m.maintain_type }}</span></td>
            <td class="p-4 text-gray-800">{{ m.description }}</td>
            <td class="p-4 text-green-600 font-bold">¥{{ m.cost }}</td>
            <td class="p-4 text-gray-600">{{ m.duration }} min</td>
            <td class="p-4 text-gray-500 text-sm">{{ new Date(m.created_date).toLocaleDateString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 解决告警弹窗 -->
    <div v-if="isResolveModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
        <h3 class="text-xl font-bold text-gray-800 mb-4">Resolve Alert</h3>
        <p class="text-sm text-gray-500 mb-4">Robot #{{ currentAlert.robot_id }}: {{ currentAlert.message }}</p>
        <textarea v-model="resolveNote" rows="3" placeholder="Enter resolution note (e.g. Replaced battery)" class="w-full border rounded p-2 mb-4"></textarea>
        <div class="flex justify-end space-x-3">
          <button @click="isResolveModalOpen = false" class="px-4 py-2 border rounded">Cancel</button>
          <button @click="submitResolve" class="px-4 py-2 bg-blue-600 text-white rounded">Confirm Resolve</button>
        </div>
      </div>
    </div>

    <!-- 新增维修记录弹窗 -->
    <div v-if="isMaintModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
        <h3 class="text-xl font-bold text-gray-800 mb-4">Add Maintenance Record</h3>
        <form @submit.prevent="submitMaintenance">
          <div class="space-y-4">
            <div><label class="block text-sm text-gray-600 mb-1">Robot ID</label><input v-model="maintForm.robot_id" type="number" required class="w-full border rounded p-2"></div>
            <div>
              <label class="block text-sm text-gray-600 mb-1">Type</label>
              <select v-model="maintForm.maintain_type" class="w-full border rounded p-2">
                <option value="fault">Fault Repair</option>
                <option value="daily">Daily Maintenance</option>
                <option value="upgrade">Upgrade</option>
              </select>
            </div>
            <div><label class="block text-sm text-gray-600 mb-1">Description</label><textarea v-model="maintForm.description" required class="w-full border rounded p-2"></textarea></div>
            <div class="flex space-x-4">
              <div class="flex-1"><label class="block text-sm text-gray-600 mb-1">Cost (¥)</label><input v-model="maintForm.cost" type="number" step="0.1" required class="w-full border rounded p-2"></div>
              <div class="flex-1"><label class="block text-sm text-gray-600 mb-1">Duration (min)</label><input v-model="maintForm.duration" type="number" required class="w-full border rounded p-2"></div>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="isMaintModalOpen = false" class="px-4 py-2 border rounded">Cancel</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded">Save Record</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '../api'

const activeTab = ref('alerts')
const alerts = ref([])
const maintenanceList = ref([])
const stats = ref({})

// 弹窗状态
const isResolveModalOpen = ref(false)
const isMaintModalOpen = ref(false)
const currentAlert = ref({})
const resolveNote = ref('')
const maintForm = ref({ robot_id: '', maintain_type: 'fault', description: '', cost: 0, duration: 0 })

// 健壮的数据加载：分开写，防止某个接口报错连累全局
const loadData = async () => {
  try {
    // 1. 加载告警
    try {
      const alertRes = await api.get('/api/alert/')
      alerts.value = alertRes.data
    } catch (e) { 
      console.error("获取告警失败，请检查后端接口 /api/alert/ 是否正常", e) 
      alerts.value = []
    }

    // 2. 加载维修列表
    try {
      const maintRes = await api.get('/api/maintenance/')
      maintenanceList.value = maintRes.data
    } catch (e) { 
      console.error("获取维修列表失败", e) 
      maintenanceList.value = []
    }

    // 3. 加载维修统计
    try {
      const statsRes = await api.get('/api/maintenance/stats')
      stats.value = statsRes.data
    } catch (e) { 
      console.error("获取维修统计失败", e) 
      stats.value = {}
    }
  } catch (err) {
    console.error("加载数据通用错误", err)
  }
}

let timer = null
onMounted(() => {
  loadData()
  // 💡 进阶：加一个定时器，每 5 秒自动刷新一次数据，不用你每次都手动刷新页面了！
  timer = setInterval(loadData, 5000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

// 打开解决告警弹窗
const openResolveModal = (alert) => {
  currentAlert.value = alert
  resolveNote.value = ''
  isResolveModalOpen.value = true
}

// 提交解决告警
const submitResolve = async () => {
  try {
    await api.put(`/api/alert/${currentAlert.value.id}/resolve`, { resolve_note: resolveNote.value })
    isResolveModalOpen.value = false
    
    // 温馨引导：解决后自动跳转到维修记录 Tab
    alert('Alert resolved! Now, please add a maintenance record for this fix.')
    activeTab.value = 'maintenance'
    
    // 自动带出机器人ID和描述，方便你录入维修单
    maintForm.value.robot_id = currentAlert.value.robot_id 
    maintForm.value.description = `Fixed alert: ${currentAlert.value.message}`
    maintForm.value.cost = 0
    maintForm.value.duration = 0
    
    loadData() // 刷新列表
  } catch (err) { alert('Failed to resolve: ' + (err.response?.data?.detail || err.message)) }
}

// 打开维修弹窗
const openMaintModal = () => {
  maintForm.value = { robot_id: '', maintain_type: 'fault', description: '', cost: 0, duration: 0 }
  isMaintModalOpen.value = true
}

// 提交维修记录
const submitMaintenance = async () => {
  try {
    // 组装正确的请求数据，强制转换类型
    const payload = {
      robot_id: Number(maintForm.value.robot_id),
      maintain_type: maintForm.value.maintain_type,
      description: maintForm.value.description,
      cost: Number(maintForm.value.cost),
      duration: Number(maintForm.value.duration)
    }

    await api.post('/api/maintenance/', payload)
    isMaintModalOpen.value = false
    loadData()
  } catch (err) { 
    const errorMsg = JSON.stringify(err.response?.data?.detail) || err.message
    alert('Failed to save maintenance record: ' + errorMsg) 
  }
}


</script>
