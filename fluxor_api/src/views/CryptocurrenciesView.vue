<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900">Cryptocurrency Management</h1>
            <span class="ml-4 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {{ totalCryptocurrencies }} Total Cryptos
            </span>
          </div>
          <div class="flex items-center space-x-4">
            <button @click="refreshData" :disabled="loading" class="btn-secondary text-sm">
              <span v-if="loading">Refreshing...</span>
              <span v-else>🔄 Refresh</span>
            </button>
            <button @click="showImportModal = true" class="btn-primary text-sm">
              📊 Import Cryptos
            </button>
            <router-link to="/admin" class="btn-secondary text-sm">← Admin Dashboard</router-link>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Stats Overview -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm">✓</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Active Cryptos</dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ stats.active_count || 0 }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm">🏦</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Stablecoins</dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ stats.stablecoin_count || 0 }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm">⭐</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Featured</dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ stats.featured_count || 0 }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm">💰</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Market Cap</dt>
                  <dd class="text-lg font-medium text-gray-900">
                    ${{ formatLargeNumber(stats.total_market_cap || 0) }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters and Search -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="p-6 border-b border-gray-200">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
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
              <select v-model="filters.category" class="input-field" @change="filterCryptocurrencies">
                <option value="">All Categories</option>
                <option v-for="category in availableCategories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>

            <!-- Blockchain Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Blockchain</label>
              <select v-model="filters.blockchain" class="input-field" @change="filterCryptocurrencies">
                <option value="">All Blockchains</option>
                <option v-for="blockchain in availableBlockchains" :key="blockchain" :value="blockchain">
                  {{ blockchain }}
                </option>
              </select>
            </div>

            <!-- Status Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select v-model="filters.status" class="input-field" @change="filterCryptocurrencies">
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="stablecoin">Stablecoins</option>
                <option value="featured">Featured</option>
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
                'px-3 py-1 rounded-full text-sm',
                activeQuickFilter === quickFilter.key
                  ? 'bg-indigo-100 text-indigo-800 border border-indigo-200'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              {{ quickFilter.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- Cryptocurrencies Table -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-medium text-gray-900">
              Cryptocurrencies ({{ filteredCryptocurrencies.length }})
            </h3>
            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-500">Sort by:</span>
              <select v-model="sortBy" @change="sortCryptocurrencies" class="text-sm border-gray-300 rounded-md">
                <option value="rank">Market Cap Rank</option>
                <option value="name">Name</option>
                <option value="symbol">Symbol</option>
                <option value="price">Price</option>
                <option value="change_24h">24h Change</option>
                <option value="volume">Volume</option>
                <option value="market_cap">Market Cap</option>
              </select>
              <button @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'; sortCryptocurrencies()" 
                      class="text-sm text-gray-500 hover:text-gray-700">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </button>
            </div>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  #
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Cryptocurrency
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Price
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  24h %
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  7d %
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Market Cap
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Volume (24h)
                </th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="crypto in paginatedCryptocurrencies" :key="crypto.id" 
                  class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ crypto.rank }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-8 w-8">
                      <div class="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center">
                        <span class="text-xs font-bold text-gray-600">{{ crypto.symbol.substring(0, 2) }}</span>
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900 flex items-center">
                        {{ crypto.name }}
                        <span v-if="crypto.is_featured" class="ml-2 text-yellow-400">⭐</span>
                        <span v-if="crypto.is_stablecoin" class="ml-2 text-blue-400">🏦</span>
                      </div>
                      <div class="text-sm text-gray-500">{{ crypto.symbol }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                  ${{ formatPrice(crypto.current_price) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm"
                    :class="getPriceChangeClass(crypto.price_change_24h)">
                  {{ formatPercent(crypto.price_change_24h) }}%
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm"
                    :class="getPriceChangeClass(crypto.price_change_7d)">
                  {{ formatPercent(crypto.price_change_7d) }}%
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                  ${{ formatLargeNumber(crypto.market_cap) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                  ${{ formatLargeNumber(crypto.volume_24h) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-center">
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    crypto.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  ]">
                    {{ crypto.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                  <div class="flex justify-center space-x-1">
                    <button @click="toggleCryptoStatus(crypto)" 
                            :class="crypto.is_active ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'"
                            class="text-xs">
                      {{ crypto.is_active ? 'Deactivate' : 'Activate' }}
                    </button>
                    <span class="text-gray-300">|</span>
                    <button @click="editCrypto(crypto)" class="text-indigo-600 hover:text-indigo-900 text-xs">
                      Edit
                    </button>
                    <span class="text-gray-300">|</span>
                    <button @click="viewDetails(crypto)" class="text-gray-600 hover:text-gray-900 text-xs">
                      Details
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
            <button @click="previousPage" :disabled="currentPage === 1" 
                    class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Previous
            </button>
            <button @click="nextPage" :disabled="currentPage === totalPages" 
                    class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
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
                        class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  ‹
                </button>
                <button v-for="page in visiblePages" :key="page" @click="goToPage(page)"
                        :class="[
                          'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                          page === currentPage 
                            ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600'
                            : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                        ]">
                  {{ page }}
                </button>
                <button @click="nextPage" :disabled="currentPage === totalPages" 
                        class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  ›
                </button>
              </nav>
            </div>
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import { api } from '@/services/api'

const toast = useToast()

// State
const loading = ref(false)
const importing = ref(false)
const showImportModal = ref(false)
const cryptocurrencies = ref([])
const stats = ref({})
const activeQuickFilter = ref('')

// Filters
const filters = reactive({
  search: '',
  category: '',
  blockchain: '',
  status: ''
})

const importOptions = reactive({
  updateExisting: true,
  limit: 200
})

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(50)
const sortBy = ref('rank')
const sortOrder = ref('asc')

// Computed
const totalCryptocurrencies = computed(() => cryptocurrencies.value.length)

const availableCategories = computed(() => {
  const categories = new Set()
  cryptocurrencies.value.forEach(crypto => {
    crypto.categories?.forEach(category => categories.add(category))
  })
  return Array.from(categories).sort()
})

const availableBlockchains = computed(() => {
  const blockchains = new Set()
  cryptocurrencies.value.forEach(crypto => {
    if (crypto.blockchain_network) {
      blockchains.add(crypto.blockchain_network)
    }
  })
  return Array.from(blockchains).sort()
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
    filtered = filtered.filter(crypto => 
      crypto.categories?.includes(filters.category)
    )
  }

  // Blockchain filter
  if (filters.blockchain) {
    filtered = filtered.filter(crypto => 
      crypto.blockchain_network === filters.blockchain
    )
  }

  // Status filter
  if (filters.status) {
    switch (filters.status) {
      case 'active':
        filtered = filtered.filter(crypto => crypto.is_active)
        break
      case 'inactive':
        filtered = filtered.filter(crypto => !crypto.is_active)
        break
      case 'stablecoin':
        filtered = filtered.filter(crypto => crypto.is_stablecoin)
        break
      case 'featured':
        filtered = filtered.filter(crypto => crypto.is_featured)
        break
    }
  }

  return filtered
})

const sortedCryptocurrencies = computed(() => {
  const sorted = [...filteredCryptocurrencies.value]
  
  sorted.sort((a, b) => {
    let aValue, bValue
    
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
        aValue = parseFloat(a.current_price) || 0
        bValue = parseFloat(b.current_price) || 0
        break
      case 'change_24h':
        aValue = parseFloat(a.price_change_24h) || 0
        bValue = parseFloat(b.price_change_24h) || 0
        break
      case 'volume':
        aValue = parseFloat(a.volume_24h) || 0
        bValue = parseFloat(b.volume_24h) || 0
        break
      case 'market_cap':
        aValue = parseFloat(a.market_cap) || 0
        bValue = parseFloat(b.market_cap) || 0
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
  
  return sorted
})

const paginatedCryptocurrencies = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return sortedCryptocurrencies.value.slice(start, end)
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

const quickFilters = [
  { key: 'all', label: 'All', filters: {} },
  { key: 'top-50', label: 'Top 50', filters: { rank_lte: 50 } },
  { key: 'stablecoins', label: 'Stablecoins', filters: { status: 'stablecoin' } },
  { key: 'defi', label: 'DeFi', filters: { category: 'DeFi' } },
  { key: 'layer1', label: 'Layer 1', filters: { category: 'Layer 1' } },
  { key: 'meme', label: 'Meme Coins', filters: { category: 'Meme' } },
  { key: 'featured', label: 'Featured', filters: { status: 'featured' } }
]

// Methods
const formatPrice = (price) => {
  const num = parseFloat(price) || 0
  if (num < 0.01) return num.toFixed(6)
  if (num < 1) return num.toFixed(4)
  if (num < 100) return num.toFixed(2)
  return num.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}

const formatPercent = (value) => {
  return parseFloat(value || 0).toFixed(2)
}

const formatLargeNumber = (value) => {
  const num = parseFloat(value) || 0
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T'
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K'
  return num.toFixed(2)
}

const getPriceChangeClass = (change) => {
  const num = parseFloat(change) || 0
  if (num > 0) return 'text-green-600'
  if (num < 0) return 'text-red-600'
  return 'text-gray-500'
}

let searchTimeout = null
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    // filterCryptocurrencies is automatically triggered by reactive filters
  }, 300)
}

const filterCryptocurrencies = () => {
  currentPage.value = 1
}

const sortCryptocurrencies = () => {
  currentPage.value = 1
}

const applyQuickFilter = (quickFilter) => {
  activeQuickFilter.value = quickFilter.key
  
  // Reset filters
  Object.keys(filters).forEach(key => {
    filters[key] = ''
  })
  
  // Apply quick filter
  if (quickFilter.filters.rank_lte) {
    // Custom logic for top rankings
  }
  if (quickFilter.filters.status) {
    filters.status = quickFilter.filters.status
  }
  if (quickFilter.filters.category) {
    filters.category = quickFilter.filters.category
  }
  
  filterCryptocurrencies()
}

const goToPage = (page) => {
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
    await Promise.all([
      loadCryptocurrencies(),
      loadStats()
    ])
  } finally {
    loading.value = false
  }
}

const loadCryptocurrencies = async () => {
  try {
    const response = await api.admin.getCryptocurrencies()
    cryptocurrencies.value = response.data
  } catch (error) {
    console.error('Error loading cryptocurrencies:', error)
    toast.showToast('Failed to load cryptocurrencies', 'error')
  }
}

const loadStats = async () => {
  try {
    const response = await api.admin.getCryptocurrencyStats()
    stats.value = response.data
  } catch (error) {
    console.error('Error loading stats:', error)
  }
}

const toggleCryptoStatus = async (crypto) => {
  try {
    await api.admin.updateCryptocurrency(crypto.id, {
      is_active: !crypto.is_active
    })
    crypto.is_active = !crypto.is_active
    toast.showToast(`${crypto.symbol} ${crypto.is_active ? 'activated' : 'deactivated'}`, 'success')
  } catch (error) {
    console.error('Error toggling crypto status:', error)
    toast.showToast('Failed to update cryptocurrency status', 'error')
  }
}

const editCrypto = (crypto) => {
  // Navigate to edit view or open modal
  console.log('Edit crypto:', crypto)
}

const viewDetails = (crypto) => {
  // Navigate to details view or open modal
  console.log('View details:', crypto)
}

const importCryptocurrencies = async () => {
  importing.value = true
  try {
    const response = await api.admin.importCryptocurrencies({
      update_existing: importOptions.updateExisting,
      limit: importOptions.limit
    })
    
    toast.showToast(`Successfully imported ${response.data.imported_count} cryptocurrencies`, 'success')
    
    showImportModal.value = false
    await refreshData()
  } catch (error) {
    console.error('Error importing cryptocurrencies:', error)
    toast.showToast('Failed to import cryptocurrencies', 'error')
  } finally {
    importing.value = false
  }
}

// Lifecycle
onMounted(async () => {
  await refreshData()
  
  // Auto-refresh every 2 minutes
  setInterval(async () => {
    if (!loading.value) {
      await loadStats()
    }
  }, 120000)
})
</script>