<template>
  <div class="users-view">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h2>User Management</h2>
        <p>Manage user accounts, permissions, and verification status</p>
      </div>
      <div class="header-actions">
        <button @click="refreshUsers" class="btn btn-secondary" :disabled="loading">
          <i class="icon-refresh"></i>
          Refresh
        </button>
        <button @click="exportUsers" class="btn btn-primary">
          <i class="icon-download"></i>
          Export
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3>Total Users</h3>
          <p class="stat-value">{{ stats.totalUsers }}</p>
          <span class="stat-change positive">+{{ stats.newUsers }} this week</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <h3>Verified Users</h3>
          <p class="stat-value">{{ stats.verifiedUsers }}</p>
          <span class="stat-change">{{ stats.verificationRate }}% rate</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🔄</div>
        <div class="stat-content">
          <h3>Pending Verification</h3>
          <p class="stat-value">{{ stats.pendingVerification }}</p>
          <span class="stat-change">{{ stats.newVerifications }} new</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <h3>Active Traders</h3>
          <p class="stat-value">{{ stats.activeTraders }}</p>
          <span class="stat-change positive">{{ stats.traderGrowth }}% growth</span>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="filters-section">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search users by email, name, or ID..."
          @input="searchUsers"
        />
      </div>
      <div class="filters">
        <select v-model="statusFilter" @change="filterUsers">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="suspended">Suspended</option>
        </select>
        <select v-model="verificationFilter" @change="filterUsers">
          <option value="">All Verification</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
        </select>
        <select v-model="roleFilter" @change="filterUsers">
          <option value="">All Roles</option>
          <option value="user">User</option>
          <option value="admin">Admin</option>
          <option value="superuser">Super Admin</option>
        </select>
      </div>
    </div>

    <!-- Users Table -->
    <div class="content-section">
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>User</th>
              <th>Email</th>
              <th>Status</th>
              <th>Verification</th>
              <th>Role</th>
              <th>Balance</th>
              <th>Joined</th>
              <th>Last Login</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id">
              <td>
                <div class="user-info">
                  <div class="user-avatar">{{ getUserInitials(user) }}</div>
                  <div class="user-details">
                    <strong>{{ user.first_name }} {{ user.last_name }}</strong>
                    <small>ID: {{ user.id }}</small>
                  </div>
                </div>
              </td>
              <td>{{ user.email }}</td>
              <td>
                <span class="status-badge" :class="user.is_active ? 'active' : 'inactive'">
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>
                <span class="status-badge" :class="user.verification_status">
                  {{ user.verification_status }}
                </span>
              </td>
              <td>
                <span class="role-badge" :class="getUserRole(user)">
                  {{ getUserRoleText(user) }}
                </span>
              </td>
              <td class="amount">${{ formatCurrency(user.balance || 0) }}</td>
              <td>{{ formatDate(user.date_joined) }}</td>
              <td>{{ formatDate(user.last_login) }}</td>
              <td>
                <div class="action-buttons">
                  <button 
                    @click="viewUser(user)" 
                    class="btn btn-primary btn-sm"
                    title="View Details"
                  >
                    <i class="icon-eye"></i>
                  </button>
                  <button 
                    @click="editUser(user)" 
                    class="btn btn-secondary btn-sm"
                    title="Edit User"
                  >
                    <i class="icon-edit"></i>
                  </button>
                  <button 
                    v-if="user.verification_status === 'pending'"
                    @click="approveVerification(user)" 
                    class="btn btn-success btn-sm"
                    title="Approve Verification"
                  >
                    <i class="icon-check"></i>
                  </button>
                  <button 
                    @click="toggleUserStatus(user)" 
                    class="btn btn-sm"
                    :class="user.is_active ? 'btn-warning' : 'btn-success'"
                    :title="user.is_active ? 'Suspend User' : 'Activate User'"
                  >
                    <i :class="user.is_active ? 'icon-pause' : 'icon-play'"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div class="pagination">
        <button 
          @click="previousPage" 
          :disabled="currentPage === 1"
          class="btn btn-secondary btn-sm"
        >
          Previous
        </button>
        <span class="page-info">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button 
          @click="nextPage" 
          :disabled="currentPage === totalPages"
          class="btn btn-secondary btn-sm"
        >
          Next
        </button>
      </div>
    </div>

    <!-- User Details Modal -->
    <div v-if="selectedUser" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>User Details</h3>
          <button @click="closeModal" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="user-detail-grid">
            <div class="detail-item">
              <label>Full Name</label>
              <span>{{ selectedUser.first_name }} {{ selectedUser.last_name }}</span>
            </div>
            <div class="detail-item">
              <label>Email</label>
              <span>{{ selectedUser.email }}</span>
            </div>
            <div class="detail-item">
              <label>Phone</label>
              <span>{{ selectedUser.phone_number || 'Not provided' }}</span>
            </div>
            <div class="detail-item">
              <label>Date of Birth</label>
              <span>{{ selectedUser.date_of_birth || 'Not provided' }}</span>
            </div>
            <div class="detail-item">
              <label>Verification Status</label>
              <span class="status-badge" :class="selectedUser.verification_status">
                {{ selectedUser.verification_status }}
              </span>
            </div>
            <div class="detail-item">
              <label>Trading Level</label>
              <span>{{ selectedUser.trading_level || 'Basic' }}</span>
            </div>
            <div class="detail-item">
              <label>Account Status</label>
              <span>{{ selectedUser.account_status || 'Active' }}</span>
            </div>
            <div class="detail-item">
              <label>Joined Date</label>
              <span>{{ formatDate(selectedUser.date_joined) }}</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeModal" class="btn btn-secondary">Close</button>
          <button @click="editUser(selectedUser)" class="btn btn-primary">Edit User</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import api from '@/services/api'

const loading = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const verificationFilter = ref('')
const roleFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const selectedUser = ref(null)

const stats = reactive({
  totalUsers: 0,
  newUsers: 0,
  verifiedUsers: 0,
  verificationRate: 0,
  pendingVerification: 0,
  newVerifications: 0,
  activeTraders: 0,
  traderGrowth: 0
})

const users = ref([])

const filteredUsers = computed(() => {
  let filtered = users.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(user => 
      user.email.toLowerCase().includes(query) ||
      `${user.first_name} ${user.last_name}`.toLowerCase().includes(query) ||
      user.id.toString().includes(query)
    )
  }

  if (statusFilter.value) {
    filtered = filtered.filter(user => 
      statusFilter.value === 'active' ? user.is_active : !user.is_active
    )
  }

  if (verificationFilter.value) {
    filtered = filtered.filter(user => user.verification_status === verificationFilter.value)
  }

  if (roleFilter.value) {
    filtered = filtered.filter(user => {
      if (roleFilter.value === 'superuser') return user.is_superuser
      if (roleFilter.value === 'admin') return user.is_staff && !user.is_superuser
      return !user.is_staff && !user.is_superuser
    })
  }

  return filtered
})

const totalPages = computed(() => Math.ceil(filteredUsers.value.length / pageSize.value))

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'Never'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getUserInitials = (user: any) => {
  const firstName = user.first_name || ''
  const lastName = user.last_name || ''
  if (firstName && lastName) {
    return (firstName[0] + lastName[0]).toUpperCase()
  }
  return user.email.substring(0, 2).toUpperCase()
}

const getUserRole = (user: any) => {
  if (user.is_superuser) return 'superuser'
  if (user.is_staff) return 'admin'
  return 'user'
}

const getUserRoleText = (user: any) => {
  if (user.is_superuser) return 'Super Admin'
  if (user.is_staff) return 'Admin'
  return 'User'
}

const refreshUsers = async () => {
  loading.value = true
  try {
    await Promise.all([loadStats(), loadUsers()])
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    // Mock data - replace with actual API calls
    stats.totalUsers = 1247
    stats.newUsers = 23
    stats.verifiedUsers = 1089
    stats.verificationRate = 87
    stats.pendingVerification = 45
    stats.newVerifications = 8
    stats.activeTraders = 892
    stats.traderGrowth = 12
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

const loadUsers = async () => {
  try {
    // Mock data - replace with actual API call
    users.value = [
      {
        id: 1,
        email: 'john.doe@example.com',
        first_name: 'John',
        last_name: 'Doe',
        is_active: true,
        is_staff: false,
        is_superuser: false,
        verification_status: 'approved',
        balance: 1500.75,
        date_joined: new Date().toISOString(),
        last_login: new Date().toISOString(),
        phone_number: '+1234567890',
        trading_level: 'Advanced'
      },
      {
        id: 2,
        email: 'admin@fluxor.pro',
        first_name: 'Admin',
        last_name: 'User',
        is_active: true,
        is_staff: true,
        is_superuser: true,
        verification_status: 'approved',
        balance: 0,
        date_joined: new Date().toISOString(),
        last_login: new Date().toISOString()
      }
    ]
  } catch (error) {
    console.error('Failed to load users:', error)
  }
}

const searchUsers = () => {
  currentPage.value = 1
}

const filterUsers = () => {
  currentPage.value = 1
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const viewUser = (user: any) => {
  selectedUser.value = user
}

const editUser = (user: any) => {
  console.log('Edit user:', user.id)
  // Implement edit functionality
}

const approveVerification = async (user: any) => {
  try {
    console.log('Approve verification for user:', user.id)
    // API call to approve verification
    await loadUsers()
  } catch (error) {
    console.error('Failed to approve verification:', error)
  }
}

const toggleUserStatus = async (user: any) => {
  try {
    console.log('Toggle status for user:', user.id)
    // API call to toggle user status
    await loadUsers()
  } catch (error) {
    console.error('Failed to toggle user status:', error)
  }
}

const exportUsers = () => {
  console.log('Export users')
  // Implement export functionality
}

const closeModal = () => {
  selectedUser.value = null
}

onMounted(() => {
  refreshUsers()
})
</script>

<style scoped>
.users-view {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.header-content h2 {
  color: var(--text-primary);
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.header-content p {
  color: var(--text-secondary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: var(--primary-color);
  color: var(--text-dark);
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-success {
  background: var(--success-color);
  color: white;
}

.btn-warning {
  background: var(--warning-color);
  color: white;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 14px;
}

.btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  border-radius: 12px;
}

.stat-content h3 {
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  color: var(--text-primary);
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.stat-change {
  font-size: 12px;
  color: var(--text-muted);
}

.stat-change.positive {
  color: var(--success-color);
}

.filters-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 20px;
}

.search-box {
  flex: 1;
  max-width: 400px;
}

.search-box input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: 16px;
}

.filters {
  display: flex;
  gap: 12px;
}

.filters select {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.content-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  font-weight: 500;
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.data-table td {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: var(--primary-color);
  color: var(--text-dark);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.user-details strong {
  display: block;
  color: var(--text-primary);
}

.user-details small {
  color: var(--text-secondary);
  font-size: 12px;
}

.amount {
  font-weight: 600;
  color: var(--primary-color);
}

.status-badge {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.status-badge.active {
  background: rgba(60, 210, 120, 0.1);
  color: var(--success-color);
}

.status-badge.inactive {
  background: rgba(207, 49, 39, 0.1);
  color: var(--error-color);
}

.status-badge.pending {
  background: rgba(247, 147, 26, 0.1);
  color: var(--warning-color);
}

.status-badge.approved {
  background: rgba(60, 210, 120, 0.1);
  color: var(--success-color);
}

.status-badge.rejected {
  background: rgba(207, 49, 39, 0.1);
  color: var(--error-color);
}

.role-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.role-badge.superuser {
  background: var(--error-color);
  color: white;
}

.role-badge.admin {
  background: var(--warning-color);
  color: white;
}

.role-badge.user {
  background: var(--secondary-color);
  color: white;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.pagination {
  padding: 20px 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  border-top: 1px solid var(--border-color);
}

.page-info {
  color: var(--text-secondary);
  font-size: 14px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--bg-card);
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  padding: 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  color: var(--text-primary);
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px;
}

.modal-body {
  padding: 24px;
}

.user-detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item label {
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-item span {
  color: var(--text-primary);
  font-weight: 500;
}

.modal-footer {
  padding: 24px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* Icons */
.icon-refresh::before { content: '🔄'; }
.icon-download::before { content: '📥'; }
.icon-eye::before { content: '👁️'; }
.icon-edit::before { content: '✏️'; }
.icon-check::before { content: '✅'; }
.icon-pause::before { content: '⏸️'; }
.icon-play::before { content: '▶️'; }
</style>
