import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { apiService } from '@/services/api'
import { useToast } from 'vue-toastification'
import type { User, LoginCredentials, RegisterData } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const isLoading = ref(false)
  const lastActivity = ref<Date>(new Date())

  // Router and toast
  const router = useRouter()
  const toast = useToast()

  // Computed
  const isAuthenticated = computed(() => !!user.value && !!token.value)
  const userName = computed(() => user.value?.full_name || user.value?.email || 'User')
  const userInitials = computed(() => {
    if (!user.value?.full_name) return 'U'
    return user.value.full_name
      .split(' ')
      .map(name => name[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  })

  // Actions
  const login = async (credentials: LoginCredentials) => {
    isLoading.value = true
    try {
      const response = await apiService.post('/accounts/login/', credentials)
      
      if (response.data.access && response.data.user) {
        // Store tokens
        token.value = response.data.access
        refreshToken.value = response.data.refresh
        localStorage.setItem('auth_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        
        // Store user
        user.value = response.data.user
        
        // Set API authorization header
        apiService.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
        
        // Update activity
        updateActivity()
        
        // Show success message
        toast.success(`Welcome back, ${response.data.user.full_name}!`)
        
        // Redirect to dashboard or intended page
        const redirect = router.currentRoute.value.query.redirect as string
        await router.push(redirect || '/')
        
        return response.data
      } else {
        throw new Error('Invalid response format')
      }
    } catch (error: any) {
      console.error('Login error:', error)
      
      let errorMessage = 'Login failed. Please try again.'
      if (error.response?.data?.error) {
        errorMessage = error.response.data.error
      } else if (error.response?.status === 401) {
        errorMessage = 'Invalid email or password'
      } else if (error.response?.status === 429) {
        errorMessage = 'Too many login attempts. Please try again later.'
      }
      
      toast.error(errorMessage)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const register = async (data: RegisterData) => {
    isLoading.value = true
    try {
      const response = await apiService.post('/accounts/register/', data)
      
      if (response.data) {
        toast.success('Account created successfully! Please check your email for verification.')
        await router.push({ name: 'Login' })
        return response.data
      }
    } catch (error: any) {
      console.error('Registration error:', error)
      
      let errorMessage = 'Registration failed. Please try again.'
      if (error.response?.data?.error) {
        errorMessage = error.response.data.error
      } else if (error.response?.data) {
        // Handle field-specific errors
        const errors = error.response.data
        if (errors.email) {
          errorMessage = `Email: ${errors.email[0]}`
        } else if (errors.password) {
          errorMessage = `Password: ${errors.password[0]}`
        } else if (errors.full_name) {
          errorMessage = `Name: ${errors.full_name[0]}`
        }
      }
      
      toast.error(errorMessage)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      // Attempt to logout on server
      if (token.value) {
        await apiService.post('/accounts/logout/')
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local state regardless of server response
      user.value = null
      token.value = null
      refreshToken.value = null
      
      // Clear localStorage
      localStorage.removeItem('auth_token')
      localStorage.removeItem('refresh_token')
      
      // Clear API authorization header
      delete apiService.defaults.headers.common['Authorization']
      
      // Redirect to login
      await router.push({ name: 'Login' })
      
      toast.info('You have been logged out')
    }
  }

  const fetchUser = async () => {
    if (!token.value) {
      throw new Error('No authentication token')
    }

    try {
      // Set authorization header
      apiService.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      
      const response = await apiService.get('/accounts/profile/')
      user.value = response.data
      updateActivity()
      
      return response.data
    } catch (error: any) {
      console.error('Fetch user error:', error)
      
      if (error.response?.status === 401) {
        // Token is invalid, try to refresh
        if (refreshToken.value) {
          try {
            await refreshAuthToken()
            // Retry fetching user
            const response = await apiService.get('/accounts/profile/')
            user.value = response.data
            updateActivity()
            return response.data
          } catch (refreshError) {
            // Refresh failed, logout
            await logout()
            throw refreshError
          }
        } else {
          // No refresh token, logout
          await logout()
          throw error
        }
      }
      
      throw error
    }
  }

  const refreshAuthToken = async () => {
    if (!refreshToken.value) {
      throw new Error('No refresh token available')
    }

    try {
      const response = await apiService.post('/accounts/token/refresh/', {
        refresh: refreshToken.value
      })

      if (response.data.access) {
        token.value = response.data.access
        localStorage.setItem('auth_token', response.data.access)
        apiService.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
        
        if (response.data.refresh) {
          refreshToken.value = response.data.refresh
          localStorage.setItem('refresh_token', response.data.refresh)
        }
        
        return response.data.access
      } else {
        throw new Error('Invalid refresh response')
      }
    } catch (error) {
      console.error('Token refresh error:', error)
      // Clear tokens and logout
      await logout()
      throw error
    }
  }

  const updateProfile = async (profileData: Partial<User>) => {
    isLoading.value = true
    try {
      const response = await apiService.put('/accounts/profile/', profileData)
      user.value = { ...user.value, ...response.data }
      toast.success('Profile updated successfully')
      return response.data
    } catch (error: any) {
      console.error('Update profile error:', error)
      
      let errorMessage = 'Failed to update profile'
      if (error.response?.data?.error) {
        errorMessage = error.response.data.error
      }
      
      toast.error(errorMessage)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const changePassword = async (passwordData: { current_password: string; new_password: string }) => {
    isLoading.value = true
    try {
      await apiService.post('/accounts/password/change/', passwordData)
      toast.success('Password changed successfully')
    } catch (error: any) {
      console.error('Change password error:', error)
      
      let errorMessage = 'Failed to change password'
      if (error.response?.data?.error) {
        errorMessage = error.response.data.error
      } else if (error.response?.data?.current_password) {
        errorMessage = 'Current password is incorrect'
      }
      
      toast.error(errorMessage)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const updateActivity = () => {
    lastActivity.value = new Date()
  }

  // Initialize token on store creation
  if (token.value) {
    apiService.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  // Auto-refresh token
  let refreshInterval: NodeJS.Timeout | null = null

  const startTokenRefresh = () => {
    if (refreshInterval) {
      clearInterval(refreshInterval)
    }
    
    // Refresh token every 50 minutes (tokens expire in 60 minutes)
    refreshInterval = setInterval(async () => {
      if (refreshToken.value && isAuthenticated.value) {
        try {
          await refreshAuthToken()
        } catch (error) {
          console.error('Auto token refresh failed:', error)
        }
      }
    }, 50 * 60 * 1000)
  }

  const stopTokenRefresh = () => {
    if (refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = null
    }
  }

  // Start auto-refresh if authenticated
  if (isAuthenticated.value) {
    startTokenRefresh()
  }

  return {
    // State
    user,
    token,
    refreshToken,
    isLoading,
    lastActivity,
    
    // Computed
    isAuthenticated,
    userName,
    userInitials,
    
    // Actions
    login,
    register,
    logout,
    fetchUser,
    refreshAuthToken,
    updateProfile,
    changePassword,
    updateActivity,
    startTokenRefresh,
    stopTokenRefresh
  }
})