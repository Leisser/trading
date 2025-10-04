<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Create your account
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Or
        <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-500">
          sign in to your existing account
        </router-link>
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="card">
        <form class="space-y-6" @submit.prevent="handleRegister">
          <div v-if="error" class="bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded">
            {{ error }}
          </div>

          <div>
            <label for="full_name" class="block text-sm font-medium text-gray-700">
              Full Name
            </label>
            <div class="mt-1">
              <input
                id="full_name"
                v-model="form.full_name"
                name="full_name"
                type="text"
                autocomplete="name"
                required
                class="input-field"
                :class="{ 'border-danger-500': errors.full_name }"
              />
            </div>
            <p v-if="errors.full_name" class="mt-1 text-sm text-danger-600">{{ errors.full_name }}</p>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Email address
            </label>
            <div class="mt-1">
              <input
                id="email"
                v-model="form.email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="input-field"
                :class="{ 'border-danger-500': errors.email }"
              />
            </div>
            <p v-if="errors.email" class="mt-1 text-sm text-danger-600">{{ errors.email }}</p>
          </div>

          <div>
            <label for="phone_number" class="block text-sm font-medium text-gray-700">
              Phone Number (optional)
            </label>
            <div class="mt-1">
              <input
                id="phone_number"
                v-model="form.phone_number"
                name="phone_number"
                type="tel"
                autocomplete="tel"
                class="input-field"
                :class="{ 'border-danger-500': errors.phone_number }"
              />
            </div>
            <p v-if="errors.phone_number" class="mt-1 text-sm text-danger-600">{{ errors.phone_number }}</p>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1">
              <input
                id="password"
                v-model="form.password"
                name="password"
                type="password"
                autocomplete="new-password"
                required
                class="input-field"
                :class="{ 'border-danger-500': errors.password }"
              />
            </div>
            <p v-if="errors.password" class="mt-1 text-sm text-danger-600">{{ errors.password }}</p>
          </div>

          <div>
            <label for="password_confirm" class="block text-sm font-medium text-gray-700">
              Confirm Password
            </label>
            <div class="mt-1">
              <input
                id="password_confirm"
                v-model="form.password_confirm"
                name="password_confirm"
                type="password"
                autocomplete="new-password"
                required
                class="input-field"
                :class="{ 'border-danger-500': errors.password_confirm }"
              />
            </div>
            <p v-if="errors.password_confirm" class="mt-1 text-sm text-danger-600">{{ errors.password_confirm }}</p>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading"
              class="btn-primary w-full flex justify-center"
            >
              <span v-if="loading" class="inline-flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating account...
              </span>
              <span v-else>Create account</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const form = reactive({
  full_name: '',
  email: '',
  phone_number: '',
  password: '',
  password_confirm: ''
})

const errors = reactive({
  full_name: '',
  email: '',
  phone_number: '',
  password: '',
  password_confirm: ''
})

const error = ref('')
const loading = ref(false)

const validateForm = () => {
  errors.full_name = ''
  errors.email = ''
  errors.phone_number = ''
  errors.password = ''
  errors.password_confirm = ''
  
  if (!form.full_name) {
    errors.full_name = 'Full name is required'
  }
  
  if (!form.email) {
    errors.email = 'Email is required'
  } else if (!/\S+@\S+\.\S+/.test(form.email)) {
    errors.email = 'Email is invalid'
  }
  
  if (form.phone_number && !/^\+?[\d\s\-\(\)]+$/.test(form.phone_number)) {
    errors.phone_number = 'Phone number is invalid'
  }
  
  if (!form.password) {
    errors.password = 'Password is required'
  } else if (form.password.length < 8) {
    errors.password = 'Password must be at least 8 characters'
  }
  
  if (!form.password_confirm) {
    errors.password_confirm = 'Please confirm your password'
  } else if (form.password !== form.password_confirm) {
    errors.password_confirm = 'Passwords do not match'
  }
  
  return !Object.values(errors).some(error => error)
}

const handleRegister = async () => {
  if (!validateForm()) return
  
  loading.value = true
  error.value = ''
  
  const result = await authStore.register({
    full_name: form.full_name,
    email: form.email,
    phone_number: form.phone_number,
    password: form.password,
    password_confirm: form.password_confirm
  })
  
  if (result.success) {
    toast.showToast('Account created successfully! Please log in.', 'success')
    router.push('/login')
  } else {
    error.value = typeof result.error === 'string' ? result.error : 'Registration failed'
    toast.showToast(error.value, 'error')
  }
  
  loading.value = false
}
</script> 