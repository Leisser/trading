import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export interface User {
  id: number
  username: string
  email: string
  firstName: string
  lastName: string
  role: 'admin' | 'manager' | 'viewer'
  permissions: string[]
  isActive: boolean
  lastLogin: Date | null
  twoFactorEnabled: boolean
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const isLoading = ref(false)
  const loginError = ref<string | null>(null)

  // Computed
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isManager = computed(() => user.value?.role === 'manager' || isAdmin.value)

  const hasPermission = (permission: string) => {
    return user.value?.permissions.includes(permission) || isAdmin.value
  }

  // Actions
  const login = async (credentials: { username: string; password: string; twoFactorCode?: string }) => {
    isLoading.value = true
    loginError.value = null

    try {
      const response = await api.auth.login(credentials)

      token.value = response.data.access_token
      user.value = response.data.user

      // Store token in localStorage
      localStorage.setItem('auth_token', token.value)
      localStorage.setItem('refresh_token', response.data.refresh_token)

      return { success: true }
    } catch (error: any) {
      loginError.value = error.response?.data?.message || 'Login failed'
      return { success: false, error: loginError.value }
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    isLoading.value = true

    try {
      if (token.value) {
        await api.auth.logout()
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear all auth data
      user.value = null
      token.value = null
      localStorage.removeItem('auth_token')
      localStorage.removeItem('refresh_token')
      isLoading.value = false
    }
  }

  const refreshToken = async () => {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      await logout()
      return false
    }

    try {
      const response = await api.auth.refresh(refreshToken)
      token.value = response.data.access_token
      localStorage.setItem('auth_token', token.value)
      return true
    } catch (error) {
      await logout()
      return false
    }
  }

  const fetchUser = async () => {
    if (!token.value) return false

    try {
      const response = await api.auth.getProfile()
      user.value = response.data
      return true
    } catch (error) {
      await logout()
      return false
    }
  }

  const changePassword = async (data: { currentPassword: string; newPassword: string }) => {
    try {
      await api.auth.changePassword(data)
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.response?.data?.message || 'Password change failed' }
    }
  }

  const enableTwoFactor = async () => {
    try {
      const response = await api.security.enableTwoFactor()
      if (user.value) {
        user.value.twoFactorEnabled = true
      }
      return { success: true, qrCode: response.data.qr_code, secret: response.data.secret }
    } catch (error: any) {
      return { success: false, error: error.response?.data?.message || 'Failed to enable 2FA' }
    }
  }

  const disableTwoFactor = async (code: string) => {
    try {
      await api.security.disableTwoFactor()
      if (user.value) {
        user.value.twoFactorEnabled = false
      }
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.response?.data?.message || 'Failed to disable 2FA' }
    }
  }

  const initialize = async () => {
    if (token.value) {
      const success = await fetchUser()
      if (!success) {
        await logout()
      }
      return success
    }
    return false
  }

  return {
    // State
    user: readonly(user),
    token: readonly(token),
    isLoading: readonly(isLoading),
    loginError: readonly(loginError),

    // Computed
    isAuthenticated,
    isAdmin,
    isManager,
    hasPermission,

    // Actions
    login,
    logout,
    refreshToken,
    fetchUser,
    changePassword,
    enableTwoFactor,
    disableTwoFactor,
    initialize
  }
})
