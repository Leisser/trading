<template>
  <button
    :class="['modern_button', `modern_button_${variant}`, { modern_button_loading: loading }]"
    :disabled="disabled || loading"
    @click="$emit('click')"
  >
    <div class="button_content">
      <svg v-if="icon && !loading" class="button_icon" fill="currentColor" viewBox="0 0 20 20">
        <path
          v-if="icon === 'arrow-right'"
          d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
        />
        <path
          v-else-if="icon === 'plus'"
          fill-rule="evenodd"
          d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
          clip-rule="evenodd"
        />
        <path
          v-else-if="icon === 'check'"
          fill-rule="evenodd"
          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
          clip-rule="evenodd"
        />
      </svg>

      <div v-if="loading" class="loading_spinner">
        <svg
          class="animate-spin h-5 w-5"
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
      </div>

      <span class="button_text">
        <slot>{{ text }}</slot>
      </span>
    </div>

    <div class="button_ripple"></div>
  </button>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning'
  size?: 'sm' | 'md' | 'lg'
  icon?: 'arrow-right' | 'plus' | 'check'
  loading?: boolean
  disabled?: boolean
  text?: string
}

withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  loading: false,
  disabled: false,
})

defineEmits<{
  click: []
}>()
</script>

<style scoped>
.modern_button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  text-decoration: none;
  min-width: 120px;
  height: 44px;
  padding: 0 1.5rem;
}

.modern_button::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.modern_button:hover::before {
  opacity: 1;
}

.modern_button:active {
  transform: translateY(1px);
}

.modern_button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Variants */
.modern_button_primary {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.modern_button_primary:hover {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
  transform: translateY(-2px);
}

.modern_button_secondary {
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  color: #374151;
  border: 1px solid #d1d5db;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.modern_button_secondary:hover {
  background: linear-gradient(135deg, #e5e7eb, #d1d5db);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

.modern_button_success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.modern_button_success:hover {
  background: linear-gradient(135deg, #059669, #047857);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
  transform: translateY(-2px);
}

.modern_button_danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.modern_button_danger:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  box-shadow: 0 8px 20px rgba(239, 68, 68, 0.4);
  transform: translateY(-2px);
}

.modern_button_warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.modern_button_warning:hover {
  background: linear-gradient(135deg, #d97706, #b45309);
  box-shadow: 0 8px 20px rgba(245, 158, 11, 0.4);
  transform: translateY(-2px);
}

/* Sizes */
.modern_button_sm {
  height: 36px;
  padding: 0 1rem;
  font-size: 0.75rem;
  min-width: 100px;
}

.modern_button_lg {
  height: 52px;
  padding: 0 2rem;
  font-size: 1rem;
  min-width: 140px;
}

/* Content */
.button_content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  z-index: 1;
}

.button_icon {
  width: 1rem;
  height: 1rem;
  transition: transform 0.3s ease;
}

.modern_button:hover .button_icon {
  transform: translateX(2px);
}

.button_text {
  font-weight: 600;
  letter-spacing: 0.025em;
}

/* Loading state */
.modern_button_loading {
  cursor: wait;
}

.loading_spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Ripple effect */
.button_ripple {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: scale(0);
  animation: ripple 0.6s linear;
  pointer-events: none;
}

@keyframes ripple {
  to {
    transform: scale(4);
    opacity: 0;
  }
}

/* Focus states */
.modern_button:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .modern_button_secondary {
    background: linear-gradient(135deg, #374151, #4b5563);
    color: #f9fafb;
    border-color: #6b7280;
  }

  .modern_button_secondary:hover {
    background: linear-gradient(135deg, #4b5563, #6b7280);
  }
}
</style>
