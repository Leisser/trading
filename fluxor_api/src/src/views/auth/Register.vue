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
          Create your account
        </h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Or
          <router-link 
            to="/login" 
            class="font-medium text-primary-600 hover:text-primary-500"
          >
            sign in to your existing account
          </router-link>
        </p>
      </div>

      <!-- Registration Form -->
      <form @submit.prevent="handleSubmit" class="mt-8 space-y-6">
        <div class="space-y-4">
          <!-- Full Name -->
          <div>
            <label for="fullName" class="form-label">
              Full Name
            </label>
            <input
              id="fullName"
              v-model="form.fullName"
              type="text"
              required
              autocomplete="name"
              class="form-input"
              :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': errors.fullName }"
              placeholder="Enter your full name"
            />
            <p v-if="errors.fullName" class="mt-1 text-sm text-red-600">
              {{ errors.fullName }}
            </p>
          </div>

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
                autocomplete="new-password"
                class="form-input pr-10"
                :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': errors.password }"
                placeholder="Create a strong password"
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
            <div class="mt-2 space-y-1">
              <div class="flex items-center text-xs" :class="passwordChecks.length ? 'text-green-600' : 'text-gray-400'">
                <CheckCircleIcon v-if="passwordChecks.length" class="h-3 w-3 mr-1" />
                <div v-else class="h-3 w-3 mr-1 border border-gray-300 rounded-full"></div>
                At least 8 characters
              </div>
              <div class="flex items-center text-xs" :class="passwordChecks.uppercase ? 'text-green-600' : 'text-gray-400'">
                <CheckCircleIcon v-if="passwordChecks.uppercase" class="h-3 w-3 mr-1" />
                <div v-else class="h-3 w-3 mr-1 border border-gray-300 rounded-full"></div>
                One uppercase letter
              </div>
              <div class="flex items-center text-xs" :class="passwordChecks.lowercase ? 'text-green-600' : 'text-gray-400'">
                <CheckCircleIcon v-if="passwordChecks.lowercase" class="h-3 w-3 mr-1" />
                <div v-else class="h-3 w-3 mr-1 border border-gray-300 rounded-full"></div>
                One lowercase letter
              </div>
              <div class="flex items-center text-xs" :class="passwordChecks.number ? 'text-green-600' : 'text-gray-400'">
                <CheckCircleIcon v-if="passwordChecks.number" class="h-3 w-3 mr-1" />
                <div v-else class="h-3 w-3 mr-1 border border-gray-300 rounded-full"></div>
                One number
              </div>
            </div>
            <p v-if="errors.password" class="mt-1 text-sm text-red-600">
              {{ errors.password }}
            </p>
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirmPassword" class="form-label">
              Confirm Password
            </label>
            <div class="relative">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                required
                autocomplete="new-password"
                class="form-input pr-10"
                :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': errors.confirmPassword }"
                placeholder="Confirm your password"
              />
              <button
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <EyeIcon v-if="!showConfirmPassword" class="h-5 w-5 text-gray-400" />
                <EyeSlashIcon v-else class="h-5 w-5 text-gray-400" />
              </button>
            </div>
            <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-600">
              {{ errors.confirmPassword }}
            </p>
          </div>
        </div>

        <!-- Terms and Privacy -->
        <div class="space-y-4">
          <div class="flex items-start">
            <input
              id="agreeTerms"
              v-model="form.agreeTerms"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded mt-1"
            />
            <label for="agreeTerms" class="ml-2 block text-sm text-gray-900 dark:text-gray-300">
              I agree to the 
              <a href="#" class="font-medium text-primary-600 hover:text-primary-500">
                Terms of Service
              </a> 
              and 
              <a href="#" class="font-medium text-primary-600 hover:text-primary-500">
                Privacy Policy
              </a>
            </label>
          </div>
          <p v-if="errors.agreeTerms" class="text-sm text-red-600">
            {{ errors.agreeTerms }}
          </p>

          <div class="flex items-start">
            <input
              id="agreeRisk"
              v-model="form.agreeRisk"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded mt-1"
            />
            <label for="agreeRisk" class="ml-2 block text-sm text-gray-900 dark:text-gray-300">
              I understand that trading involves substantial risk and I may lose all of my investment
            </label>
          </div>
          <p v-if="errors.agreeRisk" class="text-sm text-red-600">
            {{ errors.agreeRisk }}
          </p>

          <div class="flex items-start">
            <input
              id="emailNotifications"
              v-model="form.emailNotifications"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded mt-1"
            />
            <label for="emailNotifications" class="ml-2 block text-sm text-gray-900 dark:text-gray-300">
              I would like to receive email notifications about account activity and market updates (optional)
            </label>
          </div>
        </div>

        <!-- Submit Button -->
        <div>
          <button
            type="submit"
            :disabled="isLoading || !isFormValid"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            <span v-if="isLoading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating account...
            </span>
            <span v-else>
              Create Account
            </span>
          </button>
        </div>

        <!-- Password Strength Indicator -->
        <div v-if="form.password" class="mt-4">
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-600 dark:text-gray-400">Password strength:</span>
            <span :class="passwordStrengthColor">{{ passwordStrengthText }}</span>
          </div>
          <div class="mt-1 w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="passwordStrengthColor"
              :style="{ width: `${passwordStrengthPercentage}%` }"
            ></div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { EyeIcon, EyeSlashIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'

// Store
const authStore = useAuthStore()

// State
const isLoading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const form = reactive({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false,
  agreeRisk: false,
  emailNotifications: false
})

const errors = reactive({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreeTerms: '',
  agreeRisk: ''
})

// Computed
const passwordChecks = computed(() => ({
  length: form.password.length >= 8,
  uppercase: /[A-Z]/.test(form.password),
  lowercase: /[a-z]/.test(form.password),
  number: /\d/.test(form.password)
}))

const passwordStrengthScore = computed(() => {
  let score = 0
  if (passwordChecks.value.length) score++
  if (passwordChecks.value.uppercase) score++
  if (passwordChecks.value.lowercase) score++
  if (passwordChecks.value.number) score++
  if (form.password.length >= 12) score++
  if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(form.password)) score++
  return Math.min(score, 4)
})

const passwordStrengthPercentage = computed(() => {
  return (passwordStrengthScore.value / 4) * 100
})

const passwordStrengthText = computed(() => {
  const score = passwordStrengthScore.value
  if (score === 0) return 'Very Weak'
  if (score === 1) return 'Weak'
  if (score === 2) return 'Fair'
  if (score === 3) return 'Good'
  return 'Strong'
})

const passwordStrengthColor = computed(() => {
  const score = passwordStrengthScore.value
  if (score === 0) return 'text-red-600 bg-red-600'
  if (score === 1) return 'text-red-500 bg-red-500'
  if (score === 2) return 'text-yellow-500 bg-yellow-500'
  if (score === 3) return 'text-blue-500 bg-blue-500'
  return 'text-green-600 bg-green-600'
})

const isFormValid = computed(() => {
  return form.fullName && 
         form.email && 
         form.password && 
         form.confirmPassword && 
         form.agreeTerms && 
         form.agreeRisk &&
         Object.values(passwordChecks.value).every(check => check) &&
         form.password === form.confirmPassword
})

// Methods
const validateForm = () => {
  // Reset errors
  Object.keys(errors).forEach(key => {
    errors[key as keyof typeof errors] = ''
  })
  
  let isValid = true
  
  // Full name validation
  if (!form.fullName) {
    errors.fullName = 'Full name is required'
    isValid = false
  } else if (form.fullName.length < 2) {
    errors.fullName = 'Please enter a valid full name'
    isValid = false
  }
  
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
  } else if (!Object.values(passwordChecks.value).every(check => check)) {
    errors.password = 'Password does not meet all requirements'
    isValid = false
  }
  
  // Confirm password validation
  if (!form.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password'
    isValid = false
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    isValid = false
  }
  
  // Terms validation
  if (!form.agreeTerms) {
    errors.agreeTerms = 'You must agree to the Terms of Service and Privacy Policy'
    isValid = false
  }
  
  // Risk acknowledgment validation
  if (!form.agreeRisk) {
    errors.agreeRisk = 'You must acknowledge the trading risks'
    isValid = false
  }
  
  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  isLoading.value = true
  
  try {
    await authStore.register({
      full_name: form.fullName,
      email: form.email,
      password: form.password,
      email_notifications: form.emailNotifications
    })
  } catch (error: any) {
    console.error('Registration error:', error)
  } finally {
    isLoading.value = false
  }
}

// Lifecycle
onMounted(() => {
  // Auto-focus full name field
  const nameInput = document.getElementById('fullName')
  if (nameInput) {
    nameInput.focus()
  }
})
</script>

<style scoped>
/* Additional custom styles */
.form-input:focus + .absolute button {
  @apply text-gray-600;
}
</style>