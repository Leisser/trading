<template>
  <div class="dashboard-auth-container">
    <!-- Firebase Authentication for Dashboard -->
    <div v-if="!isEmailAuth" class="auth-methods">
      <h2 class="auth-title">🔐 Dashboard Access</h2>
      <p class="auth-subtitle">Superuser authentication required</p>

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
          Sign in with Google (Superuser)
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
        Sign in with email (Superuser)
      </button>
    </div>

    <!-- Email/Password Form -->
    <div v-else class="email-auth-form">
      <div class="form-header">
        <button @click="toggleEmailAuth" class="back-btn" :disabled="loading">
          ← Back
        </button>
        <h2 class="form-title">🔐 Superuser Dashboard Access</h2>
        <p class="form-subtitle">Enter your superuser credentials</p>
      </div>

      <form @submit.prevent="handleEmailAuth" class="auth-form">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            :disabled="loading"
            placeholder="admin@example.com"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            :disabled="loading"
            placeholder="Enter your password"
            class="form-input"
          />
        </div>

        <button
          type="submit"
          :disabled="loading || !email || !password"
          class="submit-btn"
        >
          <span v-if="loading" class="loading-spinner"></span>
          {{ isLogin ? 'Sign In to Dashboard' : 'Create Superuser Account' }}
        </button>
      </form>

      <div class="form-footer">
        <button
          @click="handlePasswordReset"
          :disabled="loading"
          class="forgot-password-btn"
        >
          Forgot Password?
        </button>
      </div>
    </div>

    <!-- Access Denied Message -->
    <div v-if="accessDenied" class="access-denied">
      <div class="denied-icon">🚫</div>
      <h3>Access Denied</h3>
      <p>{{ accessDeniedMessage }}</p>
      <button @click="clearAccessDenied" class="retry-btn">
        Try Again
      </button>
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
  redirectTo?: string
}

const props = withDefaults(defineProps<Props>(), {
  redirectTo: '/dashboard'
})

// Composables
const router = useRouter()
const authStore = useAuthStore()

// State
const isEmailAuth = ref(false)
const loading = ref(false)
const email = ref('')
const password = ref('')
const accessDenied = ref(false)
const accessDeniedMessage = ref('')

// Computed
const isLogin = computed(() => true) // Dashboard is always login mode

// Methods
const toggleEmailAuth = () => {
  isEmailAuth.value = !isEmailAuth.value
  clearAccessDenied()
}

const clearAccessDenied = () => {
  accessDenied.value = false
  accessDeniedMessage.value = ''
}

const signInWithGoogle = async () => {
  loading.value = true
  clearAccessDenied()

  try {
    const result = await firebaseAuth.signInWithGoogle()

    if (result.success && result.idToken) {
      const authResult = await authStore.firebaseDashboardAuth(result.idToken, result.user)

      if (authResult.success) {
        router.push(props.redirectTo)
      } else {
        if (authResult.requires_superuser) {
          accessDenied.value = true
          accessDeniedMessage.value = authResult.error || 'You do not have superuser credentials to access the dashboard.'
        } else {
          alert(authResult.error || 'Dashboard authentication failed')
        }
      }
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

const handleEmailAuth = async () => {
  if (!email.value || !password.value) {
    alert('Please enter both email and password')
    return
  }

  loading.value = true
  clearAccessDenied()

  try {
    const result = await firebaseAuth.signInWithEmail(email.value, password.value)

    if (result.success && result.idToken) {
      const authResult = await authStore.firebaseDashboardAuth(result.idToken, result.user)

      if (authResult.success) {
        router.push(props.redirectTo)
      } else {
        if (authResult.requires_superuser) {
          accessDenied.value = true
          accessDeniedMessage.value = authResult.error || 'You do not have superuser credentials to access the dashboard.'
        } else {
          alert(authResult.error || 'Dashboard authentication failed')
        }
      }
    } else {
      alert(result.error || 'Email sign-in failed')
    }
  } catch (error) {
    console.error('Email auth error:', error)
    alert('Email sign-in failed. Please try again.')
  } finally {
    loading.value = false
  }
}

const handlePasswordReset = async () => {
  if (!email.value) {
    alert('Please enter your email address first')
    return
  }

  try {
    const result = await firebaseAuth.sendPasswordReset(email.value)
    if (result.success) {
      alert('Password reset email sent! Check your inbox.')
    } else {
      alert(result.error || 'Failed to send password reset email')
    }
  } catch (error) {
    console.error('Password reset error:', error)
    alert('Password reset failed. Please try again.')
  }
}
</script>

<style scoped>
.dashboard-auth-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.auth-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
  text-align: center;
}

.auth-subtitle {
  color: #6b7280;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.social-buttons {
  margin-bottom: 1.5rem;
}

.social-btn {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.google-btn {
  background: #4285f4;
  color: white;
}

.google-btn:hover:not(:disabled) {
  background: #3367d6;
  transform: translateY(-2px);
}

.social-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.social-icon {
  width: 20px;
  height: 20px;
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
  font-size: 0.875rem;
}

.email-auth-btn {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  background: white;
  color: #374151;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.email-auth-btn:hover:not(:disabled) {
  border-color: #6366f1;
  color: #6366f1;
}

.form-header {
  margin-bottom: 2rem;
}

.back-btn {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  padding: 0.5rem 0;
}

.back-btn:hover:not(:disabled) {
  color: #374151;
}

.form-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  color: #6b7280;
  margin-bottom: 1.5rem;
}

.auth-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-input {
  width: 100%;
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

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  background: #4f46e5;
  transform: translateY(-2px);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.form-footer {
  text-align: center;
}

.forgot-password-btn {
  background: none;
  border: none;
  color: #6366f1;
  cursor: pointer;
  font-size: 0.875rem;
  text-decoration: underline;
}

.forgot-password-btn:hover:not(:disabled) {
  color: #4f46e5;
}

.access-denied {
  text-align: center;
  padding: 2rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  margin-top: 1rem;
}

.denied-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.access-denied h3 {
  color: #dc2626;
  margin-bottom: 0.5rem;
}

.access-denied p {
  color: #7f1d1d;
  margin-bottom: 1.5rem;
}

.retry-btn {
  background: #dc2626;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.retry-btn:hover {
  background: #b91c1c;
}
</style>
