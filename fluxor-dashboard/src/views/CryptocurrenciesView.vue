<template>
  <div class="space-y-6">
    <!-- Header with Actions -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Cryptocurrency Management</h1>
        <p class="text-sm text-gray-600">Manage your cryptocurrency portfolio and trading pairs</p>
      </div>
      <div class="flex space-x-3">
        <button @click="refreshData" :disabled="loading" class="btn-secondary">
          <span v-if="loading">Refreshing...</span>
          <span v-else>🔄 Refresh</span>
        </button>
        <button @click="showImportModal = true" class="btn-primary">
          📊 Import Cryptocurrencies
        </button>
        <button @click="showAddModal = true" class="btn-success">
          + Add Cryptocurrency
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-success-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">✓</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Active Cryptocurrencies</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.activeCount }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">🏦</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Stablecoins</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.stablecoinCount }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-warning-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">⭐</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Featured</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.featuredCount }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">💰</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Total Market Cap</dt>
                <dd class="text-lg font-medium text-gray-900">${{ formatLargeNumber(stats.totalMarketCap) }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="card">
      <div class="card-body">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <!-- Search -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <input
              v-model="filters.search"
              type="text"
              class="input-field"
              placeholder="Search by name or symbol..."
              @input="debouncedSearch"
            />
          </div>

          <!-- Category Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select v-model="filters.category" class="input-field" @change="applyFilters">
              <option value="">All Categories</option>
              <option v-for="category in availableCategories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>

          <!-- Status Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select v-model="filters.status" class="input-field" @change="applyFilters">
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="stablecoin">Stablecoins</option>
              <option value="featured">Featured</option>
            </select>
          </div>

          <!-- Sort By -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
            <select v-model="sortBy" @change="applySorting" class="input-field">
              <option value="rank">Market Cap Rank</option>
              <option value="name">Name</option>
              <option value="symbol">Symbol</option>
              <option value="price">Price</option>
              <option value="change_24h">24h Change</option>
              <option value="volume">Volume</option>
              <option value="market_cap">Market Cap</option>
            </select>
          </div>

          <!-- Items Per Page -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Show</label>
            <select v-model="itemsPerPage" @change="updatePagination" class="input-field">
              <option value="25">25 per page</option>
              <option value="50">50 per page</option>
              <option value="100">100 per page</option>
              <option value="200">200 per page</option>
            </select>
          </div>
        </div>

        <!-- Quick Filters -->
        <div class="mt-4 flex flex-wrap gap-2">
          <button
            v-for="quickFilter in quickFilters"
            :key="quickFilter.key"
            @click="applyQuickFilter(quickFilter)"
            :class="[
              'px-3 py-1 rounded-full text-sm transition-colors',
              activeQuickFilter === quickFilter.key
                ? 'bg-primary-100 text-primary-800 border border-primary-200'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            {{ quickFilter.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Cryptocurrencies Table -->
    <div class="card">
      <div class="card-header">
        <h3 class="text-lg font-medium text-gray-900">
          Cryptocurrencies ({{ filteredCryptocurrencies.length }})
        </h3>
      </div>
      <div class="overflow-x-auto">
        <table class="table">
          <thead class="bg-gray-50">
            <tr>
              <th class="table-header">#</th>
              <th class="table-header">Cryptocurrency</th>
              <th class="table-header text-right">Price</th>
              <th class="table-header text-right">24h %</th>
              <th class="table-header text-right">7d %</th>
              <th class="table-header text-right">Market Cap</th>
              <th class="table-header text-right">Volume (24h)</th>
              <th class="table-header text-center">Status</th>
              <th class="table-header text-center">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="crypto in paginatedCryptocurrencies" :key="crypto.id" class="hover:bg-gray-50">
              <td class="table-cell">{{ crypto.rank }}</td>
              <td class="table-cell">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-8 w-8">
                    <div class="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center">
                      <span class="text-xs font-bold text-gray-600">{{ crypto.symbol.substring(0, 2) }}</span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900 flex items-center">
                      {{ crypto.name }}
                      <span v-if="crypto.isFeatured" class="ml-2 text-yellow-400">⭐</span>
                      <span v-if="crypto.isStablecoin" class="ml-2 text-blue-400">🏦</span>
                    </div>
                    <div class="text-sm text-gray-500">{{ crypto.symbol }}</div>
                  </div>
                </div>
              </td>
              <td class="table-cell text-right">${{ formatPrice(crypto.currentPrice) }}</td>
              <td class="table-cell text-right" :class="getPriceChangeClass(crypto.priceChange24h)">
                {{ formatPercent(crypto.priceChange24h) }}%
              </td>
              <td class="table-cell text-right" :class="getPriceChangeClass(crypto.priceChange7d)">
                {{ formatPercent(crypto.priceChange7d) }}%
              </td>
              <td class="table-cell text-right">${{ formatLargeNumber(crypto.marketCap) }}</td>
              <td class="table-cell text-right">${{ formatLargeNumber(crypto.volume24h) }}</td>
              <td class="table-cell text-center">
                <span :class="crypto.isActive ? 'badge-success' : 'badge-danger'">
                  {{ crypto.isActive ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="table-cell text-center">
                <div class="flex justify-center space-x-2">
                  <button @click="editCrypto(crypto)" class="text-primary-600 hover:text-primary-900 text-sm">
                    Edit
                  </button>
                  <button @click="toggleCryptoStatus(crypto)" 
                          :class="crypto.isActive ? 'text-danger-600 hover:text-danger-900' : 'text-success-600 hover:text-success-900'"
                          class="text-sm">
                    {{ crypto.isActive ? 'Deactivate' : 'Activate' }}
                  </button>
                  <button @click="deleteCrypto(crypto)" class="text-danger-600 hover:text-danger-900 text-sm">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
        <div class="flex-1 flex justify-between sm:hidden">
          <button @click="previousPage" :disabled="currentPage === 1" class="btn-secondary">
            Previous
          </button>
          <button @click="nextPage" :disabled="currentPage === totalPages" class="btn-secondary">
            Next
          </button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Showing
              <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
              to
              <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, filteredCryptocurrencies.length) }}</span>
              of
              <span class="font-medium">{{ filteredCryptocurrencies.length }}</span>
              results
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
              <button @click="previousPage" :disabled="currentPage === 1" 
                      class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
                ‹
              </button>
              <button v-for="page in visiblePages" :key="page" @click="goToPage(page)"
                      :class="[
                        'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                        page === currentPage 
                          ? 'z-10 bg-primary-50 border-primary-500 text-primary-600'
                          : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                      ]">
                {{ page }}
              </button>
              <button @click="nextPage" :disabled="currentPage === totalPages" 
                      class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
                ›
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Import Modal -->
    <div v-if="showImportModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Import Cryptocurrencies</h3>
          
          <div class="space-y-4">
            <div>
              <label class="flex items-center">
                <input type="checkbox" v-model="importOptions.updateExisting" class="mr-2">
                Update existing cryptocurrencies
              </label>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Import Limit</label>
              <input v-model.number="importOptions.limit" type="number" min="1" max="500" 
                     class="input-field" placeholder="200">
              <p class="text-xs text-gray-500 mt-1">Number of cryptocurrencies to import (max 500)</p>
            </div>
            
            <div class="flex space-x-2">
              <button @click="showImportModal = false" class="btn-secondary flex-1">
                Cancel
              </button>
              <button @click="importCryptocurrencies" :disabled="importing" class="btn-primary flex-1">
                <span v-if="importing">Importing...</span>
                <span v-else>Import</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || editingCrypto" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border max-w-2xl shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ editingCrypto ? 'Edit Cryptocurrency' : 'Add New Cryptocurrency' }}
          </h3>
          
          <form @submit.prevent="saveCrypto" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input v-model="cryptoForm.name" type="text" class="input-field" required>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Symbol</label>
                <input v-model="cryptoForm.symbol" type="text" class="input-field" required>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Current Price</label>
                <input v-model.number="cryptoForm.currentPrice" type="number" step="0.000001" class="input-field" required>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Market Cap Rank</label>
                <input v-model.number="cryptoForm.rank" type="number" class="input-field">
              </div>
            </div>

            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="flex items-center">
                  <input type="checkbox" v-model="cryptoForm.isActive" class="mr-2">
                  Active
                </label>
              </div>
              <div>
                <label class="flex items-center">
                  <input type="checkbox" v-model="cryptoForm.isFeatured" class="mr-2">
                  Featured
                </label>
              </div>
              <div>
                <label class="flex items-center">
                  <input type="checkbox" v-model="cryptoForm.isStablecoin" class="mr-2">
                  Stablecoin
                </label>
              </div>
            </div>
            
            <div class="flex space-x-2">
              <button type="button" @click="cancelEdit" class="btn-secondary flex-1">
                Cancel
              </button>
              <button type="submit" :disabled="saving" class="btn-primary flex-1">
                <span v-if="saving">Saving...</span>
                <span v-else>{{ editingCrypto ? 'Update' : 'Create' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'

// State
const loading = ref(false)
const importing = ref(false)
const saving = ref(false)
const showImportModal = ref(false)
const showAddModal = ref(false)
const editingCrypto = ref<any>(null)
const activeQuickFilter = ref('')

// Sample data
const cryptocurrencies = ref([
  {
    id: 1, name: 'Bitcoin', symbol: 'BTC', rank: 1, currentPrice: 45234.56, 
    priceChange24h: 5.2, priceChange7d: 12.5, marketCap: 850000000000, volume24h: 25000000000,
    isActive: true, isFeatured: true, isStablecoin: false, category: 'Layer 1'
  },
  {
    id: 2, name: 'Ethereum', symbol: 'ETH', rank: 2, currentPrice: 3187.92,
    priceChange24h: 3.8, priceChange7d: 8.2, marketCap: 380000000000, volume24h: 15000000000,
    isActive: true, isFeatured: true, isStablecoin: false, category: 'Layer 1'
  },
  {
    id: 3, name: 'Tether', symbol: 'USDT', rank: 3, currentPrice: 1.00,
    priceChange24h: 0.1, priceChange7d: -0.05, marketCap: 95000000000, volume24h: 45000000000,
    isActive: true, isFeatured: false, isStablecoin: true, category: 'Stablecoin'
  },
  {
    id: 4, name: 'Cardano', symbol: 'ADA', rank: 8, currentPrice: 0.89,
    priceChange24h: -2.1, priceChange7d: 5.3, marketCap: 28000000000, volume24h: 800000000,
    isActive: true, isFeatured: false, isStablecoin: false, category: 'Layer 1'
  },
  {
    id: 5, name: 'Polkadot', symbol: 'DOT', rank: 11, currentPrice: 23.45,
    priceChange24h: 7.3, priceChange7d: 15.8, marketCap: 22000000000, volume24h: 1200000000,
    isActive: true, isFeatured: false, isStablecoin: false, category: 'Layer 1'
  }
])

const stats = ref({
  activeCount: 0,
  stablecoinCount: 0,
  featuredCount: 0,
  totalMarketCap: 0
})

// Filters
const filters = reactive({
  search: '',
  category: '',
  status: ''
})

const importOptions = reactive({
  updateExisting: true,
  limit: 200
})

const cryptoForm = reactive({
  name: '',
  symbol: '',
  currentPrice: 0,
  rank: 0,
  isActive: true,
  isFeatured: false,
  isStablecoin: false
})

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(50)
const sortBy = ref('rank')
const sortOrder = ref('asc')

// Quick filters
const quickFilters = [
  { key: 'all', label: 'All', filters: {} },
  { key: 'top-50', label: 'Top 50', filters: { rank_lte: 50 } },
  { key: 'stablecoins', label: 'Stablecoins', filters: { status: 'stablecoin' } },
  { key: 'featured', label: 'Featured', filters: { status: 'featured' } },
  { key: 'layer1', label: 'Layer 1', filters: { category: 'Layer 1' } }
]

// Computed
const availableCategories = computed(() => {
  const categories = new Set<string>()
  cryptocurrencies.value.forEach(crypto => {
    if (crypto.category) categories.add(crypto.category)
  })
  return Array.from(categories).sort()
})

const filteredCryptocurrencies = computed(() => {
  let filtered = [...cryptocurrencies.value]

  // Search filter
  if (filters.search) {
    const search = filters.search.toLowerCase()
    filtered = filtered.filter(crypto => 
      crypto.name.toLowerCase().includes(search) || 
      crypto.symbol.toLowerCase().includes(search)
    )
  }

  // Category filter
  if (filters.category) {
    filtered = filtered.filter(crypto => crypto.category === filters.category)
  }

  // Status filter
  if (filters.status) {
    switch (filters.status) {
      case 'active':
        filtered = filtered.filter(crypto => crypto.isActive)
        break
      case 'inactive':
        filtered = filtered.filter(crypto => !crypto.isActive)
        break
      case 'stablecoin':
        filtered = filtered.filter(crypto => crypto.isStablecoin)
        break
      case 'featured':
        filtered = filtered.filter(crypto => crypto.isFeatured)
        break
    }
  }

  // Sort
  filtered.sort((a, b) => {
    let aValue: any, bValue: any
    
    switch (sortBy.value) {
      case 'name':
        aValue = a.name
        bValue = b.name
        break
      case 'symbol':
        aValue = a.symbol
        bValue = b.symbol
        break
      case 'price':
        aValue = a.currentPrice
        bValue = b.currentPrice
        break
      case 'change_24h':
        aValue = a.priceChange24h
        bValue = b.priceChange24h
        break
      case 'volume':
        aValue = a.volume24h
        bValue = b.volume24h
        break
      case 'market_cap':
        aValue = a.marketCap
        bValue = b.marketCap
        break
      default: // rank
        aValue = a.rank || 999999
        bValue = b.rank || 999999
    }
    
    if (sortOrder.value === 'desc') {
      return aValue < bValue ? 1 : -1
    }
    return aValue > bValue ? 1 : -1
  })

  return filtered
})

const paginatedCryptocurrencies = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredCryptocurrencies.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredCryptocurrencies.value.length / itemsPerPage.value)
})

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 7
  const current = currentPage.value
  const total = totalPages.value
  
  let start = Math.max(1, current - Math.floor(maxVisible / 2))
  let end = Math.min(total, start + maxVisible - 1)
  
  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// Methods
const formatPrice = (price: number): string => {
  if (price < 0.01) return price.toFixed(6)
  if (price < 1) return price.toFixed(4)
  if (price < 100) return price.toFixed(2)
  return price.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}

const formatPercent = (value: number): string => {
  return value.toFixed(2)
}

const formatLargeNumber = (value: number): string => {
  if (value >= 1e12) return (value / 1e12).toFixed(2) + 'T'
  if (value >= 1e9) return (value / 1e9).toFixed(2) + 'B'
  if (value >= 1e6) return (value / 1e6).toFixed(2) + 'M'
  if (value >= 1e3) return (value / 1e3).toFixed(2) + 'K'
  return value.toFixed(2)
}

const getPriceChangeClass = (change: number): string => {
  if (change > 0) return 'text-success-600'
  if (change < 0) return 'text-danger-600'
  return 'text-gray-500'
}

const updateStats = () => {
  stats.value = {
    activeCount: cryptocurrencies.value.filter(c => c.isActive).length,
    stablecoinCount: cryptocurrencies.value.filter(c => c.isStablecoin).length,
    featuredCount: cryptocurrencies.value.filter(c => c.isFeatured).length,
    totalMarketCap: cryptocurrencies.value.reduce((sum, c) => sum + c.marketCap, 0)
  }
}

const debouncedSearch = (() => {
  let timeout: number
  return () => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      currentPage.value = 1
    }, 300)
  }
})()

const applyFilters = () => {
  currentPage.value = 1
}

const applySorting = () => {
  currentPage.value = 1
}

const updatePagination = () => {
  currentPage.value = 1
}

const applyQuickFilter = (quickFilter: any) => {
  activeQuickFilter.value = quickFilter.key
  
  // Reset filters
  Object.keys(filters).forEach(key => {
    ;(filters as any)[key] = ''
  })
  
  // Apply quick filter logic
  if (quickFilter.filters.status) {
    filters.status = quickFilter.filters.status
  }
  if (quickFilter.filters.category) {
    filters.category = quickFilter.filters.category
  }
  
  currentPage.value = 1
}

const goToPage = (page: number) => {
  currentPage.value = page
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

const refreshData = async () => {
  loading.value = true
  try {
    // TODO: Load from API
    await new Promise(resolve => setTimeout(resolve, 1000))
    updateStats()
  } finally {
    loading.value = false
  }
}

const importCryptocurrencies = async () => {
  importing.value = true
  try {
    // TODO: Call import API
    await new Promise(resolve => setTimeout(resolve, 2000))
    showImportModal.value = false
    await refreshData()
  } finally {
    importing.value = false
  }
}

const editCrypto = (crypto: any) => {
  editingCrypto.value = crypto
  Object.assign(cryptoForm, crypto)
}

const cancelEdit = () => {
  editingCrypto.value = null
  showAddModal.value = false
  Object.assign(cryptoForm, {
    name: '',
    symbol: '',
    currentPrice: 0,
    rank: 0,
    isActive: true,
    isFeatured: false,
    isStablecoin: false
  })
}

const saveCrypto = async () => {
  saving.value = true
  try {
    // TODO: Save to API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (editingCrypto.value) {
      Object.assign(editingCrypto.value, cryptoForm)
    } else {
      cryptocurrencies.value.push({
        id: Date.now(),
        ...cryptoForm,
        priceChange24h: 0,
        priceChange7d: 0,
        marketCap: 0,
        volume24h: 0,
        category: 'Other'
      })
    }
    
    cancelEdit()
    updateStats()
  } finally {
    saving.value = false
  }
}

const toggleCryptoStatus = async (crypto: any) => {
  try {
    // TODO: Update via API
    crypto.isActive = !crypto.isActive
    updateStats()
  } catch (error) {
    console.error('Failed to toggle crypto status:', error)
  }
}

const deleteCrypto = async (crypto: any) => {
  if (confirm(`Are you sure you want to delete ${crypto.name}?`)) {
    try {
      // TODO: Delete via API
      const index = cryptocurrencies.value.findIndex(c => c.id === crypto.id)
      if (index > -1) {
        cryptocurrencies.value.splice(index, 1)
        updateStats()
      }
    } catch (error) {
      console.error('Failed to delete crypto:', error)
    }
  }
}

// Lifecycle
onMounted(() => {
  updateStats()
})
</script>