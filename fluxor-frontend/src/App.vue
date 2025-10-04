<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const theme = ref('light')
const authStore = useAuthStore()
const isLoggingOut = ref(false)

const handleLogout = async () => {
  if (isLoggingOut.value) return // Prevent multiple clicks

  isLoggingOut.value = true
  try {
    await authStore.logout()
    console.log('Logout completed successfully')
  } catch (error) {
    console.error('Logout failed:', error)
  } finally {
    isLoggingOut.value = false
  }
}

const setTheme = (value: string) => {
  theme.value = value
  document.documentElement.setAttribute('data_theme', value)
  localStorage.setItem('theme', value)
}

const toggleTheme = () => {
  setTheme(theme.value === 'dark' ? 'light' : 'dark')
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(async () => {
  // Initialize theme
  const saved = localStorage.getItem('theme')
  if (saved === 'light' || saved === 'dark') {
    setTheme(saved)
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    setTheme('dark')
  } else {
    setTheme('light')
  }

  // Authentication is now handled by router guards
  console.log('App mounted, authentication will be handled by router')
})
</script>

<template>
  <div class="app_container">
    <!-- Animated background particles -->
    <div class="background_particles">
      <div class="particle particle_1"></div>
      <div class="particle particle_2"></div>
      <div class="particle particle_3"></div>
      <div class="particle particle_4"></div>
      <div class="particle particle_5"></div>
    </div>

    <header class="header">
      <div class="header_background">
        <div class="header_shapes">
          <div class="header_shape header_shape_1"></div>
          <div class="header_shape header_shape_2"></div>
          <div class="header_shape header_shape_3"></div>
        </div>
      </div>
      <div class="wrapper">
        <div class="header_left">
          <h1 class="app_title">
            <span class="gradient-text">Fluxor</span>
            <span class="app_subtitle">Trading</span>
          </h1>
          <div class="app_badge">
            <span class="badge_dot"></span>
            <span class="badge_text">Live Trading</span>
          </div>
          <!-- Show welcome message for authenticated users -->
          <div v-if="authStore.isAuthenticated && authStore.user" class="user_welcome">
            <span class="welcome_text">Welcome, {{ authStore.user.full_name }}</span>
          </div>
        </div>
        <nav class="header_nav">
          <!-- Show Home link only for unauthenticated users -->
          <RouterLink
            v-if="!authStore.isAuthenticated"
            to="/"
            class="nav-link"
            active-class="nav-link-active"
          >
            <svg class="nav_icon" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"
              />
            </svg>
            Home
          </RouterLink>

          <!-- Show different navigation based on auth status -->
          <template v-if="!authStore.isAuthenticated">
            <RouterLink to="/login" class="nav-link" active-class="nav-link-active">
              <svg class="nav_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M3 3a1 1 0 011 1v12a1 1 0 11-2 0V4a1 1 0 011-1zm7.707 3.293a1 1 0 010 1.414L9.414 9H17a1 1 0 110 2H9.414l1.293 1.293a1 1 0 01-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0z"
                  clip-rule="evenodd"
                />
              </svg>
              Sign In
            </RouterLink>
            <RouterLink
              to="/register"
              class="nav-link nav-link-primary"
              active-class="nav-link-active"
            >
              <svg class="nav_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z"
                />
              </svg>
              Sign Up
            </RouterLink>
          </template>

          <template v-else>
            <RouterLink to="/dashboard" class="nav-link" active-class="nav-link-active">
              <svg class="nav_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"
                />
              </svg>
              Dashboard
            </RouterLink>
            <RouterLink to="/profile" class="nav-link" active-class="nav-link-active">
              <svg class="nav_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                  clip-rule="evenodd"
                />
              </svg>
              Profile
            </RouterLink>
            <button @click="handleLogout" :disabled="isLoggingOut" class="nav-link nav-link-logout">
              <svg class="nav_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                  clip-rule="evenodd"
                />
              </svg>
              {{ isLoggingOut ? 'Signing Out...' : 'Sign Out' }}
            </button>
          </template>
        </nav>
      </div>
      <div class="theme_toggle_wrapper">
        <button
          class="theme_toggle_btn"
          @click="toggleTheme"
          :aria_label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
        >
          <svg v-if="theme === 'dark'" class="theme_icon" fill="currentColor" viewBox="0 0 20 20">
            <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
          </svg>
          <svg v-else class="theme_icon" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4.22 2.47a1 1 0 011.42 1.42l-.7.7a1 1 0 11-1.42-1.42l.7-.7zM18 9a1 1 0 100 2h-1a1 1 0 100-2h1zM5.64 4.22a1 1 0 00-1.42 1.42l.7.7a1 1 0 101.42-1.42l-.7-.7zM4 10a1 1 0 100 2H3a1 1 0 100-2h1zm1.64 7.78a1 1 0 001.42-1.42l-.7-.7a1 1 0 10-1.42 1.42l.7.7zM10 16a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zm7-6a7 7 0 11-14 0 7 7 0 0114 0z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>
    </header>

    <main class="main_content">
      <RouterView />
    </main>

    <!-- Floating action button -->
    <div class="floating_action">
      <button class="fab_button" @click="scrollToTop">
        <svg class="fab_icon" fill="currentColor" viewBox="0 0 20 20">
          <path
            fill-rule="evenodd"
            d="M3.293 9.707a1 1 0 010-1.414l6-6a1 1 0 011.414 0l6 6a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L4.707 9.707a1 1 0 01-1.414 0z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.app_container {
  position: relative;
  min-height: 100vh;
  overflow-x: hidden;
}

.background_particles {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.particle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
  animation: float 8s ease-in-out infinite;
}

.particle_1 {
  width: 80px;
  height: 80px;
  top: 10%;
  left: 5%;
  animation-delay: 0s;
}

.particle_2 {
  width: 60px;
  height: 60px;
  top: 70%;
  right: 10%;
  animation-delay: 2s;
}

.particle_3 {
  width: 40px;
  height: 40px;
  top: 40%;
  right: 20%;
  animation-delay: 4s;
}

.particle_4 {
  width: 100px;
  height: 100px;
  top: 20%;
  right: 60%;
  animation-delay: 6s;
}

.particle_5 {
  width: 50px;
  height: 50px;
  top: 80%;
  left: 20%;
  animation-delay: 8s;
}

.header {
  background: var(--color_surface);
  color: var(--color_text);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--color_border);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 0 8px 32px -8px rgba(0, 0, 0, 0.07);
  transition:
    background 0.3s,
    color 0.3s;
}

.header_background {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.header_shapes {
  position: relative;
  width: 100%;
  height: 100%;
}

.header_shape {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
  animation: float 6s ease-in-out infinite;
}

.header_shape_1 {
  width: 60px;
  height: 60px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.header_shape_2 {
  width: 40px;
  height: 40px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.header_shape_3 {
  width: 30px;
  height: 30px;
  top: 30%;
  right: 30%;
  animation-delay: 4s;
}

.wrapper {
  position: relative;
  z-index: 10;
  display: flex;
  place-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.header_left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.app_title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1f2937;
  margin: 0;
  letter-spacing: -0.025em;
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.app_subtitle {
  font-size: 1.25rem;
  font-weight: 600;
  color: #6b7280;
  opacity: 0.8;
}

.app_badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(16, 185, 129, 0.1));
  border: 1px solid rgba(34, 197, 94, 0.2);
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #059669;
}

.badge_dot {
  width: 6px;
  height: 6px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.badge_text {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.header_nav {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  font-weight: 500;
  font-size: 0.875rem;
  color: var(--color_text);
  text-decoration: none;
  transition:
    box-shadow 0.2s,
    transform 0.2s,
    text-decoration 0.2s;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.nav-link:hover,
.nav-link:focus {
  color: var(--color_text);
  background: none;
  text-decoration: underline;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.07);
  transform: translateY(-1px);
}

.nav-link:hover::before {
  opacity: 1;
}

.nav-link-active {
  color: var(--color_primary);
  font-weight: 600;
  text-decoration: underline;
}

.nav-link-primary {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.nav-link-primary:hover {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
}

.nav_icon {
  width: 1rem;
  height: 1rem;
  transition: transform 0.3s ease;
}

.nav-link:hover .nav_icon {
  transform: scale(1.1);
}

.main_content {
  min-height: calc(100vh - 80px);
  padding: 2rem 0;
  position: relative;
}

/* Responsive Design */
@media (max-width: 768px) {
  .wrapper {
    padding: 0 1rem;
    flex-direction: column;
    gap: 1rem;
  }

  .header_left {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }

  .app_title {
    font-size: 1.5rem;
  }

  .app_subtitle {
    font-size: 1rem;
  }

  .app_badge {
    font-size: 0.65rem;
    padding: 0.2rem 0.6rem;
  }

  .header_nav {
    width: 100%;
    justify-content: center;
    gap: 0.25rem;
  }

  .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }

  .nav_icon {
    width: 0.875rem;
    height: 0.875rem;
  }
}

@media (min-width: 1024px) {
  .header {
    padding: 1.25rem 0;
  }

  .wrapper {
    padding: 0 2rem;
  }

  .app_title {
    font-size: 2rem;
  }

  .app_subtitle {
    font-size: 1.375rem;
  }

  .header_nav {
    gap: 1rem;
  }

  .nav-link {
    padding: 0.875rem 1.25rem;
    font-size: 0.9rem;
  }

  .main_content {
    padding: 3rem 0;
  }
}

/* Animations */
@keyframes float {
  0%,
  100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-10px) rotate(180deg);
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

/* Hover effects for header */
.header:hover {
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 12px 40px -12px rgba(0, 0, 0, 0.15);
}

/* Focus states */
.nav-link:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Floating Action Button */
.floating_action {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 100;
}

.fab_button {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border: none;
  color: white;
  cursor: pointer;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.fab_button::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.fab_button:hover {
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 12px 40px rgba(59, 130, 246, 0.4);
}

.fab_button:hover::before {
  opacity: 1;
}

.fab_button:active {
  transform: translateY(-2px) scale(1.02);
}

.fab_icon {
  width: 24px;
  height: 24px;
  transition: transform 0.3s ease;
}

.fab_button:hover .fab_icon {
  transform: translateY(-2px);
}

/* Enhanced header hover effects */
.header:hover {
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 12px 40px -12px rgba(0, 0, 0, 0.15);
}

/* Enhanced navigation link effects */
.nav-link {
  position: relative;
  overflow: hidden;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.nav-link:hover::after {
  width: 80%;
}

.nav-link-active::after {
  width: 80%;
}

.nav-link-logout {
  background: none;
  border: none;
  cursor: pointer;
  color: #ef4444;
  transition: all 0.3s ease;
}

.nav-link-logout:hover:not(:disabled) {
  color: #dc2626;
  background: rgba(239, 68, 68, 0.1);
}

.nav-link-logout:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.user_welcome {
  margin-top: 0.5rem;
}

.welcome_text {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .header {
    background: rgba(17, 24, 39, 0.95);
    border-bottom-color: rgba(75, 85, 99, 0.3);
  }

  .app_title {
    color: #f9fafb;
  }

  .app_subtitle {
    color: #9ca3af;
  }

  .nav-link {
    color: #d1d5db;
  }

  .nav-link:hover {
    color: #60a5fa;
    background: rgba(59, 130, 246, 0.1);
  }

  .nav-link-active {
    color: #60a5fa;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(147, 51, 234, 0.2));
    border-color: rgba(59, 130, 246, 0.3);
  }

  .particle {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(147, 51, 234, 0.15));
  }
}

.theme_toggle_wrapper {
  position: absolute;
  top: 1.5rem;
  right: 2.5rem;
  z-index: 100;
}
.theme_toggle_btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: background 0.2s;
  outline: none;
}
.theme_toggle_btn:focus-visible {
  outline: 2px solid var(--color_primary);
  outline-offset: 2px;
  background: var(--color_surface_alt);
}
.theme_icon {
  width: 1.7rem;
  height: 1.7rem;
  color: var(--color_text);
  transition: color 0.2s;
}
</style>
