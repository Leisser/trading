import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export interface User {
  id: number
  email: string
  full_name: string
  is_verified: boolean
  kyc_verified: boolean
  role: string
}

export interface AuthTokens {
  access: string
  refresh: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const tokens = ref<AuthTokens | null>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!user.value && !!tokens.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  // Set up axios defaults
  const setupAxios = () => {
    if (tokens.value?.access) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${tokens.value.access}`
    }
  }

  // Load tokens from localStorage
  const loadTokens = () => {
    const storedTokens = localStorage.getItem('auth_tokens')
    if (storedTokens) {
      tokens.value = JSON.parse(storedTokens)
      setupAxios()
    }
  }

  // Login
  const login = async (email: string, password: string) => {
    loading.value = true
    try {
      const response = await axios.post('http://localhost:8000/api/login/', {
        email,
        password
      })
      
      tokens.value = response.data
      localStorage.setItem('auth_tokens', JSON.stringify(tokens.value))
      setupAxios()
      
      // Get user details
      await fetchUser()
      
      return { success: true }
    } catch (error: any) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    } finally {
      loading.value = false
    }
  }

  // Register
  const register = async (userData: {
    email: string
    full_name: string
    password: string
    password_confirm: string
    phone_number?: string
  }) => {
    loading.value = true
    try {
      const response = await axios.post('http://localhost:8000/api/register/', userData)
      return { success: true, data: response.data }
    } catch (error: any) {
      return { 
        success: false, 
        error: error.response?.data || 'Registration failed' 
      }
    } finally {
      loading.value = false
    }
  }

  // Fetch user details
  const fetchUser = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/user/')
      user.value = response.data
    } catch (error) {
      console.error('Failed to fetch user:', error)
    }
  }

  // Logout
  const logout = () => {
    user.value = null
    tokens.value = null
    localStorage.removeItem('auth_tokens')
    delete axios.defaults.headers.common['Authorization']
  }

  // Initialize store
  loadTokens()

  return {
    user,
    tokens,
    loading,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    fetchUser
  }
}) 