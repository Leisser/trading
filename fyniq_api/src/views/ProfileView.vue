<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900">Profile & Settings</h1>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/dashboard" class="btn-secondary text-sm">Back to Dashboard</router-link>
            <button @click="authStore.logout" class="btn-secondary text-sm">Logout</button>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Profile Information -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Basic Profile -->
          <div class="card">
            <h2 class="text-lg font-medium text-gray-900 mb-4">Profile Information</h2>
            <form @submit.prevent="updateProfile" class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Full Name</label>
                  <input
                    v-model="profileForm.full_name"
                    type="text"
                    class="input-field"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Email</label>
                  <input
                    v-model="profileForm.email"
                    type="email"
                    class="input-field"
                    required
                    disabled
                  />
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Phone Number</label>
                <input
                  v-model="profileForm.phone_number"
                  type="tel"
                  class="input-field"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Date of Birth</label>
                <input
                  v-model="profileForm.date_of_birth"
                  type="date"
                  class="input-field"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Country</label>
                <select v-model="profileForm.country" class="input-field">
                  <option value="">Select Country</option>
                  <option value="US">United States</option>
                  <option value="UK">United Kingdom</option>
                  <option value="CA">Canada</option>
                  <option value="AU">Australia</option>
                  <option value="DE">Germany</option>
                  <option value="FR">France</option>
                  <option value="JP">Japan</option>
                  <option value="SG">Singapore</option>
                  <option value="KE">Kenya</option>
                </select>
              </div>
              <button type="submit" :disabled="loading" class="btn-primary">
                <span v-if="loading">Updating...</span>
                <span v-else>Update Profile</span>
              </button>
            </form>
          </div>

          <!-- KYC Verification -->
          <div class="card">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg font-medium text-gray-900">KYC Verification</h2>
              <span :class="kycStatusClass" class="px-2 py-1 text-xs font-semibold rounded-full">
                {{ kycStatus }}
              </span>
            </div>
            
            <div v-if="!authStore.user?.kyc_verified" class="space-y-4">
              <p class="text-sm text-gray-600">
                Please upload the following documents to complete your KYC verification:
              </p>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Government ID (Passport/Driver's License)</label>
                  <input
                    ref="idFile"
                    type="file"
                    accept="image/*,.pdf"
                    @change="handleFileUpload('id_document', $event)"
                    class="input-field"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Proof of Address (Utility Bill/Bank Statement)</label>
                  <input
                    ref="addressFile"
                    type="file"
                    accept="image/*,.pdf"
                    @change="handleFileUpload('address_document', $event)"
                    class="input-field"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Selfie with ID</label>
                  <input
                    ref="selfieFile"
                    type="file"
                    accept="image/*"
                    @change="handleFileUpload('selfie', $event)"
                    class="input-field"
                  />
                </div>
              </div>
              
              <button @click="submitKYC" :disabled="kycLoading || !kycFiles.id_document || !kycFiles.address_document || !kycFiles.selfie" class="btn-primary">
                <span v-if="kycLoading">Submitting...</span>
                <span v-else>Submit KYC</span>
              </button>
            </div>
            
            <div v-else class="text-center py-4">
              <div class="text-green-600 text-lg mb-2">✓ KYC Verified</div>
              <p class="text-sm text-gray-600">Your account has been verified successfully.</p>
            </div>
          </div>
        </div>

        <!-- Settings Sidebar -->
        <div class="space-y-6">
          <!-- Change Password -->
          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Change Password</h3>
            <form @submit.prevent="changePassword" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Current Password</label>
                <input
                  v-model="passwordForm.current_password"
                  type="password"
                  class="input-field"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">New Password</label>
                <input
                  v-model="passwordForm.new_password"
                  type="password"
                  class="input-field"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Confirm New Password</label>
                <input
                  v-model="passwordForm.confirm_password"
                  type="password"
                  class="input-field"
                  required
                />
              </div>
              <button type="submit" :disabled="passwordLoading" class="btn-primary w-full">
                <span v-if="passwordLoading">Changing...</span>
                <span v-else>Change Password</span>
              </button>
            </form>
          </div>

          <!-- Notification Settings -->
          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Notification Settings</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-700">Email Notifications</p>
                  <p class="text-xs text-gray-500">Receive email alerts for trades and account activity</p>
                </div>
                <input
                  v-model="settings.email_notifications"
                  type="checkbox"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
              </div>
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-700">Trade Alerts</p>
                  <p class="text-xs text-gray-500">Get notified when trades are executed</p>
                </div>
                <input
                  v-model="settings.trade_alerts"
                  type="checkbox"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
              </div>
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-700">Price Alerts</p>
                  <p class="text-xs text-gray-500">Receive alerts for significant price movements</p>
                </div>
                <input
                  v-model="settings.price_alerts"
                  type="checkbox"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
              </div>
              <button @click="saveSettings" :disabled="settingsLoading" class="btn-primary w-full">
                <span v-if="settingsLoading">Saving...</span>
                <span v-else>Save Settings</span>
              </button>
            </div>
          </div>

          <!-- Security Settings -->
          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Security</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-700">Two-Factor Authentication</p>
                  <p class="text-xs text-gray-500">Add an extra layer of security</p>
                </div>
                <button class="btn-secondary text-sm">Enable</button>
              </div>
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-700">Login History</p>
                  <p class="text-xs text-gray-500">View recent login activity</p>
                </div>
                <button @click="showLoginHistory = true" class="btn-secondary text-sm">View</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Login History Modal -->
    <div v-if="showLoginHistory" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Login History</h3>
          <div class="max-h-64 overflow-y-auto space-y-2">
            <div v-for="login in loginHistory" :key="login.id" class="text-sm border-b pb-2">
              <p class="font-medium">{{ login.ip_address }}</p>
              <p class="text-gray-500">{{ formatDate(login.timestamp) }}</p>
            </div>
          </div>
          <button @click="showLoginHistory = false" class="btn-primary w-full mt-4">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import axios from 'axios'

const authStore = useAuthStore()
const toast = useToast()

const loading = ref(false)
const kycLoading = ref(false)
const passwordLoading = ref(false)
const settingsLoading = ref(false)
const showLoginHistory = ref(false)

const profileForm = reactive({
  full_name: '',
  email: '',
  phone_number: '',
  date_of_birth: '',
  country: ''
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const settings = reactive({
  email_notifications: true,
  trade_alerts: true,
  price_alerts: false
})

const kycFiles = reactive({
  id_document: null as File | null,
  address_document: null as File | null,
  selfie: null as File | null
})

const loginHistory = ref<any[]>([])

const kycStatus = computed(() => {
  return authStore.user?.kyc_verified ? 'Verified' : 'Pending'
})

const kycStatusClass = computed(() => {
  return authStore.user?.kyc_verified 
    ? 'bg-green-100 text-green-800' 
    : 'bg-yellow-100 text-yellow-800'
})

const updateProfile = async () => {
  loading.value = true
  try {
    const response = await axios.patch('http://localhost:8000/api/user/', profileForm)
    await authStore.fetchUser()
    toast.showToast('Profile updated successfully!', 'success')
  } catch (error: any) {
    toast.showToast(error.response?.data?.detail || 'Failed to update profile', 'error')
  } finally {
    loading.value = false
  }
}

const changePassword = async () => {
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    toast.showToast('New passwords do not match', 'error')
    return
  }
  
  passwordLoading.value = true
  try {
    await axios.post('http://localhost:8000/api/change_password/', {
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password
    })
    toast.showToast('Password changed successfully!', 'success')
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (error: any) {
    toast.showToast(error.response?.data?.detail || 'Failed to change password', 'error')
  } finally {
    passwordLoading.value = false
  }
}

const handleFileUpload = (type: string, event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    kycFiles[type as keyof typeof kycFiles] = target.files[0]
  }
}

const submitKYC = async () => {
  kycLoading.value = true
  try {
    const formData = new FormData()
    if (kycFiles.id_document) formData.append('id_document', kycFiles.id_document)
    if (kycFiles.address_document) formData.append('address_document', kycFiles.address_document)
    if (kycFiles.selfie) formData.append('selfie', kycFiles.selfie)
    
    await axios.post('http://localhost:8000/api/kyc_upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    toast.showToast('KYC documents submitted successfully!', 'success')
    await authStore.fetchUser()
  } catch (error: any) {
    toast.showToast(error.response?.data?.detail || 'Failed to submit KYC', 'error')
  } finally {
    kycLoading.value = false
  }
}

const saveSettings = async () => {
  settingsLoading.value = true
  try {
    await axios.patch('http://localhost:8000/api/user/settings/', settings)
    toast.showToast('Settings saved successfully!', 'success')
  } catch (error: any) {
    toast.showToast('Failed to save settings', 'error')
  } finally {
    settingsLoading.value = false
  }
}

const fetchLoginHistory = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/login_history/')
    loginHistory.value = response.data.results || response.data
  } catch (error) {
    loginHistory.value = []
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

onMounted(async () => {
  if (authStore.user) {
    profileForm.full_name = authStore.user.full_name
    profileForm.email = authStore.user.email
    // Load other profile data if available
  }
  await fetchLoginHistory()
})
</script> 