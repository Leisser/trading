<template>
  <div class="firebase-auth-container">
    <!-- Email/Password Form -->
    <div v-if="!isEmailAuth" class="auth-methods">
      <h2 class="auth-title">{{ isLogin ? 'Sign In' : 'Create Account' }}</h2>

      <!-- Social Login Buttons -->
      <div class="social-buttons">
        <button
          @click="signInWithGoogle"
          :disabled="loading"
          class="social-btn google-btn"
        >
          <svg class="social-icon" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          {{ isLogin ? 'Sign in with Google' : 'Sign up with Google' }}
        </button>

      </div>

      <!-- Divider -->
      <div class="divider">
        <span>or</span>
      </div>

      <!-- Email/Password Option -->
      <button
        @click="toggleEmailAuth"
        class="email-auth-btn"
        :disabled="loading"
      >
        {{ isLogin ? 'Sign in with email' : 'Sign up with email' }}
      </button>
    </div>

    <!-- Email/Password Form -->
    <div v-else class="email-auth-form">
      <h2 class="auth-title">{{ isLogin ? 'Sign In' : 'Create Account' }}</h2>

      <form @submit.prevent="handleEmailAuth" class="auth-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="Enter your email"
            class="form-input"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="Enter your password"
            class="form-input"
            :disabled="loading"
            minlength="6"
          />
        </div>

        <div v-if="!isLogin" class="form-group">
          <label for="displayName">Full Name (Optional)</label>
          <input
            id="displayName"
            v-model="displayName"
            type="text"
            placeholder="Enter your full name"
            class="form-input"
            :disabled="loading"
          />
        </div>

        <button
          type="submit"
          class="auth-submit-btn"
          :disabled="loading || !email || !password"
        >
          <span v-if="loading" class="spinner"></span>
          {{ isLogin ? 'Sign In' : 'Create Account' }}
        </button>
      </form>

      <!-- Password Reset Link -->
      <div v-if="isLogin" class="auth-links">
        <button @click="handlePasswordReset" class="link-btn" :disabled="loading">
          Forgot password?
        </button>
      </div>

      <!-- Toggle Login/Register -->
      <div class="auth-links">
        <button @click="toggleLoginMode" class="link-btn" :disabled="loading">
          {{ isLogin ? "Don't have an account? Sign up" : "Already have an account? Sign in" }}
        </button>
      </div>

      <!-- Back to social login -->
      <button @click="toggleEmailAuth" class="back-btn" :disabled="loading">
        ← Back to other options
      </button>
    </div>

    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { firebaseAuth, type AuthResult } from '@/services/firebaseAuthFixed'
import { useAuthStore } from '@/stores/auth'

// Props
interface Props {
  defaultMode?: 'login' | 'register'
  redirectTo?: string
}

const props = withDefaults(defineProps<Props>(), {
  defaultMode: 'login',
  redirectTo: '/dashboard'
})

// Composables
const router = useRouter()
const authStore = useAuthStore()

// State
const isLogin = ref(props.defaultMode === 'login')
const isEmailAuth = ref(false)
const loading = ref(false)
const email = ref('')
const password = ref('')
const displayName = ref('')

// Methods
const toggleLoginMode = () => {
  isLogin.value = !isLogin.value
  clearForm()
}

const toggleEmailAuth = () => {
  isEmailAuth.value = !isEmailAuth.value
  clearForm()
}

const clearForm = () => {
  email.value = ''
  password.value = ''
  displayName.value = ''
}

const handleEmailAuth = async () => {
  loading.value = true

  try {
    let result: AuthResult

    if (isLogin.value) {
      result = await firebaseAuth.signInWithEmail(email.value, password.value)
    } else {
      result = await firebaseAuth.createAccount(email.value, password.value, displayName.value)
    }

    if (result.success && result.idToken) {
      // Authenticate with Django backend using Firebase token
      await authStore.firebaseAuth(result.idToken, result.user)
      router.push(props.redirectTo)
    } else {
      alert(result.error || 'Authentication failed')
    }
  } catch (error) {
    console.error('Email auth error:', error)
    alert('Authentication failed. Please try again.')
  } finally {
    loading.value = false
  }
}

const signInWithGoogle = async () => {
  loading.value = true

  try {
    const result = await firebaseAuth.signInWithGoogle()

    if (result.success && result.idToken) {
      await authStore.firebaseAuth(result.idToken, result.user)
      router.push(props.redirectTo)
    } else {
      alert(result.error || 'Google sign-in failed')
    }
  } catch (error) {
    console.error('Google auth error:', error)
    alert('Google sign-in failed. Please try again.')
  } finally {
    loading.value = false
  }
}


const handlePasswordReset = async () => {
  if (!email.value) {
    alert('Please enter your email address first')
    return
  }

  loading.value = true

  try {
    const result = await firebaseAuth.sendPasswordReset(email.value)

    if (result.success) {
      alert('Password reset email sent! Check your inbox.')
    } else {
      alert(result.error || 'Failed to send password reset email')
    }
  } catch (error) {
    console.error('Password reset error:', error)
    alert('Failed to send password reset email. Please try again.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.firebase-auth-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.auth-title {
  text-align: center;
  margin-bottom: 2rem;
  color: #1f2937;
  font-size: 1.5rem;
  font-weight: 600;
}

.social-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.social-btn:hover:not(:disabled) {
  border-color: #d1d5db;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.social-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.social-icon {
  width: 20px;
  height: 20px;
}

.google-btn:hover {
  border-color: #4285f4;
}

.apple-btn:hover {
  border-color: #000;
}

.divider {
  text-align: center;
  margin: 1.5rem 0;
  position: relative;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e5e7eb;
}

.divider span {
  background: white;
  padding: 0 1rem;
  color: #6b7280;
}

.email-auth-btn, .back-btn {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #6366f1;
  border-radius: 8px;
  background: white;
  color: #6366f1;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.email-auth-btn:hover:not(:disabled), .back-btn:hover:not(:disabled) {
  background: #6366f1;
  color: white;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #374151;
}

.form-input {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #6366f1;
}

.form-input:disabled {
  background: #f9fafb;
  cursor: not-allowed;
}

.auth-submit-btn {
  width: 100%;
  padding: 0.75rem 1rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.auth-submit-btn:hover:not(:disabled) {
  background: #4f46e5;
}

.auth-submit-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.auth-links {
  text-align: center;
  margin-top: 1rem;
}

.link-btn {
  background: none;
  border: none;
  color: #6366f1;
  cursor: pointer;
  text-decoration: underline;
  font-size: 0.875rem;
}

.link-btn:hover:not(:disabled) {
  color: #4f46e5;
}

.link-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
