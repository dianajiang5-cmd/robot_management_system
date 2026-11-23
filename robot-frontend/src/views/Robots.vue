<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative min-h-[600px]">
    <!-- 顶部 Tab 和 新增按钮 -->
    <div class="flex border-b border-gray-200 bg-gray-50 justify-between items-center pr-6">
      <div class="flex">
        <button @click="activeTab = 'robots'" :class="['py-4 px-8 font-semibold flex items-center transition-colors', activeTab === 'robots' ? 'text-blue-600 border-b-2 border-blue-600 bg-white' : 'text-gray-500 hover:text-gray-700']">
          <i class="fa-solid fa-robot mr-2"></i> Robots
        </button>
        <button @click="activeTab = 'sites'" :class="['py-4 px-8 font-semibold flex items-center transition-colors', activeTab === 'sites' ? 'text-blue-600 border-b-2 border-blue-600 bg-white' : 'text-gray-500 hover:text-gray-700']">
          <i class="fa-solid fa-building mr-2"></i> Sites
        </button>
      </div>
      <button @click="openModal('add', activeTab)" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm shadow transition">
        <i class="fa-solid fa-plus mr-1"></i> Add {{ activeTab === 'robots' ? 'Robot' : 'Site' }}
      </button>
    </div>

    <!-- 机器人列表 -->
    <div v-show="activeTab === 'robots'" class="p-6 overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 text-gray-600 text-sm border-b">
            <th class="p-4 font-semibold">ID</th>
            <th class="p-4 font-semibold">Name</th>
            <th class="p-4 font-semibold">Type</th>
            <th class="p-4 font-semibold">Status</th>
            <th class="p-4 font-semibold">IP Address</th>
            <th class="p-4 font-semibold text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="robot in robots" :key="robot.id" class="hover:bg-blue-50 transition-colors border-b last:border-b-0">
            <td class="p-4 text-gray-600">{{ robot.id }}</td>
            <td class="p-4 font-medium text-gray-800"><i class="fa-solid fa-microchip text-blue-400 mr-2"></i>{{ robot.name }}</td>
            <td class="p-4 text-gray-600">{{ robot.robot_type }}</td>
            <td class="p-4">
              <span :class="getStatusClass(robot.status)" class="px-3 py-1 rounded-full text-xs font-bold uppercase">{{ robot.status }}</span>
            </td>
            <td class="p-4 text-gray-600 font-mono text-sm">{{ robot.ip_address || '-' }}</td>
            <td class="p-4 text-right space-x-2">
              <button @click="openModal('detail', 'robots', robot)" class="text-blue-500 hover:text-blue-700" title="Detail"><i class="fa-solid fa-eye"></i></button>
              <button @click="openModal('edit', 'robots', robot)" class="text-yellow-500 hover:text-yellow-700" title="Edit"><i class="fa-solid fa-pen"></i></button>
              <button @click="deleteItem('robots', robot.id)" class="text-red-500 hover:text-red-700" title="Delete"><i class="fa-solid fa-trash"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 站点列表 -->
    <div v-show="activeTab === 'sites'" class="p-6 overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 text-gray-600 text-sm border-b">
            <th class="p-4 font-semibold">ID</th>
            <th class="p-4 font-semibold">Site Name</th>
            <th class="p-4 font-semibold">Location</th>
            <th class="p-4 font-semibold">Status</th>
            <th class="p-4 font-semibold text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="site in sites" :key="site.id" class="hover:bg-blue-50 transition-colors border-b last:border-b-0">
            <td class="p-4 text-gray-600">{{ site.id }}</td>
            <td class="p-4 font-medium text-gray-800"><i class="fa-solid fa-warehouse text-indigo-400 mr-2"></i>{{ site.site_name }}</td>
            <td class="p-4 text-gray-600">{{ site.location || 'Unknown' }}</td>
            <td class="p-4">
              <span :class="site.is_active ? 'text-green-600' : 'text-red-600'" class="font-semibold">
                {{ site.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="p-4 text-right space-x-2">
              <button @click="openModal('detail', 'sites', site)" class="text-blue-500 hover:text-blue-700"><i class="fa-solid fa-eye"></i></button>
              <button @click="openModal('edit', 'sites', site)" class="text-yellow-500 hover:text-yellow-700"><i class="fa-solid fa-pen"></i></button>
              <button @click="deleteItem('sites', site.id)" class="text-red-500 hover:text-red-700"><i class="fa-solid fa-trash"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 通用弹窗 (Modal) -->
    <div v-if="isModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-gray-800">{{ modalTitle }}</h3>
          <button @click="isModalOpen = false" class="text-gray-500 hover:text-red-500"><i class="fa-solid fa-xmark text-xl"></i></button>
        </div>

        <!-- 机器人表单 -->
        <form v-if="modalType === 'robots'" @submit.prevent="submitRobot">
          <div class="space-y-4">
            <div><label class="block text-sm text-gray-600 mb-1">Name</label><input v-model="formData.name" :disabled="isDetail" required class="w-full border rounded p-2"></div>
            <div><label class="block text-sm text-gray-600 mb-1">Type (e.g. delivery)</label><input v-model="formData.robot_type" :disabled="isDetail" required class="w-full border rounded p-2"></div>
            <div><label class="block text-sm text-gray-600 mb-1">Site ID</label><input v-model="formData.site_id" type="number" :disabled="isDetail" required class="w-full border rounded p-2"></div>
            <div><label class="block text-sm text-gray-600 mb-1">IP Address</label><input v-model="formData.ip_address" :disabled="isDetail" class="w-full border rounded p-2"></div>
            <div><label class="block text-sm text-gray-600 mb-1">Purchase Date</label><input v-model="formData.purchase_date" type="date" :disabled="isDetail" required class="w-full border rounded p-2"></div>
            <div><label class="block text-sm text-gray-600 mb-1">Warranty End</label><input v-model="formData.warranty_end_date" type="date" :disabled="isDetail" required class="w-full border rounded p-2"></div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="isModalOpen = false" class="px-4 py-2 border rounded hover:bg-gray-50">Close</button>
            <button v-if="!isDetail" type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Save</button>
          </div>
        </form>

        <!-- 站点表单 -->
        <form v-if="modalType === 'sites'" @submit.prevent="submitSite">
          <div class="space-y-4">
            <div><label class="block text-sm text-gray-600 mb-1">Site Name</label><input v-model="formData.site_name" :disabled="isDetail" required class="w-full border rounded p-2"></div>
            <div><label class="block text-sm text-gray-600 mb-1">Location</label><input v-model="formData.location" :disabled="isDetail" class="w-full border rounded p-2"></div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="isModalOpen = false" class="px-4 py-2 border rounded hover:bg-gray-50">Close</button>
            <button v-if="!isDetail" type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const activeTab = ref('robots')
const robots = ref([])
const sites = ref([])

// 弹窗控制
const isModalOpen = ref(false)
const modalTitle = ref('')
const modalType = ref('robots') // 'robots' or 'sites'
const isDetail = ref(false)
const formData = ref({})

const loadData = async () => {
  try {
    const [rRes, sRes] = await Promise.all([
      api.get('/api/robot/get_robot_list'),
      api.get('/api/site/')
    ])
    robots.value = rRes.data
    sites.value = sRes.data
  } catch (err) {
    console.error(err)
  }
}

onMounted(loadData)

const getStatusClass = (status) => {
  if (status === 'idle') return 'bg-green-100 text-green-700'
  if (status === 'working') return 'bg-blue-100 text-blue-700'
  return 'bg-gray-200 text-gray-700'
}

// 打开弹窗
const openModal = (action, type, item = null) => {
  modalType.value = type
  formData.value = item ? { ...item } : {}
  isDetail.value = action === 'detail'
  modalTitle.value = action === 'add' ? 'Add New' : action === 'edit' ? 'Edit' : 'Detail'
  isModalOpen.value = true
}

// 提交
const submitRobot = async () => {
  try {
    // 日期校验：防止用户漏填导致浏览器拦截或后端报错
    if (!formData.value.purchase_date || !formData.value.warranty_end_date) {
      alert('Please select both Purchase Date and Warranty End!')
      return
    }

    if (formData.value.id) {
      // 修改机器人 (你后端的 PUT /api/robot/{robot_id})
      await api.put(`/api/robot/${formData.value.id}`, formData.value)
    } else {
      // 新增机器人 (你后端的 POST /api/robot/)
      await api.post('/api/robot/', formData.value)
    }
    
    isModalOpen.value = false
    loadData() // 保存成功后刷新列表
  } catch (err) { 
    console.error(err)
    alert('Save failed: ' + (err.response?.data?.detail || err.message)) 
  }
}


const submitSite = async () => {
  try {
    if (formData.value.id) {
      await api.put(`/api/site/${formData.value.id}`, formData.value)
    } else {
      await api.post('/api/site/', formData.value)
    }
    isModalOpen.value = false
    loadData()
  } catch (err) { alert('Save failed: ' + (err.response?.data?.detail || err.message)) }
}

// 删除
const deleteItem = async (type, id) => {
  if (!confirm('Are you sure you want to delete this?')) return
  try {
    if (type === 'robots') await api.delete(`/api/robot/${id}`)
    else await api.delete(`/api/site/${id}`)
    loadData()
  } catch (err) { alert('Delete failed') }
}
</script>
