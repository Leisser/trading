<template>
  <div class="login_container">
    <div class="login_background">
      <div class="floating_shapes">
        <div class="shape shape_1"></div>
        <div class="shape shape_2"></div>
        <div class="shape shape_3"></div>
        <div class="shape shape_4"></div>
        <div class="shape shape_5"></div>
      </div>
      <div class="background_particles">
        <div class="particle particle_1"></div>
        <div class="particle particle_2"></div>
        <div class="particle particle_3"></div>
      </div>
      <div class="background_grid">
        <div class="grid_line grid_line_1"></div>
        <div class="grid_line grid_line_2"></div>
        <div class="grid_line grid_line_3"></div>
      </div>
    </div>

    <div class="login_content">
      <div class="login_header">
        <h1 class="login_title">Welcome back to <span class="gradient-text">Fluxor</span></h1>
        <p class="login_subtitle">Sign in to access your trading dashboard</p>
      </div>

      <div class="login_form_container">
        <div class="card">
          <form class="login_form" @submit.prevent="handleLogin">
            <div v-if="error" class="error_message">
              <svg class="error_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              {{ error }}
            </div>

            <div class="form_group">
              <label for="email" class="form_label">
                <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"
                  ></path>
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path>
                </svg>
                Email address
              </label>
              <input
                id="email"
                v-model="form.email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="input-field"
                :class="{ input_error: errors.email }"
                placeholder="Enter your email"
              />
              <p v-if="errors.email" class="error_text">{{ errors.email }}</p>
            </div>

            <div class="form_group">
              <label for="password" class="form_label">
                <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                Password
              </label>
              <input
                id="password"
                v-model="form.password"
                name="password"
                type="password"
                autocomplete="current-password"
                required
                class="input-field"
                :class="{ input_error: errors.password }"
                placeholder="Enter your password"
              />
              <p v-if="errors.password" class="error_text">{{ errors.password }}</p>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="btn-primary w-full flex justify-center items-center"
            >
              <span v-if="loading" class="loading_spinner">
                <svg
                  class="animate-spin h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Signing in...
              </span>
              <span v-else class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M3 3a1 1 0 011 1v12a1 1 0 11-2 0V4a1 1 0 011-1zm7.707 3.293a1 1 0 010 1.414L9.414 9H17a1 1 0 110 2H9.414l1.293 1.293a1 1 0 01-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                Sign in
              </span>
            </button>
          </form>

          <!-- Social Login Buttons -->
          <SocialLoginButtons :loading="loading" @phone-login="showPhoneModal = true" />

          <div class="login_footer">
            <p class="footer_text">
              Don't have an account?
              <router-link to="/register" class="footer_link"> Create one now </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Phone Verification Modal -->
    <PhoneVerificationModal
      :is-open="showPhoneModal"
      @close="showPhoneModal = false"
      @success="handlePhoneVerificationSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import SocialLoginButtons from '@/components/SocialLoginButtons.vue'
import PhoneVerificationModal from '@/components/PhoneVerificationModal.vue'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const form = reactive({
  email: '',
  password: '',
})

const errors = reactive({
  email: '',
  password: '',
})

const error = ref('')
const loading = ref(false)
const showPhoneModal = ref(false)

const validateForm = () => {
  errors.email = ''
  errors.password = ''

  if (!form.email) {
    errors.email = 'Email is required'
  } else if (!/\S+@\S+\.\S+/.test(form.email)) {
    errors.email = 'Email is invalid'
  }

  if (!form.password) {
    errors.password = 'Password is required'
  } else if (form.password.length < 6) {
    errors.password = 'Password must be at least 6 characters'
  }

  return !errors.email && !errors.password
}

const handleLogin = async () => {
  if (!validateForm()) return

  loading.value = true
  error.value = ''

  try {
    console.log('Attempting login with:', {
      email: form.email,
      password: form.password ? '***' : 'empty',
    })

    const result = await authStore.login(form.email, form.password)

    console.log('Login result:', result)

    if (result.success) {
      toast.showToast('Login successful!', 'success')
      router.push('/dashboard')
    } else {
      error.value = result.error || 'Login failed'
      toast.showToast(result.error || 'Login failed', 'error')
    }
  } catch (err) {
    console.error('Login error:', err)
    error.value = 'An unexpected error occurred during login'
    toast.showToast('An unexpected error occurred during login', 'error')
  } finally {
    loading.value = false
  }
}

const handlePhoneVerificationSuccess = (phoneNumber: string) => {
  showPhoneModal.value = false
  toast.showToast(`Phone ${phoneNumber} verified successfully!`, 'success')
  // You can redirect or perform additional actions here
}
</script>

<style scoped>
.login_container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}

.login_background {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.floating_shapes {
  position: absolute;
  inset: 0;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 8s ease-in-out infinite;
}

.shape_1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.shape_2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: 3s;
}

.shape_3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 20%;
  animation-delay: 6s;
}

.shape_4 {
  width: 120px;
  height: 120px;
  top: 80%;
  right: 10%;
  animation-delay: 9s;
}

.shape_5 {
  width: 80px;
  height: 80px;
  top: 40%;
  right: 40%;
  animation-delay: 12s;
}

.background_particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.background_particles .particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background: linear-gradient(135deg, #ffffff, #f093fb);
  border-radius: 50%;
  animation: particleFloat 15s linear infinite;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.6);
}

.background_particles .particle_1 {
  top: 15%;
  left: 15%;
  animation-delay: 0s;
}

.background_particles .particle_2 {
  top: 70%;
  right: 20%;
  animation-delay: 5s;
}

.background_particles .particle_3 {
  bottom: 25%;
  left: 35%;
  animation-delay: 10s;
}

.background_grid {
  position: absolute;
  inset: 0;
  opacity: 0.05;
}

.background_grid .grid_line {
  position: absolute;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
}

.background_grid .grid_line_1 {
  top: 25%;
  left: 0;
  right: 0;
  height: 1px;
}

.background_grid .grid_line_2 {
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
}

.background_grid .grid_line_3 {
  top: 0;
  bottom: 0;
  left: 50%;
  width: 1px;
  transform: translateX(-50%);
}

.login_content {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 1200px;
  padding: 2rem 2.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  box-sizing: border-box;
}

.login_header {
  color: white;
  text-align: center;
}

.login_title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.login_subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.login_form_container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.card {
  background: rgba(17, 24, 39, 0.98);
  backdrop-filter: blur(24px);
  border: 1.5px solid rgba(59, 130, 246, 0.15);
  border-radius: 2rem;
  padding: 3rem 2.25rem 2.5rem 2.25rem;
  box-shadow:
    0 12px 48px 0 rgba(59, 130, 246, 0.18),
    0 2px 8px 0 rgba(0, 0, 0, 0.1);
  max-width: 420px;
  width: 100%;
  margin: 0 1.5rem;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  box-sizing: border-box;
  min-width: 320px;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
  border-radius: 2rem 2rem 0 0;
}

.card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(147, 51, 234, 0.08));
  opacity: 0.7;
  pointer-events: none;
  z-index: 0;
}

.login_form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  z-index: 1;
}

.form_group {
  margin-bottom: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form_label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.label_icon {
  width: 1rem;
  height: 1rem;
  color: #6b7280;
}

.input-field {
  width: 100%;
  box-sizing: border-box;
  padding: 1rem 1.25rem;
  border: 2px solid rgba(229, 231, 235, 0.5);
  border-radius: 12px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-right: 0;
}

.input-field:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow:
    0 0 0 3px rgba(59, 130, 246, 0.1),
    0 8px 16px -4px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.input-field.error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.input-field::placeholder {
  color: #9ca3af;
}

.error_text {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.error_text::before {
  content: '⚠';
  font-size: 0.75rem;
}

.btn-primary {
  width: 100%;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 16px -4px rgba(59, 130, 246, 0.3);
  position: relative;
  overflow: hidden;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
  height: 48px;
  font-size: 1.1rem;
  border-radius: 1rem;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-primary:hover::before {
  left: 100%;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  transform: translateY(-2px);
  box-shadow: 0 12px 24px -6px rgba(59, 130, 246, 0.4);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading_spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login_footer {
  margin-top: 1.5rem;
  text-align: center;
  z-index: 1;
}

.footer_text {
  color: #6b7280;
  font-size: 0.875rem;
}

.footer_link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.footer_link:hover {
  color: #2563eb;
  text-decoration: underline;
}

/* Enhanced Card Styling */
.card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
  border-radius: 24px 24px 0 0;
}

.card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(147, 51, 234, 0.05));
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.card:hover::after {
  opacity: 1;
}

/* Animations */
@keyframes float {
  0%,
  100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes particleFloat {
  0% {
    transform: translateY(0px) translateX(0px);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) translateX(50px);
    opacity: 0;
  }
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* Apply animations */
.login_header {
  animation: fadeIn 0.8s ease-out;
}

.login_form_container {
  animation: slideIn 0.8s ease-out 0.2s both;
}

.form_group {
  animation: fadeIn 0.6s ease-out;
}

.form_group:nth-child(1) {
  animation-delay: 0.4s;
}
.form_group:nth-child(2) {
  animation-delay: 0.6s;
}

.btn-primary {
  animation: fadeIn 0.6s ease-out 0.8s both;
}

.login_footer {
  animation: fadeIn 0.6s ease-out 1s both;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .login_content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }

  .login_header {
    order: 2;
  }

  .login_form_container {
    order: 1;
  }

  .login_title {
    font-size: 2.5rem;
  }

  .login_subtitle {
    font-size: 1.125rem;
  }
}

@media (max-width: 768px) {
  .login_container {
    padding: 1rem;
  }

  .login_content {
    padding: 1rem;
  }

  .login_title {
    font-size: 2rem;
  }

  .login_subtitle {
    font-size: 1rem;
  }

  .card {
    padding: 2rem;
  }

  .form_label {
    font-size: 0.8rem;
  }

  .input-field {
    padding: 0.875rem 1rem;
    font-size: 0.9rem;
  }

  .btn-primary {
    padding: 0.875rem 1.25rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .login_title {
    font-size: 1.75rem;
  }

  .card {
    padding: 1.5rem;
    border-radius: 16px;
  }

  .shape {
    display: none;
  }
}

@media (max-width: 900px) {
  .login_content {
    padding: 1.5rem 1rem;
  }
  .card {
    margin: 0 0.5rem;
    min-width: 0;
  }
}

@media (max-width: 600px) {
  .login_content {
    padding: 0.5rem;
    min-height: 100vh;
  }
  .card {
    padding: 2rem 0.5rem 1.5rem 0.5rem;
    max-width: 98vw;
    border-radius: 1.25rem;
    margin: 0 0.25rem;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .card {
    background: rgba(17, 24, 39, 0.95);
    border-color: rgba(75, 85, 99, 0.3);
  }

  .form_label {
    color: #f9fafb;
  }

  .input-field {
    background: rgba(31, 41, 55, 0.9);
    border-color: rgba(75, 85, 99, 0.5);
    color: #f9fafb;
  }

  .input-field:focus {
    border-color: #60a5fa;
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
  }

  .input-field::placeholder {
    color: #9ca3af;
  }

  .footer_text {
    color: #9ca3af;
  }

  .footer_link {
    color: #60a5fa;
  }

  .footer_link:hover {
    color: #93c5fd;
  }
}

/* Focus states for accessibility */
.btn-primary:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.input-field:focus-visible {
  outline: none;
}

/* Loading state enhancements */
.loading_spinner svg {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Hover effects for interactive elements */
.form_group:hover .form_label {
  color: #3b82f6;
}

.form_group:hover .label_icon {
  color: #3b82f6;
  transform: scale(1.1);
  transition: all 0.3s ease;
}

/* Enhanced error states */
.input-field.error:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.error_message {
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

/* Success state for form submission */
.btn-primary:disabled {
  background: linear-gradient(135deg, #10b981, #059669);
  cursor: not-allowed;
}

/* Enhanced visual feedback */
.input-field:valid {
  border-color: #10b981;
}

.input-field:valid:focus {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}
</style>
