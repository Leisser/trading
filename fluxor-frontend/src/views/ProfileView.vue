<template>
  <div class="profile_container">
    <!-- Enhanced Header -->
    <header class="profile_header">
      <div class="header_content">
        <div class="header_left">
          <router-link to="/dashboard" class="back_btn">
            <svg class="back_icon" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
                clip-rule="evenodd"
              ></path>
            </svg>
            Back to Dashboard
          </router-link>
          <h1 class="header_title">Profile & Settings</h1>
        </div>
        <div class="header_right">
          <button
            @click="toggleTheme"
            class="action_btn theme_btn"
            :title="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
          >
            <svg
              v-if="theme === 'dark'"
              class="action_icon"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
            </svg>
            <svg v-else class="action_icon" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4.22 2.47a1 1 0 011.42 1.42l-.7.7a1 1 0 11-1.42-1.42l.7-.7zM18 9a1 1 0 100 2h-1a1 1 0 100-2h1zM5.64 4.22a1 1 0 00-1.42 1.42l.7.7a1 1 0 101.42-1.42l-.7-.7zM4 10a1 1 0 100 2H3a1 1 0 100-2h1zm1.64 7.78a1 1 0 001.42-1.42l-.7-.7a1 1 0 10-1.42 1.42l.7.7zM10 16a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zm7-6a7 7 0 11-14 0 7 7 0 0114 0z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
          <button @click="authStore.logout" class="logout_btn">
            <svg class="logout_icon" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                clip-rule="evenodd"
              ></path>
            </svg>
            Logout
          </button>
        </div>
      </div>
    </header>

    <div class="profile_content">
      <div class="profile_grid">
        <!-- Profile Information -->
        <div class="profile_main">
          <!-- User Profile Card -->
          <div class="profile_card">
            <div class="profile_header_section">
              <div class="profile_avatar">
                <svg class="avatar_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </div>
              <div class="profile_info">
                <h2 class="profile_name">{{ authStore.user?.full_name }}</h2>
                <p class="profile_email">{{ authStore.user?.email }}</p>
                <div class="profile_status">
                  <span class="status_badge" :class="kycStatusClass">
                    <svg class="status_icon" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clip-rule="evenodd"
                      ></path>
                    </svg>
                    {{ kycStatus }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Basic Profile Form -->
          <div class="form_section">
            <div class="section_header">
              <h3 class="section_title">Profile Information</h3>
              <p class="section_description">Update your personal information and preferences</p>
            </div>

            <form @submit.prevent="updateProfile" class="profile_form">
              <div class="form_grid">
                <div class="form_group">
                  <label class="form_label">
                    <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                        clip-rule="evenodd"
                      ></path>
                    </svg>
                    Full Name
                  </label>
                  <input
                    v-model="profileForm.full_name"
                    type="text"
                    class="form_input"
                    required
                    placeholder="Enter your full name"
                  />
                </div>

                <div class="form_group">
                  <label class="form_label">
                    <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"
                      ></path>
                      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path>
                    </svg>
                    Email Address
                  </label>
                  <input
                    v-model="profileForm.email"
                    type="email"
                    class="form_input disabled"
                    required
                    disabled
                    placeholder="your.email@example.com"
                  />
                </div>

                <div class="form_group">
                  <label class="form_label">
                    <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"
                      ></path>
                    </svg>
                    Phone Number
                  </label>
                  <input
                    v-model="profileForm.phone_number"
                    type="tel"
                    class="form_input"
                    placeholder="+1 (555) 123-4567"
                  />
                </div>

                <div class="form_group">
                  <label class="form_label">
                    <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                        clip-rule="evenodd"
                      ></path>
                    </svg>
                    Date of Birth
                  </label>
                  <input v-model="profileForm.date_of_birth" type="date" class="form_input" />
                </div>

                <div class="form_group">
                  <label class="form_label">
                    <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                        clip-rule="evenodd"
                      ></path>
                    </svg>
                    Country
                  </label>
                  <select v-model="profileForm.country" class="form_input">
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
              </div>

              <button type="submit" :disabled="loading" class="submit_btn">
                <span v-if="loading" class="loading_content">
                  <div class="loading_spinner"></div>
                  Updating Profile...
                </span>
                <span v-else class="btn_content">
                  <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                  Update Profile
                </span>
              </button>
            </form>
          </div>

          <!-- KYC Verification -->
          <div class="form_section">
            <div class="section_header">
              <h3 class="section_title">KYC Verification</h3>
              <p class="section_description">
                Complete your identity verification to unlock all features
              </p>
            </div>

            <div v-if="!authStore.user?.kyc_verified" class="kyc_form">
              <div class="kyc_steps">
                <div class="kyc_step">
                  <div class="step_icon">
                    <svg fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z"
                        clip-rule="evenodd"
                      ></path>
                    </svg>
                  </div>
                  <div class="step_content">
                    <h4 class="step_title">Government ID</h4>
                    <p class="step_description">Passport, Driver's License, or National ID</p>
                    <input
                      ref="idFile"
                      type="file"
                      accept="image/*,.pdf"
                      @change="handleFileUpload('id_document', $event)"
                      class="file_input"
                    />
                  </div>
                </div>

                <div class="kyc_step">
                  <div class="step_icon">
                    <svg fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                        clip-rule="evenodd"
                      ></path>
                    </svg>
                  </div>
                  <div class="step_content">
                    <h4 class="step_title">Proof of Address</h4>
                    <p class="step_description">Utility bill or bank statement</p>
                    <input
                      ref="addressFile"
                      type="file"
                      accept="image/*,.pdf"
                      @change="handleFileUpload('address_document', $event)"
                      class="file_input"
                    />
                  </div>
                </div>

                <div class="kyc_step">
                  <div class="step_icon">
                    <svg fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                        clip-rule="evenodd"
                      ></path>
                    </svg>
                  </div>
                  <div class="step_content">
                    <h4 class="step_title">Selfie with ID</h4>
                    <p class="step_description">Photo of yourself holding your ID</p>
                    <input
                      ref="selfieFile"
                      type="file"
                      accept="image/*"
                      @change="handleFileUpload('selfie', $event)"
                      class="file_input"
                    />
                  </div>
                </div>
              </div>

              <button
                @click="submitKYC"
                :disabled="
                  kycLoading ||
                  !kycFiles.id_document ||
                  !kycFiles.address_document ||
                  !kycFiles.selfie
                "
                class="kyc_submit_btn"
              >
                <span v-if="kycLoading" class="loading_content">
                  <div class="loading_spinner"></div>
                  Submitting KYC...
                </span>
                <span v-else class="btn_content">
                  <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                  Submit KYC
                </span>
              </button>
            </div>

            <div v-else class="kyc_verified">
              <div class="verified_icon">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </div>
              <h4 class="verified_title">KYC Verified</h4>
              <p class="verified_description">
                Your account has been verified successfully. You now have access to all trading
                features.
              </p>
            </div>
          </div>
        </div>

        <!-- Settings Sidebar -->
        <div class="settings_sidebar">
          <!-- Change Password -->
          <div class="settings_card">
            <div class="card_header">
              <h3 class="card_title">Change Password</h3>
              <svg class="card_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </div>

            <form @submit.prevent="changePassword" class="password_form">
              <div class="form_group">
                <label class="form_label">Current Password</label>
                <input
                  v-model="passwordForm.current_password"
                  type="password"
                  class="form_input"
                  required
                  placeholder="Enter current password"
                />
              </div>
              <div class="form_group">
                <label class="form_label">New Password</label>
                <input
                  v-model="passwordForm.new_password"
                  type="password"
                  class="form_input"
                  required
                  placeholder="Enter new password"
                />
              </div>
              <div class="form_group">
                <label class="form_label">Confirm Password</label>
                <input
                  v-model="passwordForm.confirm_password"
                  type="password"
                  class="form_input"
                  required
                  placeholder="Confirm new password"
                />
              </div>
              <button type="submit" :disabled="passwordLoading" class="settings_btn">
                <span v-if="passwordLoading" class="loading_content">
                  <div class="loading_spinner"></div>
                  Changing...
                </span>
                <span v-else>Change Password</span>
              </button>
            </form>
          </div>

          <!-- Notification Settings -->
          <div class="settings_card">
            <div class="card_header">
              <h3 class="card_title">Notifications</h3>
              <svg class="card_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"
                ></path>
              </svg>
            </div>

            <div class="settings_list">
              <div class="setting_item">
                <div class="setting_info">
                  <h4 class="setting_title">Email Notifications</h4>
                  <p class="setting_description">
                    Receive email alerts for trades and account activity
                  </p>
                </div>
                <label class="toggle_switch">
                  <input
                    v-model="settings.email_notifications"
                    type="checkbox"
                    class="toggle_input"
                  />
                  <span class="toggle_slider"></span>
                </label>
              </div>

              <div class="setting_item">
                <div class="setting_info">
                  <h4 class="setting_title">Trade Alerts</h4>
                  <p class="setting_description">Get notified when trades are executed</p>
                </div>
                <label class="toggle_switch">
                  <input v-model="settings.trade_alerts" type="checkbox" class="toggle_input" />
                  <span class="toggle_slider"></span>
                </label>
              </div>

              <div class="setting_item">
                <div class="setting_info">
                  <h4 class="setting_title">Price Alerts</h4>
                  <p class="setting_description">Receive alerts for significant price movements</p>
                </div>
                <label class="toggle_switch">
                  <input v-model="settings.price_alerts" type="checkbox" class="toggle_input" />
                  <span class="toggle_slider"></span>
                </label>
              </div>
            </div>

            <button @click="saveSettings" :disabled="settingsLoading" class="settings_btn">
              <span v-if="settingsLoading" class="loading_content">
                <div class="loading_spinner"></div>
                Saving...
              </span>
              <span v-else>Save Settings</span>
            </button>
          </div>

          <!-- Security Settings -->
          <div class="settings_card">
            <div class="card_header">
              <h3 class="card_title">Security</h3>
              <svg class="card_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </div>

            <div class="security_list">
              <div class="security_item">
                <div class="security_info">
                  <h4 class="security_title">Two-Factor Authentication</h4>
                  <p class="security_description">Add an extra layer of security</p>
                </div>
                <button class="security_btn">Enable</button>
              </div>

              <div class="security_item">
                <div class="security_info">
                  <h4 class="security_title">Login History</h4>
                  <p class="security_description">View recent login activity</p>
                </div>
                <button @click="showLoginHistory = true" class="security_btn">View</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Login History Modal -->
    <div v-if="showLoginHistory" class="modal_overlay" @click="showLoginHistory = false">
      <div class="modal_content" @click.stop>
        <div class="modal_header">
          <h3 class="modal_title">Login History</h3>
          <button @click="showLoginHistory = false" class="modal_close">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </button>
        </div>

        <div class="modal_body">
          <div class="login_history">
            <div v-for="login in loginHistory" :key="login.id" class="login_item">
              <div class="login_info">
                <div class="login_ip">{{ login.ip_address }}</div>
                <div class="login_time">{{ formatDate(login.timestamp) }}</div>
              </div>
              <div class="login_status">
                <svg class="status_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div class="modal_footer">
          <button @click="showLoginHistory = false" class="modal_btn">Close</button>
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

interface LoginHistory {
  id: number
  ip_address: string
  timestamp: string
}

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
  country: '',
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: '',
})

const settings = reactive({
  email_notifications: true,
  trade_alerts: true,
  price_alerts: false,
})

const kycFiles = reactive({
  id_document: null as File | null,
  address_document: null as File | null,
  selfie: null as File | null,
})

const loginHistory = ref<LoginHistory[]>([])

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
    await axios.patch('http://localhost:8000/api/user/', profileForm)
    await authStore.fetchUser()
    toast.showToast('Profile updated successfully!', 'success')
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to update profile'
    toast.showToast(errorMessage, 'error')
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
      new_password: passwordForm.new_password,
    })
    toast.showToast('Password changed successfully!', 'success')
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to change password'
    toast.showToast(errorMessage, 'error')
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
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    toast.showToast('KYC documents submitted successfully!', 'success')
    await authStore.fetchUser()
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to submit KYC'
    toast.showToast(errorMessage, 'error')
  } finally {
    kycLoading.value = false
  }
}

const saveSettings = async () => {
  settingsLoading.value = true
  try {
    await axios.patch('http://localhost:8000/api/user/settings/', settings)
    toast.showToast('Settings saved successfully!', 'success')
  } catch {
    toast.showToast('Failed to save settings', 'error')
  } finally {
    settingsLoading.value = false
  }
}

const fetchLoginHistory = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/login_history/')
    loginHistory.value = response.data.results || response.data
  } catch {
    loginHistory.value = []
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

// Theme functionality
const theme = ref('light')

const getCurrentTheme = () => {
  if (typeof window !== 'undefined') {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) return savedTheme

    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark'
    }
  }
  return 'light'
}

const setTheme = (value: string) => {
  theme.value = value
  document.documentElement.setAttribute('data_theme', value)
  localStorage.setItem('theme', value)
}

const toggleTheme = () => {
  setTheme(theme.value === 'dark' ? 'light' : 'dark')
}

// Initialize theme
onMounted(async () => {
  const currentTheme = getCurrentTheme()
  setTheme(currentTheme)

  // Listen for theme changes from other components
  const observer = new MutationObserver(() => {
    const newTheme = getCurrentTheme()
    if (newTheme !== theme.value) {
      theme.value = newTheme
    }
  })

  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data_theme'],
  })

  window.addEventListener('storage', () => {
    const newTheme = getCurrentTheme()
    if (newTheme !== theme.value) {
      theme.value = newTheme
    }
  })

  // Original profile initialization
  if (authStore.user) {
    profileForm.full_name = authStore.user.full_name
    profileForm.email = authStore.user.email
    // Load other profile data if available
  }
  await fetchLoginHistory()
})
</script>

<style scoped>
.profile_container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.profile_header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(229, 231, 235, 0.5);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.header_content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header_left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.back_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  text-decoration: none;
  transition: all 0.2s ease;
}

.back_btn:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.back_icon {
  width: 1rem;
  height: 1rem;
}

.header_title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1f2937;
  margin: 0;
  letter-spacing: -0.025em;
}

.header_right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.action_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  text-decoration: none;
  transition: all 0.2s ease;
  background: rgba(229, 231, 235, 0.5);
  border: 1px solid rgba(229, 231, 235, 0.5);
}

.action_btn:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border-color: rgba(59, 130, 246, 0.2);
}

.action_icon {
  width: 1rem;
  height: 1rem;
}

.theme_btn {
  background: rgba(229, 231, 235, 0.5);
  border: 1px solid rgba(229, 231, 235, 0.5);
  color: #6b7280;
}

.theme_btn:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border-color: rgba(59, 130, 246, 0.2);
}

.logout_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #ef4444;
  transition: all 0.2s ease;
  cursor: pointer;
}

.logout_btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.3);
}

.logout_icon {
  width: 1rem;
  height: 1rem;
}

.profile_content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.profile_grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.profile_main {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile_card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.profile_header_section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.profile_avatar {
  width: 4rem;
  height: 4rem;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.avatar_icon {
  width: 2rem;
  height: 2rem;
}

.profile_info {
  flex: 1;
}

.profile_name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.profile_email {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.75rem;
}

.profile_status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status_badge {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status_badge.bg-green-100 {
  background: rgba(34, 197, 94, 0.1);
  color: #059669;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.status_badge.bg-yellow-100 {
  background: rgba(245, 158, 11, 0.1);
  color: #d97706;
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.status_icon {
  width: 0.875rem;
  height: 0.875rem;
}

.form_section {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.section_header {
  margin-bottom: 2rem;
}

.section_title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.section_description {
  color: #6b7280;
  font-size: 0.875rem;
}

.profile_form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.form_group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form_label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.label_icon {
  width: 1rem;
  height: 1rem;
  color: #6b7280;
}

.form_input {
  padding: 0.75rem 1rem;
  border: 2px solid rgba(229, 231, 235, 0.5);
  border-radius: 8px;
  font-size: 0.875rem;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.2s ease;
  color: #1f2937;
}

.form_input::placeholder {
  color: #9ca3af;
}

.form_input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form_input.disabled {
  background: rgba(249, 250, 251, 0.8);
  color: #6b7280;
  cursor: not-allowed;
}

.submit_btn {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  align-self: flex-start;
}

.submit_btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px -3px rgba(59, 130, 246, 0.4);
}

.submit_btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading_content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn_content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.loading_spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.btn_icon {
  width: 1.25rem;
  height: 1.25rem;
}

.kyc_form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.kyc_steps {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.kyc_step {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(59, 130, 246, 0.05);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 12px;
}

.step_icon {
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.step_content {
  flex: 1;
}

.step_title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.step_description {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 1rem;
}

.file_input {
  width: 100%;
  padding: 0.75rem;
  border: 2px dashed rgba(59, 130, 246, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.5);
  transition: all 0.2s ease;
  cursor: pointer;
}

.file_input:hover {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
}

.kyc_submit_btn {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #059669, #10b981);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  align-self: flex-start;
}

.kyc_submit_btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px -3px rgba(5, 150, 105, 0.4);
}

.kyc_submit_btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.kyc_verified {
  text-align: center;
  padding: 3rem 2rem;
}

.verified_icon {
  width: 4rem;
  height: 4rem;
  background: linear-gradient(135deg, #059669, #10b981);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 1.5rem;
}

.verified_title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #059669;
  margin-bottom: 0.5rem;
}

.verified_description {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
}

.settings_sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.settings_card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.card_header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.card_title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.card_icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #6b7280;
}

.password_form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.settings_list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.setting_item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.setting_info {
  flex: 1;
}

.setting_title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.25rem;
}

.setting_description {
  font-size: 0.75rem;
  color: #6b7280;
}

.toggle_switch {
  position: relative;
  display: inline-block;
  width: 3rem;
  height: 1.5rem;
  cursor: pointer;
}

.toggle_input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle_slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #d1d5db;
  transition: 0.3s;
  border-radius: 1.5rem;
}

.toggle_slider:before {
  position: absolute;
  content: '';
  height: 1.125rem;
  width: 1.125rem;
  left: 0.1875rem;
  bottom: 0.1875rem;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

.toggle_input:checked + .toggle_slider {
  background-color: #3b82f6;
}

.toggle_input:checked + .toggle_slider:before {
  transform: translateX(1.5rem);
}

.settings_btn {
  width: 100%;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.settings_btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.settings_btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.security_list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.security_item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.security_info {
  flex: 1;
}

.security_title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.25rem;
}

.security_description {
  font-size: 0.75rem;
  color: #6b7280;
}

.security_btn {
  padding: 0.5rem 1rem;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 6px;
  color: #3b82f6;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.security_btn:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.3);
}

.modal_overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal_content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  width: 100%;
  max-width: 500px;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal_header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(229, 231, 235, 0.5);
}

.modal_title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.modal_close {
  width: 2rem;
  height: 2rem;
  border-radius: 6px;
  border: 1px solid rgba(229, 231, 235, 0.5);
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal_close:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
}

.modal_body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.login_history {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.login_item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: rgba(249, 250, 251, 0.5);
  border-radius: 8px;
  border: 1px solid rgba(229, 231, 235, 0.5);
}

.login_info {
  flex: 1;
}

.login_ip {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.25rem;
}

.login_time {
  font-size: 0.75rem;
  color: #6b7280;
}

.login_status {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background: rgba(34, 197, 94, 0.1);
  border-radius: 50%;
  color: #059669;
}

.modal_footer {
  padding: 1.5rem;
  border-top: 1px solid rgba(229, 231, 235, 0.5);
  display: flex;
  justify-content: flex-end;
}

.modal_btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal_btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

@media (max-width: 1024px) {
  .profile_grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .form_grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .profile_content {
    padding: 1rem;
  }

  .header_content {
    padding: 0 1rem;
  }

  .header_left {
    gap: 1rem;
  }

  .header_title {
    font-size: 1.5rem;
  }

  .profile_header_section {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .form_section,
  .profile_card,
  .settings_card {
    padding: 1.5rem;
  }

  .kyc_step {
    flex-direction: column;
    text-align: center;
  }

  .step_icon {
    align-self: center;
  }
}

/* Dark mode support */
[data_theme='dark'] .profile_container {
  background: #111827;
  color: #f9fafb;
}

[data_theme='dark'] .profile_header {
  background: linear-gradient(135deg, #1f2937, #374151);
  border-bottom: 1px solid #374151;
}

[data_theme='dark'] .header_title {
  color: #f9fafb;
}

[data_theme='dark'] .back_btn {
  color: #9ca3af;
}

[data_theme='dark'] .back_btn:hover {
  color: #f9fafb;
}

[data_theme='dark'] .profile_card {
  background: #1f2937;
  border: 1px solid #374151;
}

[data_theme='dark'] .profile_name {
  color: #f9fafb;
}

[data_theme='dark'] .profile_email {
  color: #9ca3af;
}

[data_theme='dark'] .form_section {
  background: #1f2937;
  border: 1px solid #374151;
}

[data_theme='dark'] .section_title {
  color: #f9fafb;
}

[data_theme='dark'] .section_description {
  color: #9ca3af;
}

[data_theme='dark'] .form_label {
  color: #9ca3af;
}

[data_theme='dark'] .form_input {
  background: #374151;
  border-color: #4b5563;
  color: #f9fafb;
}

[data_theme='dark'] .form_input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

[data_theme='dark'] .form_input::placeholder {
  color: #9ca3af;
}

[data_theme='dark'] .form_input.disabled {
  background: #4b5563;
  color: #9ca3af;
}

[data_theme='dark'] .submit_btn {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
}

[data_theme='dark'] .kyc_form {
  background: #1f2937;
  border: 1px solid #374151;
}

[data_theme='dark'] .kyc_step {
  border-bottom-color: #374151;
}

[data_theme='dark'] .step_title {
  color: #f9fafb;
}

[data_theme='dark'] .step_description {
  color: #9ca3af;
}

[data_theme='dark'] .file_input {
  background: #374151;
  border-color: #4b5563;
  color: #f9fafb;
}

[data_theme='dark'] .file_input:hover {
  border-color: #3b82f6;
}

[data_theme='dark'] .settings_card {
  background: #1f2937;
  border: 1px solid #374151;
}

[data_theme='dark'] .setting_item {
  border-bottom-color: #374151;
}

[data_theme='dark'] .setting_label {
  color: #f9fafb;
}

[data_theme='dark'] .setting_description {
  color: #9ca3af;
}

[data_theme='dark'] .toggle_switch {
  background: #4b5563;
}

[data_theme='dark'] .toggle_switch.active {
  background: #3b82f6;
}

[data_theme='dark'] .toggle_thumb {
  background: #9ca3af;
}

[data_theme='dark'] .toggle_switch.active .toggle_thumb {
  background: white;
}

[data_theme='dark'] .security_btn {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.3);
  color: #3b82f6;
}

[data_theme='dark'] .modal_content {
  background: #1f2937;
  border: 1px solid #374151;
}

[data_theme='dark'] .modal_title {
  color: #f9fafb;
}

[data_theme='dark'] .modal_header {
  border-bottom-color: #374151;
}

[data_theme='dark'] .modal_close {
  background: #374151;
  border-color: #4b5563;
  color: #9ca3af;
}

[data_theme='dark'] .modal_close:hover {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

[data_theme='dark'] .modal_footer {
  border-top-color: #374151;
}

[data_theme='dark'] .login_item {
  background: #374151;
  border-color: #4b5563;
}

[data_theme='dark'] .login_ip {
  color: #f9fafb;
}

[data_theme='dark'] .login_time {
  color: #9ca3af;
}

[data_theme='dark'] .action_btn {
  background: rgba(75, 85, 99, 0.5);
  border-color: rgba(75, 85, 99, 0.5);
  color: #9ca3af;
}

[data_theme='dark'] .action_btn:hover {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border-color: rgba(59, 130, 246, 0.3);
}

[data_theme='dark'] .theme_btn {
  background: rgba(75, 85, 99, 0.5);
  border-color: rgba(75, 85, 99, 0.5);
  color: #9ca3af;
}

[data_theme='dark'] .theme_btn:hover {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border-color: rgba(59, 130, 246, 0.3);
}
</style>
