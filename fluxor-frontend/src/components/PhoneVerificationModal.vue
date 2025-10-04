<template>
  <div v-if="isOpen" class="modal_overlay" @click="handleOverlayClick">
    <div class="modal_container" @click.stop>
      <div class="modal_content">
        <!-- Header -->
        <div class="modal_header">
          <h2 class="modal_title">Phone Verification</h2>
          <button @click="closeModal" class="close_button" type="button">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </button>
        </div>

        <!-- Step 1: Phone Number Input -->
        <div v-if="step === 1" class="step_content">
          <div class="step_description">
            <p class="description_text">Enter your phone number to receive a verification code</p>
          </div>

          <form @submit.prevent="sendVerificationCode" class="phone_form">
            <div class="form_group">
              <label for="phone_number" class="form_label">
                <svg class="label_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"
                  />
                </svg>
                Phone Number
              </label>
              <input
                id="phone_number"
                v-model="phoneNumber"
                type="tel"
                autocomplete="tel"
                required
                class="phone_input"
                :class="{ error: errors.phoneNumber }"
                placeholder="+1 (555) 123-4567"
                :disabled="loading"
              />
              <p v-if="errors.phoneNumber" class="error_text">{{ errors.phoneNumber }}</p>
            </div>

            <button type="submit" :disabled="loading || !phoneNumber" class="submit_button">
              <span v-if="loading" class="loading_content">
                <div class="loading_spinner"></div>
                Sending Code...
              </span>
              <span v-else class="button_content">
                <svg class="button_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"
                  />
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                </svg>
                Send Verification Code
              </span>
            </button>
          </form>
        </div>

        <!-- Step 2: OTP Verification -->
        <div v-if="step === 2" class="step_content">
          <div class="step_description">
            <p class="description_text">Enter the 6-digit code sent to</p>
            <p class="phone_display">{{ phoneNumber }}</p>
          </div>

          <form @submit.prevent="verifyCode" class="otp_form">
            <div class="otp_container">
              <div class="otp_inputs">
                <input
                  v-for="(digit, index) in 6"
                  :key="index"
                  v-model="otpCode[index]"
                  type="text"
                  maxlength="1"
                  class="otp_input"
                  :class="{ error: errors.otp }"
                  @input="handleOtpInput($event, index)"
                  @keydown="handleOtpKeydown($event, index)"
                  @paste="handleOtpPaste"
                  ref="otpInputs"
                  :disabled="loading"
                />
              </div>
              <p v-if="errors.otp" class="error_text">{{ errors.otp }}</p>
            </div>

            <div class="resend_section">
              <p class="resend_text">
                Didn't receive the code?
                <button
                  @click="resendCode"
                  :disabled="resendCooldown > 0 || loading"
                  type="button"
                  class="resend_button"
                >
                  {{ resendCooldown > 0 ? `Resend in ${resendCooldown}s` : 'Resend Code' }}
                </button>
              </p>
            </div>

            <div class="action_buttons">
              <button @click="step = 1" type="button" class="back_button">
                <svg class="back_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
                    clip-rule="evenodd"
                  />
                </svg>
                Back
              </button>
              <button
                type="submit"
                :disabled="loading || otpCode.join('').length !== 6"
                class="verify_button"
              >
                <span v-if="loading" class="loading_content">
                  <div class="loading_spinner"></div>
                  Verifying...
                </span>
                <span v-else class="button_content">
                  <svg class="button_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  Verify Code
                </span>
              </button>
            </div>
          </form>
        </div>

        <!-- Success State -->
        <div v-if="step === 3" class="step_content">
          <div class="success_content">
            <div class="success_icon">
              <svg fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <h3 class="success_title">Phone Verified!</h3>
            <p class="success_text">Your phone number has been successfully verified.</p>
            <button @click="closeModal" class="success_button">Continue</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

interface Props {
  isOpen: boolean
}

defineProps<Props>()

const emit = defineEmits<{
  close: []
  success: [phoneNumber: string]
}>()

const authStore = useAuthStore()
const toast = useToast()

const step = ref(1)
const phoneNumber = ref('')
const otpCode = reactive(['', '', '', '', '', ''])
const loading = ref(false)
const resendCooldown = ref(0)
const otpInputs = ref<HTMLInputElement[]>([])

const errors = reactive({
  phoneNumber: '',
  otp: '',
})

let resendTimer: number | null = null

const validatePhoneNumber = (phone: string) => {
  const phoneRegex = /^\+?[1-9]\d{1,14}$/
  return phoneRegex.test(phone.replace(/\D/g, ''))
}

const handleOverlayClick = () => {
  if (!loading.value) {
    closeModal()
  }
}

const closeModal = () => {
  if (!loading.value) {
    emit('close')
    resetForm()
  }
}

const resetForm = () => {
  step.value = 1
  phoneNumber.value = ''
  otpCode.splice(0, 6, '', '', '', '', '', '')
  errors.phoneNumber = ''
  errors.otp = ''
  loading.value = false
}

const sendVerificationCode = async () => {
  errors.phoneNumber = ''

  if (!phoneNumber.value) {
    errors.phoneNumber = 'Phone number is required'
    return
  }

  if (!validatePhoneNumber(phoneNumber.value)) {
    errors.phoneNumber = 'Please enter a valid phone number'
    return
  }

  loading.value = true

  try {
    const result = await authStore.sendPhoneVerification(phoneNumber.value)
    if (result.success) {
      step.value = 2
      toast.showToast('Verification code sent!', 'success')
      startResendCooldown()
      // Focus first OTP input
      await nextTick()
      if (otpInputs.value[0]) {
        otpInputs.value[0].focus()
      }
    } else {
      errors.phoneNumber = result.error || 'Failed to send verification code'
      toast.showToast(result.error || 'Failed to send verification code', 'error')
    }
  } catch {
    errors.phoneNumber = 'Failed to send verification code'
    toast.showToast('Failed to send verification code', 'error')
  } finally {
    loading.value = false
  }
}

const verifyCode = async () => {
  errors.otp = ''

  const code = otpCode.join('')
  if (code.length !== 6) {
    errors.otp = 'Please enter the complete 6-digit code'
    return
  }

  loading.value = true

  try {
    const result = await authStore.verifyPhoneCode(phoneNumber.value, code)
    if (result.success) {
      step.value = 3
      toast.showToast('Phone number verified successfully!', 'success')
      emit('success', phoneNumber.value)
    } else {
      errors.otp = result.error || 'Verification failed'
      toast.showToast(result.error || 'Verification failed', 'error')
    }
  } catch {
    errors.otp = 'Failed to verify code'
    toast.showToast('Failed to verify code', 'error')
  } finally {
    loading.value = false
  }
}

const resendCode = async () => {
  if (resendCooldown.value > 0 || loading.value) return

  loading.value = true

  try {
    const result = await authStore.sendPhoneVerification(phoneNumber.value)
    if (result.success) {
      toast.showToast('New verification code sent!', 'success')
      startResendCooldown()
      // Clear OTP inputs
      otpCode.splice(0, 6, '', '', '', '', '', '')
      // Focus first input
      await nextTick()
      if (otpInputs.value[0]) {
        otpInputs.value[0].focus()
      }
    } else {
      toast.showToast(result.error || 'Failed to resend code', 'error')
    }
  } catch {
    toast.showToast('Failed to resend code', 'error')
  } finally {
    loading.value = false
  }
}

const startResendCooldown = () => {
  resendCooldown.value = 60
  resendTimer = setInterval(() => {
    resendCooldown.value--
    if (resendCooldown.value <= 0) {
      if (resendTimer) {
        clearInterval(resendTimer)
        resendTimer = null
      }
    }
  }, 1000)
}

const handleOtpInput = (event: Event, index: number) => {
  const target = event.target as HTMLInputElement
  const value = target.value

  // Only allow digits
  if (!/^\d*$/.test(value)) {
    target.value = ''
    return
  }

  otpCode[index] = value

  // Move to next input if value entered
  if (value && index < 5) {
    nextTick(() => {
      if (otpInputs.value[index + 1]) {
        otpInputs.value[index + 1].focus()
      }
    })
  }
}

const handleOtpKeydown = (event: KeyboardEvent, index: number) => {
  const target = event.target as HTMLInputElement

  // Handle backspace
  if (event.key === 'Backspace' && !target.value && index > 0) {
    nextTick(() => {
      if (otpInputs.value[index - 1]) {
        otpInputs.value[index - 1].focus()
      }
    })
  }
}

const handleOtpPaste = (event: ClipboardEvent) => {
  event.preventDefault()
  const pastedData = event.clipboardData?.getData('text/plain')

  if (pastedData && /^\d{6}$/.test(pastedData)) {
    const digits = pastedData.split('')
    digits.forEach((digit, index) => {
      if (index < 6) {
        otpCode[index] = digit
      }
    })
  }
}

onUnmounted(() => {
  if (resendTimer) {
    clearInterval(resendTimer)
  }
})
</script>

<style scoped>
.modal_overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal_container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  max-width: 480px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.modal_content {
  padding: 2rem;
}

.modal_header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(229, 231, 235, 0.5);
}

.modal_title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.close_button {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close_button:hover {
  background: rgba(107, 114, 128, 0.1);
  color: #374151;
}

.close_button svg {
  width: 1.25rem;
  height: 1.25rem;
}

.step_content {
  animation: fadeIn 0.3s ease-out;
}

.step_description {
  text-align: center;
  margin-bottom: 2rem;
}

.description_text {
  color: #6b7280;
  font-size: 1rem;
  margin: 0 0 0.5rem 0;
}

.phone_display {
  color: #111827;
  font-weight: 600;
  font-size: 1.125rem;
  margin: 0;
}

.form_group {
  margin-bottom: 1.5rem;
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

.phone_input {
  width: 100%;
  padding: 1rem 1.25rem;
  border: 2px solid rgba(229, 231, 235, 0.5);
  border-radius: 12px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
}

.phone_input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.phone_input.error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.phone_input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

.submit_button,
.verify_button {
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
  margin-top: 1rem;
}

.submit_button::before,
.verify_button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.submit_button:hover::before,
.verify_button:hover::before {
  left: 100%;
}

.submit_button:hover,
.verify_button:hover {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  transform: translateY(-2px);
  box-shadow: 0 12px 24px -6px rgba(59, 130, 246, 0.4);
}

.submit_button:disabled,
.verify_button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading_content,
.button_content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.loading_spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.button_icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* OTP Styles */
.otp_container {
  margin-bottom: 1.5rem;
}

.otp_inputs {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  margin-bottom: 1rem;
}

.otp_input {
  width: 3rem;
  height: 3.5rem;
  text-align: center;
  font-size: 1.25rem;
  font-weight: 600;
  border: 2px solid rgba(229, 231, 235, 0.5);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.otp_input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  transform: scale(1.05);
}

.otp_input.error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.otp_input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.resend_section {
  text-align: center;
  margin-bottom: 2rem;
}

.resend_text {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.resend_button {
  background: none;
  border: none;
  color: #3b82f6;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.2s ease;
}

.resend_button:hover:not(:disabled) {
  color: #2563eb;
}

.resend_button:disabled {
  color: #9ca3af;
  cursor: not-allowed;
  text-decoration: none;
}

.action_buttons {
  display: flex;
  gap: 1rem;
}

.back_button {
  flex: 1;
  padding: 1rem 1.5rem;
  background: rgba(229, 231, 235, 0.5);
  color: #374151;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.back_button:hover {
  background: rgba(229, 231, 235, 0.8);
  transform: translateY(-1px);
}

.back_icon {
  width: 1.25rem;
  height: 1.25rem;
}

.verify_button {
  flex: 2;
  margin-top: 0;
}

/* Success State */
.success_content {
  text-align: center;
  padding: 2rem 0;
}

.success_icon {
  width: 4rem;
  height: 4rem;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: white;
}

.success_icon svg {
  width: 2rem;
  height: 2rem;
}

.success_title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem 0;
}

.success_text {
  color: #6b7280;
  font-size: 1rem;
  margin: 0 0 2rem 0;
}

.success_button {
  width: 100%;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 16px -4px rgba(16, 185, 129, 0.3);
}

.success_button:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-2px);
  box-shadow: 0 12px 24px -6px rgba(16, 185, 129, 0.4);
}

/* Animations */
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

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .modal_container {
    background: rgba(17, 24, 39, 0.95);
    border-color: rgba(75, 85, 99, 0.3);
  }

  .modal_title {
    color: #f9fafb;
  }

  .description_text {
    color: #9ca3af;
  }

  .phone_display {
    color: #f9fafb;
  }

  .form_label {
    color: #f9fafb;
  }

  .phone_input,
  .otp_input {
    background: rgba(31, 41, 55, 0.9);
    border-color: rgba(75, 85, 99, 0.5);
    color: #f9fafb;
  }

  .phone_input:focus,
  .otp_input:focus {
    border-color: #60a5fa;
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
  }

  .back_button {
    background: rgba(75, 85, 99, 0.5);
    color: #f9fafb;
  }

  .back_button:hover {
    background: rgba(75, 85, 99, 0.8);
  }

  .resend_text {
    color: #9ca3af;
  }

  .resend_button {
    color: #60a5fa;
  }

  .resend_button:hover:not(:disabled) {
    color: #93c5fd;
  }

  .success_title {
    color: #f9fafb;
  }

  .success_text {
    color: #9ca3af;
  }
}

/* Responsive design */
@media (max-width: 480px) {
  .modal_content {
    padding: 1.5rem;
  }

  .modal_title {
    font-size: 1.25rem;
  }

  .otp_inputs {
    gap: 0.5rem;
  }

  .otp_input {
    width: 2.5rem;
    height: 3rem;
    font-size: 1rem;
  }

  .action_buttons {
    flex-direction: column;
  }

  .back_button,
  .verify_button {
    flex: none;
  }
}
</style>
