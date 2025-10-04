<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Header -->
      <div class="text-center">
        <div class="flex justify-center">
          <div class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-gradient-to-r from-primary-600 to-primary-800 rounded-lg"></div>
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Fluxor Trading</h1>
          </div>
        </div>
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900 dark:text-white">
          Sign in to your account
        </h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Or
          <router-link 
            to="/register" 
            class="font-medium text-primary-600 hover:text-primary-500"
          >
            create a new account
          </router-link>
        </p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleSubmit" class="mt-8 space-y-6">
        <div class="space-y-4">
          <!-- Email -->
          <div>
            <label for="email" class="form-label">
              Email address
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              autocomplete="email"
              class="form-input"
              :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': errors.email }"
              placeholder="Enter your email"
            />
            <p v-if="errors.email" class="mt-1 text-sm text-red-600">
              {{ errors.email }}
            </p>
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="form-label">
              Password
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="current-password"
                class="form-input pr-10"
                :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': errors.password }"
                placeholder="Enter your password"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <EyeIcon v-if="!showPassword" class="h-5 w-5 text-gray-400" />
                <EyeSlashIcon v-else class="h-5 w-5 text-gray-400" />
              </button>
            </div>
            <p v-if="errors.password" class="mt-1 text-sm text-red-600">
              {{ errors.password }}
            </p>
          </div>

          <!-- 2FA Code (shown if required) -->
          <div v-if="show2FA" class="space-y-2">
            <label for="twoFactorCode" class="form-label">
              Two-Factor Authentication Code
            </label>
            <input
              id="twoFactorCode"
              v-model="form.twoFactorCode"
              type="text"
              maxlength="6"
              placeholder="000000"
              class="form-input text-center text-lg tracking-widest"
              :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': errors.twoFactorCode }"
            />
            <p class="text-xs text-gray-500 text-center">
              Enter the 6-digit code from your authenticator app
            </p>
            <p v-if="errors.twoFactorCode" class="mt-1 text-sm text-red-600 text-center">
              {{ errors.twoFactorCode }}
            </p>
          </div>
        </div>

        <!-- Remember me and Forgot password -->
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              v-model="form.rememberMe"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label for="remember-me" class="ml-2 block text-sm text-gray-900 dark:text-gray-300">
              Remember me
            </label>
          </div>

          <div class="text-sm">
            <router-link 
              to="/forgot-password" 
              class="font-medium text-primary-600 hover:text-primary-500"
            >
              Forgot your password?
            </router-link>
          </div>
        </div>

        <!-- Submit Button -->
        <div>
          <button
            type="submit"
            :disabled="isLoading"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            <span v-if="isLoading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ show2FA ? 'Verifying...' : 'Signing in...' }}
            </span>
            <span v-else>
              {{ show2FA ? 'Verify & Sign in' : 'Sign in' }}
            </span>
          </button>
        </div>

        <!-- Back to password (if 2FA is shown) -->
        <div v-if="show2FA" class="text-center">
          <button
            type="button"
            @click="reset2FA"
            class="text-sm font-medium text-primary-600 hover:text-primary-500"
          >
            ← Back to password
          </button>
        </div>

        <!-- Demo Credentials -->
        <div v-if="showDemoCredentials" class="mt-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Demo Credentials:</h4>
          <div class="space-y-1 text-xs text-gray-600 dark:text-gray-400">
            <div>Email: demo@example.com</div>
            <div>Password: demo123</div>
          </div>
          <button
            type="button"
            @click="fillDemoCredentials"
            class="mt-2 text-xs font-medium text-primary-600 hover:text-primary-500"
          >
            Fill demo credentials
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline'

// Store
const authStore = useAuthStore()

// State
const isLoading = ref(false)
const showPassword = ref(false)
const show2FA = ref(false)
const showDemoCredentials = ref(true)

const form = reactive({
  email: '',
  password: '',
  twoFactorCode: '',
  rememberMe: false
})

const errors = reactive({
  email: '',
  password: '',
  twoFactorCode: ''
})

// Methods
const validateForm = () => {
  // Reset errors
  Object.keys(errors).forEach(key => {
    errors[key as keyof typeof errors] = ''
  })
  
  let isValid = true
  
  // Email validation
  if (!form.email) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Please enter a valid email address'
    isValid = false
  }
  
  // Password validation
  if (!form.password) {
    errors.password = 'Password is required'
    isValid = false
  } else if (form.password.length < 6) {
    errors.password = 'Password must be at least 6 characters'
    isValid = false
  }
  
  // 2FA validation (if shown)
  if (show2FA.value) {
    if (!form.twoFactorCode) {
      errors.twoFactorCode = '2FA code is required'
      isValid = false
    } else if (!/^\d{6}$/.test(form.twoFactorCode)) {
      errors.twoFactorCode = 'Please enter a valid 6-digit code'
      isValid = false
    }
  }
  
  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  isLoading.value = true
  
  try {
    await authStore.login({
      email: form.email,
      password: form.password,
      two_factor_code: show2FA.value ? form.twoFactorCode : undefined
    })
  } catch (error: any) {
    console.error('Login error:', error)
    
    // Check if 2FA is required
    if (error.response?.status === 400 && error.response?.data?.require_2fa) {
      show2FA.value = true
      errors.twoFactorCode = ''
    }
  } finally {
    isLoading.value = false
  }
}

const reset2FA = () => {
  show2FA.value = false
  form.twoFactorCode = ''
  errors.twoFactorCode = ''
}

const fillDemoCredentials = () => {
  form.email = 'demo@example.com'
  form.password = 'demo123'
}

// Lifecycle
onMounted(() => {
  // Auto-focus email field
  const emailInput = document.getElementById('email')
  if (emailInput) {
    emailInput.focus()
  }
})
</script>

<style scoped>
/* Custom input styles for 2FA */
input[type="text"][maxlength="6"] {
  letter-spacing: 0.5em;
}
</style>