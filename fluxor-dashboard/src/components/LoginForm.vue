<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <h1>Fluxor</h1>
          <span>Admin Dashboard</span>
        </div>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="credentials.username"
            type="email"
            placeholder="Enter your email"
            required
            :disabled="isLoading"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="credentials.password"
            type="password"
            placeholder="Enter your password"
            required
            :disabled="isLoading"
          />
        </div>
        
        <div v-if="loginError" class="error-message">
          {{ loginError }}
        </div>
        
        <button type="submit" class="login-button" :disabled="isLoading">
          <span v-if="isLoading">Signing in...</span>
          <span v-else>Sign In</span>
        </button>
      </form>
      
      <div class="login-footer">
        <p>Admin and Superadmin access only</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const credentials = reactive({
  username: '',
  password: ''
})

const isLoading = ref(false)
const loginError = ref('')

const handleLogin = async () => {
  if (!credentials.username || !credentials.password) {
    loginError.value = 'Please enter both email and password'
    return
  }
  
  isLoading.value = true
  loginError.value = ''
  
  try {
    // Use the API directly since the store might not have the right method
    const response = await fetch('http://localhost:8000/api/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: credentials.username,
        password: credentials.password
      }),
    })
    
    if (!response.ok) {
      throw new Error('Invalid credentials')
    }
    
    const data = await response.json()
    
    // Store tokens
    localStorage.setItem('auth_token', data.access)
    localStorage.setItem('token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    
    // Fetch user profile to check admin status
    const profileResponse = await fetch('http://localhost:8000/api/profile/', {
      headers: {
        'Authorization': `Bearer ${data.access}`,
      },
    })
    
    if (profileResponse.ok) {
      const user = await profileResponse.json()
      
      // Check if user is admin or superuser
      if (!user.is_staff && !user.is_superuser) {
        loginError.value = 'Access denied. Admin privileges required.'
        localStorage.removeItem('auth_token')
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
        return
      }
      
      // Initialize auth store
      await authStore.initialize()
      
      // Redirect to dashboard
      router.push('/')
    } else {
      throw new Error('Failed to fetch user profile')
    }
  } catch (error: any) {
    console.error('Login error:', error)
    loginError.value = error.message || 'Login failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  padding: 20px;
}

.login-card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border-color);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo h1 {
  color: var(--primary-color);
  font-size: 32px;
  font-weight: bold;
  margin: 0 0 8px 0;
}

.logo span {
  color: var(--text-secondary);
  font-size: 16px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: var(--text-primary);
  font-weight: 500;
  font-size: 14px;
}

.form-group input {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: 16px;
  transition: border-color 0.2s ease;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(153, 227, 158, 0.1);
}

.form-group input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: var(--error-color);
  font-size: 14px;
  text-align: center;
  padding: 8px;
  background: rgba(207, 49, 39, 0.1);
  border-radius: 6px;
  border: 1px solid rgba(207, 49, 39, 0.2);
}

.login-button {
  background: var(--primary-color);
  color: var(--text-dark);
  border: none;
  padding: 14px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 8px;
}

.login-button:hover:not(:disabled) {
  background: var(--primary-dark);
  transform: translateY(-1px);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
}

.login-footer p {
  color: var(--text-muted);
  font-size: 14px;
  margin: 0;
}
</style>
