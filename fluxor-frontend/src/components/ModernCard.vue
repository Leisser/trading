<template>
  <div :class="['modern_card', `modern_card_${variant}`, { modern_card_hoverable: hoverable }]">
    <div v-if="header" class="card_header">
      <div class="header_content">
        <h3 v-if="title" class="card_title">{{ title }}</h3>
        <p v-if="subtitle" class="card_subtitle">{{ subtitle }}</p>
      </div>
      <div v-if="$slots.headerAction" class="header_action">
        <slot name="headerAction" />
      </div>
    </div>

    <div class="card_content">
      <slot />
    </div>

    <div v-if="$slots.footer" class="card_footer">
      <slot name="footer" />
    </div>

    <div class="card_glow"></div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'default' | 'premium' | 'glass' | 'gradient'
  hoverable?: boolean
  title?: string
  subtitle?: string
  header?: boolean
}

withDefaults(defineProps<Props>(), {
  variant: 'default',
  hoverable: false,
})
</script>

<style scoped>
.modern_card {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.modern_card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(147, 51, 234, 0.05));
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.modern_card_hoverable:hover {
  transform: translateY(-4px);
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modern_card_hoverable:hover::before {
  opacity: 1;
}

/* Variants */
.modern_card_default {
  background: white;
  border: 1px solid rgba(229, 231, 235, 0.5);
}

.modern_card_premium {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.8));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modern_card_premium::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
}

.modern_card_glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.modern_card_gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
}

/* Header */
.card_header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem 1.5rem 0;
  border-bottom: 1px solid rgba(229, 231, 235, 0.3);
  margin-bottom: 1rem;
}

.modern_card_gradient .card_header {
  border-bottom-color: rgba(255, 255, 255, 0.2);
}

.header_content {
  flex: 1;
}

.card_title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
  line-height: 1.4;
}

.modern_card_gradient .card_title {
  color: white;
}

.card_subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.modern_card_gradient .card_subtitle {
  color: rgba(255, 255, 255, 0.8);
}

.header_action {
  flex-shrink: 0;
  margin-left: 1rem;
}

/* Content */
.card_content {
  padding: 0 1.5rem 1.5rem;
  position: relative;
  z-index: 1;
}

/* Footer */
.card_footer {
  padding: 1rem 1.5rem 1.5rem;
  border-top: 1px solid rgba(229, 231, 235, 0.3);
  margin-top: 1rem;
  background: rgba(249, 250, 251, 0.5);
}

.modern_card_gradient .card_footer {
  border-top-color: rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
}

/* Glow effect */
.card_glow {
  position: absolute;
  inset: 0;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.modern_card_hoverable:hover .card_glow {
  opacity: 1;
}

/* Focus states */
.modern_card:focus-within {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .modern_card_default {
    background: #1f2937;
    border-color: rgba(75, 85, 99, 0.5);
  }

  .card_title {
    color: #f9fafb;
  }

  .card_subtitle {
    color: #9ca3af;
  }

  .card_footer {
    background: rgba(31, 41, 55, 0.5);
    border-top-color: rgba(75, 85, 99, 0.3);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .card_header {
    padding: 1rem 1rem 0;
  }

  .card_content {
    padding: 0 1rem 1rem;
  }

  .card_footer {
    padding: 1rem;
  }

  .card_title {
    font-size: 1.125rem;
  }
}
</style>
