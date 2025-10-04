<template>
  <div class="firebase-login-page">
    <div class="login-container">
      <div class="login-header">
        <h1 class="login-title">Welcome to Fluxor</h1>
        <p class="login-subtitle">Your cryptocurrency trading platform</p>
      </div>

      <FirebaseAuth
        :default-mode="defaultMode"
        :redirect-to="redirectTo"
        class="auth-component"
      />

      <div class="login-footer">
        <p class="footer-text">
          By continuing, you agree to our
          <a href="/terms" class="footer-link">Terms of Service</a>
          and
          <a href="/privacy" class="footer-link">Privacy Policy</a>
        </p>
      </div>
    </div>

    <!-- Background Elements -->
    <div class="background-elements">
      <div class="crypto-bg crypto-1">₿</div>
      <div class="crypto-bg crypto-2">Ξ</div>
      <div class="crypto-bg crypto-3">₳</div>
      <div class="crypto-bg crypto-4">●</div>
      <div class="crypto-bg crypto-5">♦</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import FirebaseAuth from '@/components/FirebaseAuth.vue'

const route = useRoute()

// Get default mode from route query or default to login
const defaultMode = computed(() => {
  const mode = route.query.mode as string
  return mode === 'register' ? 'register' : 'login'
})

// Get redirect URL from route query or default to dashboard
const redirectTo = computed(() => {
  return (route.query.redirect as string) || '/dashboard'
})
</script>

<style scoped>
.firebase-login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

.login-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
  max-width: 500px;
  width: 100%;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-title {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 0.5rem 0;
}

.login-subtitle {
  color: #6b7280;
  font-size: 1.1rem;
  margin: 0;
}

.auth-component {
  margin-bottom: 2rem;
}

.login-footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.footer-text {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
  line-height: 1.5;
}

.footer-link {
  color: #6366f1;
  text-decoration: none;
  font-weight: 500;
}

.footer-link:hover {
  text-decoration: underline;
}

/* Background Elements */
.background-elements {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

.crypto-bg {
  position: absolute;
  font-size: 8rem;
  color: rgba(255, 255, 255, 0.1);
  font-weight: bold;
  animation: float 20s infinite ease-in-out;
}

.crypto-1 {
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.crypto-2 {
  top: 20%;
  right: 15%;
  animation-delay: 4s;
}

.crypto-3 {
  bottom: 20%;
  left: 20%;
  animation-delay: 8s;
}

.crypto-4 {
  bottom: 30%;
  right: 25%;
  animation-delay: 12s;
}

.crypto-5 {
  top: 60%;
  left: 50%;
  animation-delay: 16s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.1;
  }
  25% {
    transform: translateY(-20px) rotate(5deg);
    opacity: 0.2;
  }
  50% {
    transform: translateY(-40px) rotate(0deg);
    opacity: 0.15;
  }
  75% {
    transform: translateY(-20px) rotate(-5deg);
    opacity: 0.2;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .firebase-login-page {
    padding: 1rem;
  }

  .login-container {
    padding: 2rem;
  }

  .login-title {
    font-size: 2rem;
  }

  .crypto-bg {
    font-size: 4rem;
  }
}

@media (max-width: 480px) {
  .login-container {
    padding: 1.5rem;
  }

  .login-title {
    font-size: 1.75rem;
  }
}
</style>
