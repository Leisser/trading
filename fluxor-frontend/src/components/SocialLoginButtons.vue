<template>
  <div class="social_login_container">
    <div class="divider">
      <span class="divider_text">or continue with</span>
    </div>

    <div class="social_buttons">
      <button
        @click="handleGoogleLogin"
        :disabled="props.loading"
        class="social_button google_button"
        type="button"
      >
        <svg class="social_icon" viewBox="0 0 24 24">
          <path
            fill="#4285F4"
            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
          />
          <path
            fill="#34A853"
            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
          />
          <path
            fill="#FBBC05"
            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
          />
          <path
            fill="#EA4335"
            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
          />
        </svg>
        <span class="social_text">Continue with Google</span>
      </button>

      <button
        @click="handleAppleLogin"
        :disabled="props.loading"
        class="social_button apple_button"
        type="button"
      >
        <svg class="social_icon" viewBox="0 0 24 24">
          <path
            d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"
          />
        </svg>
        <span class="social_text">Continue with Apple</span>
      </button>

      <button
        @click="handlePhoneLogin"
        :disabled="props.loading"
        class="social_button phone_button"
        type="button"
      >
        <svg class="social_icon" fill="currentColor" viewBox="0 0 20 20">
          <path
            d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"
          />
        </svg>
        <span class="social_text">Continue with Phone</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useToast } from '@/composables/useToast'

interface Props {
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
})

const emit = defineEmits<{
  phoneLogin: []
}>()

const toast = useToast()

const handleGoogleLogin = async () => {
  try {
    // For now, we'll show a placeholder message since Google OAuth requires setup
    // In a real implementation, you would integrate with Google OAuth
    toast.showToast('Google login coming soon!', 'info')
    // const result = await authStore.socialLogin('google', accessToken, userData)
    // if (result.success) {
    //   toast.showToast('Google login successful!', 'success')
    // } else {
    //   toast.showToast(result.error, 'error')
    // }
  } catch {
    toast.showToast('Google login failed', 'error')
  }
}

const handleAppleLogin = async () => {
  try {
    // For now, we'll show a placeholder message since Apple Sign-In requires setup
    // In a real implementation, you would integrate with Apple Sign-In
    toast.showToast('Apple login coming soon!', 'info')
    // const result = await authStore.socialLogin('apple', accessToken, userData)
    // if (result.success) {
    //   toast.showToast('Apple login successful!', 'success')
    // } else {
    //   toast.showToast(result.error, 'error')
    // }
  } catch {
    toast.showToast('Apple login failed', 'error')
  }
}

const handlePhoneLogin = () => {
  emit('phoneLogin')
}
</script>

<style scoped>
.social_login_container {
  width: 100%;
  margin: 1.5rem 0;
}

.divider {
  position: relative;
  text-align: center;
  margin: 1.5rem 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(156, 163, 175, 0.5), transparent);
}

.divider_text {
  background: rgba(255, 255, 255, 0.95);
  padding: 0 1rem;
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

.social_buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.social_button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.875rem 1.25rem;
  border: 2px solid rgba(229, 231, 235, 0.5);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.social_button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.5s;
}

.social_button:hover::before {
  left: 100%;
}

.social_button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.1);
}

.social_button:active {
  transform: translateY(0);
}

.social_button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.social_icon {
  width: 1.5rem;
  height: 1.5rem;
  flex-shrink: 0;
}

.social_text {
  font-weight: 600;
  color: #374151;
}

/* Google Button Specific */
.google_button {
  border-color: rgba(66, 133, 244, 0.2);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
}

.google_button:hover {
  border-color: rgba(66, 133, 244, 0.4);
  background: linear-gradient(135deg, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0.95));
  box-shadow: 0 8px 16px -4px rgba(66, 133, 244, 0.2);
}

/* Apple Button Specific */
.apple_button {
  border-color: rgba(0, 0, 0, 0.2);
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.95), rgba(0, 0, 0, 0.9));
  color: white;
}

.apple_button:hover {
  border-color: rgba(0, 0, 0, 0.4);
  background: linear-gradient(135deg, rgba(0, 0, 0, 1), rgba(0, 0, 0, 0.95));
  box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.3);
}

.apple_button .social_text {
  color: white;
}

.apple_button .social_icon {
  fill: white;
}

/* Phone Button Specific */
.phone_button {
  border-color: rgba(59, 130, 246, 0.2);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
}

.phone_button:hover {
  border-color: rgba(59, 130, 246, 0.4);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(59, 130, 246, 0.1));
  box-shadow: 0 8px 16px -4px rgba(59, 130, 246, 0.2);
}

.phone_button .social_icon {
  color: #3b82f6;
}

.phone_button .social_text {
  color: #3b82f6;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .divider_text {
    background: rgba(17, 24, 39, 0.95);
    color: #9ca3af;
  }

  .social_button {
    background: rgba(31, 41, 55, 0.9);
    border-color: rgba(75, 85, 99, 0.5);
  }

  .social_text {
    color: #f9fafb;
  }

  .google_button {
    border-color: rgba(66, 133, 244, 0.3);
    background: rgba(31, 41, 55, 0.9);
  }

  .google_button:hover {
    border-color: rgba(66, 133, 244, 0.5);
    background: rgba(31, 41, 55, 1);
  }

  .phone_button {
    border-color: rgba(59, 130, 246, 0.3);
    background: rgba(31, 41, 55, 0.9);
  }

  .phone_button:hover {
    border-color: rgba(59, 130, 246, 0.5);
    background: rgba(31, 41, 55, 1);
  }

  .phone_button .social_text {
    color: #60a5fa;
  }

  .phone_button .social_icon {
    color: #60a5fa;
  }
}

/* Focus states for accessibility */
.social_button:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Responsive design */
@media (max-width: 480px) {
  .social_button {
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
  }

  .social_icon {
    width: 1.25rem;
    height: 1.25rem;
  }
}
</style>
