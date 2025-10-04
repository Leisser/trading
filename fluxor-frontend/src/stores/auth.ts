import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/services/api'
import { PersistenceService } from '@/services/persistenceService'

export interface User {
  id: number | string
  email: string
  full_name: string
  is_verified?: boolean
  kyc_verified?: boolean
  role: string
  is_active?: boolean
  email_verified?: boolean
  phone_number?: string
  avatar?: string
  created_at?: string
  updated_at?: string
  firebase_uid?: string
  auth_provider?: string
}

export interface AuthTokens {
  access: string
  refresh: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const tokens = ref<AuthTokens | null>(null)
  const loading = ref(false)
  const isInitializing = ref(false)
  const persistenceService = PersistenceService.getInstance()

  const isAuthenticated = computed(() => {
    const authenticated = !!user.value && !!tokens.value
    console.log('Auth state check:', { user: !!user.value, tokens: !!tokens.value, authenticated })
    return authenticated
  })
  const isAdmin = computed(() => user.value?.role === 'admin')

  // Set up axios defaults (legacy - now handled by API service)
  const setupAxios = () => {
    // This is now handled by the API service interceptors
  }

    // Load tokens from persistence service and initialize user
  const loadTokens = async () => {
    // Prevent multiple simultaneous initializations
    if (isInitializing.value) {
      return
    }

    if (!isAuthenticated.value) {
      isInitializing.value = true
      try {
        const authData = await persistenceService.loadAuthData()

        if (authData) {
          tokens.value = {
            access: authData.access,
            refresh: authData.refresh
          }

          if (authData.user) {
            user.value = authData.user
            console.log('User data loaded from storage:', authData.user.email)
          } else {
            // Fetch user details if not stored
            await fetchUser()
          }

          setupAxios()
          startTokenRefresh()

          console.log('Authentication loaded successfully from', persistenceService.getStorageMethod())
        } else {
          console.log('No stored authentication data found')
        }
      } catch (error) {
        console.error('Failed to load stored tokens:', error)
        // Clear invalid tokens
        await logout()
      } finally {
        isInitializing.value = false
      }
    }
  }

  // Refresh access token
  const refreshToken = async () => {
    if (!tokens.value?.refresh || !user.value?.id) {
      return false
    }

    try {
      // Try Firebase session refresh first if user has Firebase UID
      if (user.value.firebase_uid) {
        const response = await authAPI.refreshFirebaseSession({
          refresh: tokens.value.refresh,
          user_id: String(user.value.id)
        })

        tokens.value = {
          access: response.access,
          refresh: response.refresh
        }

        // Update user data if provided
        if (response.user) {
          user.value = response.user
        }

        // Save to persistent storage
        await persistenceService.refreshAuthData(tokens.value)
        setupAxios()
        return true
      } else {
        // Fallback to regular JWT refresh
        const response = await authAPI.refreshToken(tokens.value.refresh)
        tokens.value = {
          access: response.access,
          refresh: response.refresh || tokens.value.refresh
        }

        // Save to persistent storage
        await persistenceService.refreshAuthData(tokens.value)
        setupAxios()
        return true
      }
    } catch (error) {
      console.error('Token refresh failed:', error)
      // If refresh fails, logout user
      await logout()
      return false
    }
  }

  // Firebase Authentication (Primary method)
  const firebaseAuth = async (
    idToken: string,
    firebaseUser?: {
      uid: string
      email: string | null
      displayName: string | null
      photoURL: string | null
      emailVerified: boolean
      phoneNumber: string | null
    }
  ) => {
    loading.value = true
    try {
      console.log('Sending Firebase token to backend...')
      const response = await authAPI.firebaseAuth({
        id_token: idToken,
        firebase_user: firebaseUser
      })

      console.log('Backend response:', response)

      tokens.value = response

      // Create user data for persistent storage
      const userData = firebaseUser ? {
        id: firebaseUser.uid,
        email: firebaseUser.email || '',
        full_name: firebaseUser.displayName || '',
        avatar: firebaseUser.photoURL || '',
        role: 'user',
        is_active: true,
        email_verified: firebaseUser.emailVerified,
        phone_number: firebaseUser.phoneNumber || '',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      } : undefined

      // Save to persistent storage with long-term expiry
      await persistenceService.saveAuthData({
        access: response.access,
        refresh: response.refresh,
        user: userData,
        firebase_uid: firebaseUser?.uid,
        auth_provider: 'firebase',
        expires_at: Date.now() + (30 * 24 * 60 * 60 * 1000) // 30 days
      })

      setupAxios()
      startTokenRefresh()

      if (userData) {
        user.value = userData
        console.log('Firebase user authenticated and stored:', userData.email)
      } else {
        await fetchUser()
      }

      return { success: true }
    } catch (error: unknown) {
      console.error('Firebase authentication error:', error)
      const axiosError = error as { response?: { data?: { detail?: string } } }
      return {
        success: false,
        error: axiosError.response?.data?.detail || 'Firebase authentication failed',
      }
    } finally {
      loading.value = false
    }
  }

  // Firebase Dashboard Authentication (Superuser only)
  const firebaseDashboardAuth = async (
    idToken: string,
    firebaseUser?: {
      uid: string
      email: string | null
      displayName: string | null
      photoURL: string | null
      emailVerified: boolean
      phoneNumber: string | null
    }
  ) => {
    loading.value = true
    try {
      console.log('Sending Firebase token to backend for dashboard access...')
      const response = await authAPI.firebaseDashboardAuth({
        id_token: idToken,
        firebase_user: firebaseUser
      })

      console.log('Dashboard authentication response:', response)

      tokens.value = response

      // Create user data for persistent storage
      const userData = firebaseUser ? {
        id: firebaseUser.uid,
        email: firebaseUser.email || '',
        full_name: firebaseUser.displayName || '',
        avatar: firebaseUser.photoURL || '',
        role: 'superuser',
        is_active: true,
        email_verified: firebaseUser.emailVerified,
        phone_number: firebaseUser.phoneNumber || '',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      } : undefined

      // Save to persistent storage with long-term expiry
      await persistenceService.saveAuthData({
        access: response.access,
        refresh: response.refresh,
        user: userData,
        firebase_uid: firebaseUser?.uid,
        auth_provider: 'firebase',
        expires_at: Date.now() + (30 * 24 * 60 * 60 * 1000) // 30 days
      })

      setupAxios()
      startTokenRefresh()

      if (userData) {
        user.value = userData
        console.log('Dashboard superuser authenticated and stored:', userData.email)
      } else {
        await fetchUser()
      }

      return { success: true }
    } catch (error: unknown) {
      console.error('Dashboard authentication error:', error)
      const axiosError = error as { response?: { data?: { detail?: string; message?: string; requires_superuser?: boolean } } }

      // Handle superuser access denied
      if (axiosError.response?.data?.requires_superuser) {
        return {
          success: false,
          error: axiosError.response.data.message || 'Access denied. Superuser credentials required.',
          requires_superuser: true
        }
      }

      return {
        success: false,
        error: axiosError.response?.data?.detail || axiosError.response?.data?.message || 'Dashboard authentication failed',
      }
    } finally {
      loading.value = false
    }
  }

  // Legacy login method (kept for compatibility but not used in Firebase flow)
  const login = async (email: string, password: string) => {
    return {
      success: false,
      error: 'Please use Firebase authentication instead of email/password login'
    }
  }

  // Register
  // Legacy register method (kept for compatibility but not used in Firebase flow)
  const register = async (userData: {
    email: string
    full_name: string
    password: string
    password_confirm: string
    phone_number?: string
  }) => {
    return {
      success: false,
      error: 'Please use Firebase authentication instead of email/password registration'
    }
  }

  // Fetch user details
  const fetchUser = async () => {
    try {
      const response = await authAPI.getUser()
      user.value = response
    } catch (error) {
      console.error('Failed to fetch user:', error)
      // If we can't fetch user details, clear tokens as they might be invalid
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as { response?: { status?: number } }
        if (axiosError.response?.status === 401) {
          logout()
        }
      }
    }
  }

  // Logout
  const logout = async () => {
    try {
      // Call server logout endpoint to invalidate tokens
      if (tokens.value?.access) {
        await authAPI.logout()
        console.log('Server logout successful')
      }
    } catch (error) {
      console.warn('Server logout failed, but continuing with local cleanup:', error)
    } finally {
      // Always clear local data regardless of server response
      user.value = null
      tokens.value = null

      // Clear all persistent storage
      await persistenceService.clearAuthData()

      // Clear any Firebase auth state
      try {
        const { firebaseAuth } = await import('@/services/firebaseAuthFixed')
        await firebaseAuth.signOut()
        console.log('Firebase logout successful')
      } catch (error) {
        console.warn('Firebase logout failed:', error)
      }

      stopTokenRefresh()
      console.log('Complete logout completed - all sessions cleared')
    }
  }

  // Social login
  const socialLogin = async (
    provider: 'google' | 'apple',
    accessToken: string,
    userData?: Record<string, unknown>,
  ) => {
    loading.value = true
    try {
      const response = await authAPI.socialAuth({
        provider,
        access_token: accessToken,
        user_data: userData,
      })
      tokens.value = response
      localStorage.setItem('auth_tokens', JSON.stringify(tokens.value))
      await fetchUser()
      return { success: true }
    } catch (error: unknown) {
      const axiosError = error as { response?: { data?: { detail?: string } } }
      return {
        success: false,
        error: axiosError.response?.data?.detail || 'Social login failed',
      }
    } finally {
      loading.value = false
    }
  }


  // Phone login (verification)
  const sendPhoneVerification = async (phoneNumber: string) => {
    loading.value = true
    try {
      const response = await authAPI.sendPhoneVerification(phoneNumber)
      return { success: true, code: response.code }
    } catch (error: unknown) {
      const axiosError = error as { response?: { data?: { error?: string } } }
      return {
        success: false,
        error: axiosError.response?.data?.error || 'Failed to send verification code',
      }
    } finally {
      loading.value = false
    }
  }

  const verifyPhoneCode = async (phoneNumber: string, code: string) => {
    loading.value = true
    try {
      const response = await authAPI.verifyPhoneCode(phoneNumber, code)
      // Optionally fetch user if logged in
      await fetchUser()
      return { success: true, message: response.message }
    } catch (error: unknown) {
      const axiosError = error as { response?: { data?: { error?: string } } }
      return {
        success: false,
        error: axiosError.response?.data?.error || 'Verification failed',
      }
    } finally {
      loading.value = false
    }
  }

  // Initialize store
  loadTokens()

  // Set up periodic token refresh (every 10 minutes)
  let refreshInterval: number | null = null

  const startTokenRefresh = () => {
    if (refreshInterval) {
      clearInterval(refreshInterval)
    }

    refreshInterval = setInterval(async () => {
      if (tokens.value?.refresh) {
        try {
          await refreshToken()
          console.log('Token refreshed automatically')
        } catch (error) {
          console.error('Automatic token refresh failed:', error)
        }
      }
    }, 10 * 60 * 1000) // 10 minutes
  }

  const stopTokenRefresh = () => {
    if (refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = null
    }
  }

  // Initialize authentication on store creation
  const initializeAuth = async () => {
    try {
      console.log('Initializing authentication...')
      await loadTokens()

      // Start refresh interval if we have tokens
      if (tokens.value?.refresh) {
        startTokenRefresh()
        console.log('Token refresh started')
      }
    } catch (error) {
      console.error('Authentication initialization failed:', error)
    }
  }

  // Auto-initialize on store creation
  initializeAuth()

  return {
    user,
    tokens,
    loading,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    fetchUser,
    refreshToken,
    loadTokens,
    startTokenRefresh,
    stopTokenRefresh,
    socialLogin,
    firebaseAuth,
    firebaseDashboardAuth,
    sendPhoneVerification,
    verifyPhoneCode,
  }
})
