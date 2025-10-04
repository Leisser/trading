<template>
  <div class="admin_container">
    <div class="admin_background">
      <div class="admin_shapes">
        <div class="admin_shape admin_shape_1"></div>
        <div class="admin_shape admin_shape_2"></div>
        <div class="admin_shape admin_shape_3"></div>
      </div>
    </div>
    <header class="admin_header">
      <div class="header_content">
        <div class="header_left">
          <svg class="header_icon animate-glow" fill="none" viewBox="0 0 32 32">
            <circle cx="16" cy="16" r="14" stroke="#6366f1" stroke-width="3" fill="#a5b4fc" />
            <path
              d="M16 10v6l4 2"
              stroke="#6366f1"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <h1 class="header_title gradient-text">Admin Dashboard</h1>
        </div>
        <router-link to="/dashboard" class="btn-secondary text-sm">
          <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3a1 1 0 00.293.707l2 2a1 1 0 001.414-1.414L11 9.586V7z"
              clip-rule="evenodd"
            />
          </svg>
          Back to Trading
        </router-link>
      </div>
    </header>
    <main class="admin_main">
      <div class="admin_grid">
        <!-- Users -->
        <div class="admin_card glass-card animate-3d">
          <h2 class="card_title gradient-text">Users</h2>
          <div v-if="users.length > 0" class="table_wrapper">
            <table class="admin_table">
              <thead class="table_header sticky-header">
                <tr>
                  <th>Email</th>
                  <th>Name</th>
                  <th>Role</th>
                  <th>KYC</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(user, index) in users"
                  :key="user.id"
                  :class="{ zebra: index % 2 === 1 }"
                >
                  <td>{{ user.email }}</td>
                  <td>{{ user.full_name }}</td>
                  <td>
                    <span
                      class="role_chip"
                      :class="user.role === 'admin' ? 'chip_admin' : 'chip_user'"
                    >
                      <svg
                        v-if="user.role === 'admin'"
                        class="chip_icon"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          d="M10 2a2 2 0 012 2v2h2a2 2 0 012 2v2h-2v2h2v2a2 2 0 01-2 2h-2v2a2 2 0 01-2 2 2 2 0 01-2-2v-2H6a2 2 0 01-2-2v-2h2v-2H4V8a2 2 0 012-2h2V4a2 2 0 012-2z"
                        />
                      </svg>
                      <svg v-else class="chip_icon" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 3a3 3 0 110 6 3 3 0 010-6zm0 8a5 5 0 00-4.546 2.916A7.963 7.963 0 0010 18a7.963 7.963 0 004.546-1.084A5 5 0 0010 13z"
                        />
                      </svg>
                      {{ user.role }}
                    </span>
                  </td>
                  <td>
                    <span
                      class="kyc_chip"
                      :class="user.kyc_verified ? 'chip_verified animate-glow' : 'chip_unverified'"
                    >
                      <svg
                        v-if="user.kyc_verified"
                        class="chip_icon"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      <svg v-else class="chip_icon" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          fill-rule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3a1 1 0 00.293.707l2 2a1 1 0 001.414-1.414L11 9.586V7z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      {{ user.kyc_verified ? 'Verified' : 'Unverified' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="empty_state">
            <svg class="empty_icon" fill="none" viewBox="0 0 48 48">
              <circle cx="24" cy="24" r="22" stroke="#a5b4fc" stroke-width="4" fill="#f3f4f6" />
              <path
                d="M16 32c2-2 6-2 8 0s6 2 8 0"
                stroke="#6366f1"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
            <div class="empty_title">No users found</div>
            <div class="empty_description">Invite new users to get started.</div>
          </div>
        </div>
        <!-- Trades -->
        <div class="admin_card glass-card animate-3d">
          <h2 class="card_title gradient-text">Trades</h2>
          <div v-if="trades.length > 0" class="table_wrapper">
            <table class="admin_table">
              <thead class="table_header sticky-header">
                <tr>
                  <th>User</th>
                  <th>Type</th>
                  <th>Amount</th>
                  <th>Price</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(trade, index) in trades"
                  :key="trade.id"
                  :class="{ zebra: index % 2 === 1 }"
                >
                  <td>{{ trade.user_email || 'N/A' }}</td>
                  <td>
                    <span
                      class="trade_chip"
                      :class="trade.trade_type === 'buy' ? 'chip_buy' : 'chip_sell'"
                    >
                      <svg
                        v-if="trade.trade_type === 'buy'"
                        class="chip_icon"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" />
                      </svg>
                      <svg v-else class="chip_icon" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M15 10a1 1 0 01-1 1H6a1 1 0 110-2h8a1 1 0 011 1z" />
                      </svg>
                      {{ trade.trade_type }}
                    </span>
                  </td>
                  <td>{{ trade.btc_amount }} BTC</td>
                  <td>${{ trade.usd_price }}</td>
                  <td>
                    <span
                      class="status_chip"
                      :class="
                        trade.status === 'completed'
                          ? 'chip_completed animate-glow'
                          : 'chip_pending'
                      "
                    >
                      <svg
                        v-if="trade.status === 'completed'"
                        class="chip_icon"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      <svg v-else class="chip_icon" fill="currentColor" viewBox="0 0 20 20">
                        <circle
                          cx="10"
                          cy="10"
                          r="8"
                          stroke="#fbbf24"
                          stroke-width="2"
                          fill="#fef3c7"
                        />
                      </svg>
                      {{ trade.status }}
                    </span>
                  </td>
                  <td>{{ formatDate(trade.timestamp) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="empty_state">
            <svg class="empty_icon" fill="none" viewBox="0 0 48 48">
              <circle cx="24" cy="24" r="22" stroke="#a5b4fc" stroke-width="4" fill="#f3f4f6" />
              <path
                d="M16 32c2-2 6-2 8 0s6 2 8 0"
                stroke="#6366f1"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
            <div class="empty_title">No trades found</div>
            <div class="empty_description">Trades will appear here as users trade.</div>
          </div>
        </div>
      </div>
      <!-- Floating Action Button -->
      <button class="fab" @click="openInviteModal">
        <svg class="fab_icon" fill="currentColor" viewBox="0 0 20 20">
          <path
            d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
          />
        </svg>
      </button>
      <!-- Confetti Animation (shown on success) -->
      <div v-if="showConfetti" class="confetti_overlay">
        <div class="confetti"></div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

interface User {
  id: number
  email: string
  full_name: string
  role: string
  kyc_verified: boolean
}

interface Trade {
  id: number
  user_email: string
  trade_type: string
  btc_amount: number
  usd_price: number
  status: string
  timestamp: string
}

const router = useRouter()
const authStore = useAuthStore()

// Define reactive variables for template
const users = ref<User[]>([])
const trades = ref<Trade[]>([])
const showConfetti = ref<boolean>(false)

const fetchUsers = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/accounts/users/')
    users.value = response.data.results || response.data
  } catch {
    users.value = []
  }
}

const fetchTrades = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/trades/')
    trades.value = response.data.results || response.data
  } catch {
    trades.value = []
  }
}

const openInviteModal = (): void => {
  showConfetti.value = true
  setTimeout(() => {
    showConfetti.value = false
  }, 1500)
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  if (!authStore.isAdmin) {
    router.push('/dashboard')
  }
  fetchUsers()
  fetchTrades()
})
</script>

<style scoped>
.admin_container {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}
.admin_background {
  position: absolute;
  inset: 0;
  background: var(--color_bg);
  z-index: 0;
  overflow: hidden;
}
.admin_shapes {
  position: absolute;
  inset: 0;
  z-index: 1;
}
.admin_shape {
  position: absolute;
  border-radius: 50%;
  background: var(--color_surface_alt);
  animation: float 8s ease-in-out infinite;
}
.admin_shape_1 {
  width: 220px;
  height: 220px;
  top: 8%;
  left: 8%;
  animation-delay: 0s;
}
.admin_shape_2 {
  width: 160px;
  height: 160px;
  bottom: 12%;
  right: 10%;
  animation-delay: 3s;
}
.admin_shape_3 {
  width: 100px;
  height: 100px;
  top: 50%;
  left: 60%;
  animation-delay: 6s;
}

.admin_header {
  position: relative;
  z-index: 10;
  background: var(--color_surface);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--color_border);
  box-shadow: 0 8px 32px -8px rgba(0, 0, 0, 0.07);
  padding: 1.5rem 0 1rem 0;
}
.header_content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header_left {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.header_icon {
  width: 2.5rem;
  height: 2.5rem;
  filter: drop-shadow(0 0 12px var(--color_secondary));
}
.animate-glow {
  animation: glow 2s infinite alternate;
}
@keyframes glow {
  0% {
    filter: drop-shadow(0 0 8px var(--color_secondary));
  }
  100% {
    filter: drop-shadow(0 0 24px var(--color_primary));
  }
}
.header_title {
  font-size: 2rem;
  font-weight: 900;
  letter-spacing: -0.025em;
  color: var(--color_primary);
}
.gradient-text {
  color: var(--color_primary);
  background: none;
  -webkit-background-clip: initial;
  -webkit-text-fill-color: initial;
  font-weight: 900;
}
.btn-secondary {
  background: var(--color_surface_alt);
  color: var(--color_text);
  font-weight: 600;
  padding: 0.5rem 1.25rem;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
  border: 1.5px solid var(--color_border);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition:
    box-shadow 0.2s,
    transform 0.2s;
}
.btn-secondary:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px) scale(1.03);
}
.btn_icon {
  width: 1rem;
  height: 1rem;
  margin-right: 0.5rem;
}
.admin_main {
  position: relative;
  z-index: 10;
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem 2rem 2rem;
}
.admin_grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2.5rem;
}
.admin_card {
  position: relative;
  z-index: 2;
  border-radius: 24px;
  box-shadow: 0 16px 48px -12px var(--color_primary);
  overflow: hidden;
  transition:
    transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
    box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.glass-card {
  background: var(--color_surface);
  backdrop-filter: blur(24px);
  border: 1.5px solid var(--color_border);
}
.animate-3d:hover {
  transform: perspective(800px) rotateY(4deg) scale(1.03);
  box-shadow: 0 32px 64px -16px var(--color_secondary);
}
.card_title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  letter-spacing: -0.01em;
  color: var(--color_primary);
}
.table_wrapper {
  overflow-x: auto;
  border-radius: 16px;
  box-shadow: 0 4px 24px -8px var(--color_secondary);
}
.admin_table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 600px;
  background: transparent;
}
.table_header {
  background: var(--color_surface_alt);
  position: sticky;
  top: 0;
  z-index: 5;
}
.table_header th {
  padding: 1rem 0.75rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--color_primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 2px solid var(--color_border);
  background: var(--color_surface);
  position: sticky;
  top: 0;
}
.admin_table td {
  padding: 1rem 0.75rem;
  font-size: 1rem;
  color: var(--color_text);
  background: var(--color_surface);
  border-bottom: 1px solid var(--color_border);
  transition: background 0.2s;
}
.zebra {
  background: var(--color_surface_alt) !important;
}
.role_chip,
.kyc_chip,
.trade_chip,
.status_chip {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.9rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
  box-shadow: 0 2px 8px -2px var(--color_secondary);
  transition:
    background 0.2s,
    color 0.2s,
    box-shadow 0.2s;
}
.chip_admin {
  background: var(--color_primary);
  color: var(--color_text_on_primary);
}
.chip_user {
  background: var(--color_surface_alt);
  color: var(--color_primary);
}
.chip_verified {
  background: var(--color_success);
  color: var(--color_text_on_primary);
  border: 1.5px solid var(--color_success);
}
.chip_unverified {
  background: var(--color_error);
  color: var(--color_text_on_primary);
  border: 1.5px solid var(--color_error);
}
.chip_buy {
  background: var(--color_success);
  color: var(--color_text_on_primary);
  border: 1.5px solid var(--color_success);
}
.chip_sell {
  background: var(--color_error);
  color: var(--color_text_on_primary);
  border: 1.5px solid var(--color_error);
}
.chip_completed {
  background: var(--color_warning);
  color: var(--color_text_on_surface);
  border: 1.5px solid var(--color_warning);
}
.chip_pending {
  background: var(--color_surface_alt);
  color: var(--color_primary);
  border: 1.5px solid var(--color_secondary);
}
.chip_icon {
  width: 1rem;
  height: 1rem;
  margin-right: 0.3rem;
}
.animate-glow {
  animation: glow 2s infinite alternate;
}

.empty_state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--color_primary);
}
.empty_icon {
  width: 3rem;
  height: 3rem;
  margin: 0 auto 1rem;
  display: block;
}
.empty_title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}
.empty_description {
  font-size: 0.95rem;
  color: var(--color_text_secondary);
}
.fab {
  position: fixed;
  bottom: 2.5rem;
  right: 2.5rem;
  z-index: 100;
  background: var(--color_primary);
  color: var(--color_text_on_primary);
  border: none;
  border-radius: 50%;
  width: 64px;
  height: 64px;
  box-shadow: 0 8px 32px -8px var(--color_primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  cursor: pointer;
  transition:
    box-shadow 0.2s,
    transform 0.2s;
}
.fab:hover {
  box-shadow: 0 16px 48px -12px var(--color_secondary);
  transform: scale(1.08);
}
.fab_icon {
  width: 2rem;
  height: 2rem;
}
.confetti_overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
}
.confetti {
  width: 100vw;
  height: 100vh;
  background: url('https://svgshare.com/i/12dA.svg') repeat top center;
  animation: confetti-fall 1.5s linear;
}
@keyframes confetti-fall {
  0% {
    background-position-y: -100vh;
    opacity: 1;
  }
  100% {
    background-position-y: 0;
    opacity: 0;
  }
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
@media (max-width: 1024px) {
  .admin_main {
    padding: 2rem 1rem;
  }
  .admin_grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
@media (max-width: 768px) {
  .header_content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  .header_title {
    font-size: 1.5rem;
  }
  .admin_main {
    padding: 1rem;
  }
  .admin_card {
    border-radius: 16px;
  }
  .fab {
    width: 52px;
    height: 52px;
    font-size: 1.5rem;
  }
}
@media (max-width: 480px) {
  .admin_main {
    padding: 0.5rem;
  }
  .admin_card {
    border-radius: 10px;
  }
  .fab {
    width: 40px;
    height: 40px;
    font-size: 1.1rem;
    bottom: 1.2rem;
    right: 1.2rem;
  }
}
</style>
