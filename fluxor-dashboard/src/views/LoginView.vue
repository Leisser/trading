<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <div class="mx-auto h-12 w-12 flex items-center justify-center bg-primary-600 rounded-full">
          <span class="text-white font-bold text-xl">F</span>
        </div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Sign in to Fluxor Dashboard
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Trading Control Panel Access
        </p>
      </div>
      
      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
        <div v-if="authStore.loginError" class="bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded relative">
          <strong class="font-bold">Login Failed:</strong>
          <span class="block sm:inline">{{ authStore.loginError }}</span>
        </div>

        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="username" class="sr-only">Username</label>
            <input
              id="username"
              v-model="loginForm.username"
              name="username"
              type="text"
              required
              class="input-field"
              placeholder="Username"
              :disabled="authStore.isLoading"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              v-model="loginForm.password"
              name="password"
              type="password"
              required
              class="input-field"
              placeholder="Password"
              :disabled="authStore.isLoading"
            />
          </div>
          <div v-if="showTwoFactor">
            <label for="twoFactorCode" class="sr-only">2FA Code</label>
            <input
              id="twoFactorCode"
              v-model="loginForm.twoFactorCode"
              name="twoFactorCode"
              type="text"
              maxlength="6"
              class="input-field"
              placeholder="2FA Code (6 digits)"
              :disabled="authStore.isLoading"
            />
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              v-model="loginForm.rememberMe"
              name="remember-me"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label for="remember-me" class="ml-2 block text-sm text-gray-900">
              Remember me
            </label>
          </div>

          <div class="text-sm">
            <a href="#" class="font-medium text-primary-600 hover:text-primary-500">
              Forgot your password?
            </a>
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <LockClosedIcon v-if="!authStore.isLoading" class="h-5 w-5 text-primary-500 group-hover:text-primary-400" />
              <div v-else class="loading-spinner"></div>
            </span>
            {{ authStore.isLoading ? 'Signing in...' : 'Sign in' }}
          </button>
        </div>

        <div class="text-center">
          <button
            type="button"
            @click="showTwoFactor = !showTwoFactor"
            class="text-sm text-primary-600 hover:text-primary-500"
          >
            {{ showTwoFactor ? 'Hide' : 'Show' }} 2FA Code
          </button>
        </div>
      </form>

      <!-- Demo Credentials -->
      <div class="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
        <h3 class="text-sm font-medium text-yellow-800">Demo Credentials</h3>
        <div class="mt-2 text-sm text-yellow-700">
          <p><strong>Admin:</strong> admin / admin123</p>
          <p><strong>Manager:</strong> manager / manager123</p>
          <p><strong>Viewer:</strong> viewer / viewer123</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { LockClosedIcon } from '@heroicons/vue/24/solid'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const showTwoFactor = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
  twoFactorCode: '',
  rememberMe: false
})

const handleLogin = async () => {
  const credentials: any = {
    username: loginForm.username,
    password: loginForm.password
  }

  if (showTwoFactor.value && loginForm.twoFactorCode) {
    credentials.twoFactorCode = loginForm.twoFactorCode
  }

  const result = await authStore.login(credentials)
  
  if (result.success) {
    // Redirect to dashboard or intended route
    const redirect = router.currentRoute.value.query.redirect as string
    await router.push(redirect || '/')
  }
  // Error handling is done by the store
}
</script>
