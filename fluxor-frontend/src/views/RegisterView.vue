<template>
  <div class="register_container">
    <!-- Animated Background -->
    <div class="animated_background">
      <div class="floating_shape shape_1"></div>
      <div class="floating_shape shape_2"></div>
      <div class="floating_shape shape_3"></div>
      <div class="floating_shape shape_4"></div>
      <div class="floating_shape shape_5"></div>
    </div>

    <div class="register_content">
      <div class="register_header">
        <div class="logo_section">
          <div class="logo_icon">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
          <h1 class="register_title">Join <span class="gradient-text">Fluxor</span></h1>
          <p class="register_subtitle">Start your trading journey today</p>
        </div>
      </div>

      <div class="register_form_container">
        <div class="form_card">
          <div class="form_header">
            <h2 class="form_title">Create Account</h2>
            <p class="form_description">
              Already have an account?
              <router-link to="/login" class="link_text">Sign in here</router-link>
            </p>
          </div>

          <form @submit.prevent="handleRegister" class="register_form">
            <div v-if="error" class="error_banner">
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
              <label for="full_name" class="form_label">
                <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                Full Name
              </label>
              <input
                id="full_name"
                v-model="form.full_name"
                type="text"
                autocomplete="name"
                required
                class="form_input"
                :class="{ error: errors.full_name }"
                placeholder="Enter your full name"
              />
              <p v-if="errors.full_name" class="error_message">{{ errors.full_name }}</p>
            </div>

            <div class="form_group">
              <label for="email" class="form_label">
                <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"
                  ></path>
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path>
                </svg>
                Email Address
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                autocomplete="email"
                required
                class="form_input"
                :class="{ error: errors.email }"
                placeholder="Enter your email"
              />
              <p v-if="errors.email" class="error_message">{{ errors.email }}</p>
            </div>

            <div class="form_group">
              <label for="phone_number" class="form_label">
                <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"
                  ></path>
                </svg>
                Phone Number (Optional)
              </label>
              <input
                id="phone_number"
                v-model="form.phone_number"
                type="tel"
                autocomplete="tel"
                class="form_input"
                :class="{ error: errors.phone_number }"
                placeholder="Enter your phone number"
              />
              <p v-if="errors.phone_number" class="error_message">{{ errors.phone_number }}</p>
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
                type="password"
                autocomplete="new-password"
                required
                class="form_input"
                :class="{ error: errors.password }"
                placeholder="Create a strong password"
              />
              <p v-if="errors.password" class="error_message">{{ errors.password }}</p>
            </div>

            <div class="form_group">
              <label for="password_confirm" class="form_label">
                <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                Confirm Password
              </label>
              <input
                id="password_confirm"
                v-model="form.password_confirm"
                type="password"
                autocomplete="new-password"
                required
                class="form_input"
                :class="{ error: errors.password_confirm }"
                placeholder="Confirm your password"
              />
              <p v-if="errors.password_confirm" class="error_message">
                {{ errors.password_confirm }}
              </p>
            </div>

            <button type="submit" :disabled="loading" class="submit_btn">
              <span v-if="loading" class="loading_content">
                <div class="loading_spinner"></div>
                Creating Account...
              </span>
              <span v-else class="btn_content">
                <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                Create Account
              </span>
            </button>
          </form>

          <!-- Social Login Buttons -->
          <SocialLoginButtons :loading="loading" @phone-login="showPhoneModal = true" />

          <div class="form_footer">
            <p class="footer_text">
              By creating an account, you agree to our
              <a href="#" class="footer_link">Terms of Service</a> and
              <a href="#" class="footer_link">Privacy Policy</a>
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
  full_name: '',
  email: '',
  phone_number: '',
  password: '',
  password_confirm: '',
})

const errors = reactive({
  full_name: '',
  email: '',
  phone_number: '',
  password: '',
  password_confirm: '',
})

const error = ref('')
const loading = ref(false)
const showPhoneModal = ref(false)

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

  return !Object.values(errors).some((error) => error)
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
    password_confirm: form.password_confirm,
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

const handlePhoneVerificationSuccess = (phoneNumber: string) => {
  showPhoneModal.value = false
  toast.showToast(`Phone ${phoneNumber} verified successfully!`, 'success')
  // You can redirect or perform additional actions here
}
</script>

<style scoped>
.register_container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

.animated_background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 1;
}

.floating_shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.shape_1 {
  width: 80px;
  height: 80px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.shape_2 {
  width: 120px;
  height: 120px;
  top: 20%;
  right: 10%;
  animation-delay: 1s;
}

.shape_3 {
  width: 60px;
  height: 60px;
  bottom: 20%;
  left: 20%;
  animation-delay: 2s;
}

.shape_4 {
  width: 100px;
  height: 100px;
  bottom: 10%;
  right: 20%;
  animation-delay: 3s;
}

.shape_5 {
  width: 40px;
  height: 40px;
  top: 50%;
  left: 50%;
  animation-delay: 4s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

.register_content {
  width: 100%;
  max-width: 1200px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  z-index: 2;
  position: relative;
}

.register_header {
  color: white;
}

.logo_section {
  text-align: center;
}

.logo_icon {
  width: 4rem;
  height: 4rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2rem;
  color: white;
}

.register_title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.1;
}

.register_subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  font-weight: 300;
}

.register_form_container {
  display: flex;
  justify-content: center;
}

.form_card {
  width: 100%;
  max-width: 480px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.form_header {
  text-align: center;
  margin-bottom: 2rem;
}

.form_title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.form_description {
  color: #6b7280;
  font-size: 0.875rem;
}

.link_text {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.link_text:hover {
  color: #2563eb;
}

.register_form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.error_banner {
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  border: 1px solid #fca5a5;
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #dc2626;
  font-size: 0.875rem;
  font-weight: 500;
}

.error_icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

.form_group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form_label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.label_icon {
  width: 1rem;
  height: 1rem;
  color: #6b7280;
}

.form_input {
  padding: 1rem 1.25rem;
  border: 2px solid rgba(229, 231, 235, 0.5);
  border-radius: 12px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.2s ease;
  color: #1f2937;
}

.form_input::placeholder {
  color: #9ca3af;
}

.form_input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.form_input.error {
  border-color: #ef4444;
  background: rgba(254, 242, 242, 0.5);
}

.form_input.error:focus {
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.1);
}

.error_message {
  font-size: 0.75rem;
  color: #dc2626;
  font-weight: 500;
  margin-top: 0.25rem;
}

.submit_btn {
  margin-top: 1rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.submit_btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.submit_btn:hover::before {
  left: 100%;
}

.submit_btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -3px rgba(59, 130, 246, 0.4);
}

.submit_btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading_content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.btn_content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.loading_spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.btn_icon {
  width: 1.25rem;
  height: 1.25rem;
}

.form_footer {
  margin-top: 2rem;
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(229, 231, 235, 0.5);
}

.footer_text {
  font-size: 0.75rem;
  color: #6b7280;
  line-height: 1.5;
}

.footer_link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.footer_link:hover {
  color: #2563eb;
}

@media (max-width: 1024px) {
  .register_content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .register_header {
    text-align: center;
  }

  .register_title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .register_container {
    padding: 1rem;
  }

  .form_card {
    padding: 2rem;
  }

  .register_title {
    font-size: 2rem;
  }

  .register_subtitle {
    font-size: 1rem;
  }

  .form_title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .form_card {
    padding: 1.5rem;
  }

  .register_title {
    font-size: 1.75rem;
  }

  .form_title {
    font-size: 1.25rem;
  }
}
</style>
