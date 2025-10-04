<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900">Admin Control Dashboard</h1>
            <div class="ml-6 flex items-center space-x-2">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="systemStatus.trading_enabled ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                {{ systemStatus.trading_enabled ? 'Trading ON' : 'Trading OFF' }}
              </span>
              <span v-if="systemStatus.maintenance_mode" 
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                Maintenance Mode
              </span>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/cryptocurrencies" class="btn-primary text-sm">
              💰 Manage Cryptocurrencies
            </router-link>
            <button @click="refreshDashboard" class="btn-secondary text-sm">
              <span v-if="refreshing">Refreshing...</span>
              <span v-else>Refresh</span>
            </button>
            <router-link to="/dashboard" class="btn-secondary text-sm">User Dashboard</router-link>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm">₿</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Portfolio</dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ formatBTC(dashboardStats.trading_stats?.total_portfolio_value_btc || 0) }} BTC
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
                <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm">↗</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Active Investments</dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ dashboardStats.trading_stats?.active_investments || 0 }}
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
                  <span class="text-white text-sm">⏳</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Pending Deposits</dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ dashboardStats.deposit_stats?.pending_deposits || 0 }}
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
                  <span class="text-white text-sm">⚡</span>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Active Scenarios</dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ dashboardStats.scenario_stats?.active_scenarios || 0 }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Dashboard Tabs -->
      <div class="bg-white shadow rounded-lg">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8 px-6">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                activeTab === tab.id
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>

        <div class="p-6">
          <!-- Trading Settings Tab -->
          <div v-if="activeTab === 'settings'" class="space-y-6">
            <h3 class="text-lg font-medium text-gray-900">Global Trading Settings</h3>
            
            <form @submit.prevent="updateTradingSettings" class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Global Controls -->
                <div class="space-y-4">
                  <h4 class="text-md font-medium text-gray-800">System Controls</h4>
                  
                  <div class="flex items-center">
                    <input
                      v-model="tradingSettings.trading_enabled"
                      type="checkbox"
                      class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    />
                    <label class="ml-2 block text-sm text-gray-900">Trading Enabled</label>
                  </div>

                  <div class="flex items-center">
                    <input
                      v-model="tradingSettings.maintenance_mode"
                      type="checkbox"
                      class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    />
                    <label class="ml-2 block text-sm text-gray-900">Maintenance Mode</label>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Profit/Loss Mode</label>
                    <select v-model="tradingSettings.profit_loss_mode" class="input-field">
                      <option value="manual">Manual Control</option>
                      <option value="automatic">Automatic (Market Based)</option>
                      <option value="simulated">Simulated Trading</option>
                      <option value="custom">Custom Scenarios</option>
                    </select>
                  </div>
                </div>

                <!-- Rate Controls -->
                <div class="space-y-4">
                  <h4 class="text-md font-medium text-gray-800">Profit/Loss Rates</h4>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Default Profit Rate (% per hour)</label>
                    <input
                      v-model.number="tradingSettings.default_profit_rate"
                      type="number"
                      step="0.1"
                      class="input-field"
                      placeholder="5.0"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Default Loss Rate (% per hour)</label>
                    <input
                      v-model.number="tradingSettings.default_loss_rate"
                      type="number"
                      step="0.1"
                      class="input-field"
                      placeholder="2.0"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Max Profit Rate (% per hour)</label>
                    <input
                      v-model.number="tradingSettings.max_profit_rate"
                      type="number"
                      step="0.1"
                      class="input-field"
                      placeholder="100.0"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Max Loss Rate (% per hour)</label>
                    <input
                      v-model.number="tradingSettings.max_loss_rate"
                      type="number"
                      step="0.1"
                      class="input-field"
                      placeholder="50.0"
                    />
                  </div>
                </div>

                <!-- Index Settings -->
                <div class="space-y-4">
                  <h4 class="text-md font-medium text-gray-800">Index Settings</h4>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Index Appreciation Rate (% per day)</label>
                    <input
                      v-model.number="tradingSettings.index_appreciation_rate"
                      type="number"
                      step="0.1"
                      class="input-field"
                      placeholder="10.0"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Index Depreciation Rate (% per day)</label>
                    <input
                      v-model.number="tradingSettings.index_depreciation_rate"
                      type="number"
                      step="0.1"
                      class="input-field"
                      placeholder="5.0"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Index Volatility Factor</label>
                    <input
                      v-model.number="tradingSettings.index_volatility_factor"
                      type="number"
                      step="0.1"
                      class="input-field"
                      placeholder="1.5"
                    />
                  </div>
                </div>

                <!-- Update Frequencies -->
                <div class="space-y-4">
                  <h4 class="text-md font-medium text-gray-800">Update Frequencies (seconds)</h4>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Price Updates</label>
                    <input
                      v-model.number="tradingSettings.price_update_frequency"
                      type="number"
                      min="1"
                      class="input-field"
                      placeholder="1"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Investment Updates</label>
                    <input
                      v-model.number="tradingSettings.investment_update_frequency"
                      type="number"
                      min="1"
                      class="input-field"
                      placeholder="5"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Portfolio Calculations</label>
                    <input
                      v-model.number="tradingSettings.portfolio_calculation_frequency"
                      type="number"
                      min="1"
                      class="input-field"
                      placeholder="10"
                    />
                  </div>
                </div>
              </div>

              <div class="flex justify-end">
                <button type="submit" :disabled="updatingSettings" class="btn-primary">
                  <span v-if="updatingSettings">Updating...</span>
                  <span v-else>Update Settings</span>
                </button>
              </div>
            </form>
          </div>

          <!-- Cryptocurrencies Tab -->
          <div v-if="activeTab === 'cryptocurrencies'" class="space-y-6">
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-medium text-gray-900">Cryptocurrency Overview</h3>
              <router-link to="/cryptocurrencies" class="btn-primary">
                💰 Manage All Cryptocurrencies
              </router-link>
            </div>
            
            <!-- Quick Stats -->
            <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
              <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm font-medium text-blue-600">Total Cryptos</p>
                    <p class="text-2xl font-bold text-blue-900">{{ dashboardStats.crypto_stats?.total_count || 0 }}</p>
                  </div>
                  <div class="text-blue-400">
                    <svg class="h-8 w-8" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"/>
                      <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"/>
                    </svg>
                  </div>
                </div>
              </div>
              
              <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm font-medium text-green-600">Active</p>
                    <p class="text-2xl font-bold text-green-900">{{ dashboardStats.crypto_stats?.active_count || 0 }}</p>
                  </div>
                  <div class="text-green-400">
                    <svg class="h-8 w-8" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                </div>
              </div>
              
              <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm font-medium text-yellow-600">Stablecoins</p>
                    <p class="text-2xl font-bold text-yellow-900">{{ dashboardStats.crypto_stats?.stablecoin_count || 0 }}</p>
                  </div>
                  <div class="text-yellow-400">
                    <svg class="h-8 w-8" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"/>
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm-7-8a7 7 0 1114 0c0 5.25-5.85 7.45-7 7.45S3 15.25 3 10z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                </div>
              </div>
              
              <div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm font-medium text-purple-600">Featured</p>
                    <p class="text-2xl font-bold text-purple-900">{{ dashboardStats.crypto_stats?.featured_count || 0 }}</p>
                  </div>
                  <div class="text-purple-400">
                    <svg class="h-8 w-8" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                    </svg>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Top Cryptocurrencies Preview -->
            <div class="bg-white border rounded-lg">
              <div class="px-6 py-4 border-b border-gray-200">
                <h4 class="text-md font-medium text-gray-900">Top 10 Cryptocurrencies</h4>
              </div>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">#</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                      <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                      <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">24h %</th>
                      <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Market Cap</th>
                      <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="crypto in cryptocurrencies.slice(0, 10)" :key="crypto.id" class="hover:bg-gray-50">
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ crypto.rank || '-' }}</td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex items-center">
                          <div class="flex-shrink-0 h-6 w-6">
                            <div class="h-6 w-6 rounded-full bg-gray-200 flex items-center justify-center">
                              <span class="text-xs font-bold text-gray-600">{{ crypto.symbol?.substring(0, 1) }}</span>
                            </div>
                          </div>
                          <div class="ml-3">
                            <div class="text-sm font-medium text-gray-900 flex items-center">
                              {{ crypto.name }}
                              <span v-if="crypto.is_featured" class="ml-1 text-yellow-400">⭐</span>
                              <span v-if="crypto.is_stablecoin" class="ml-1 text-blue-400">🏦</span>
                            </div>
                            <div class="text-sm text-gray-500">{{ crypto.symbol }}</div>
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                        ${{ formatPrice(crypto.current_price || 0) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-right text-sm"
                          :class="getPriceChangeClass(crypto.price_change_24h || 0)">
                        {{ formatPercent(crypto.price_change_24h || 0) }}%
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                        ${{ formatLargeNumber(crypto.market_cap || 0) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-center">
                        <span :class="[
                          'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                          crypto.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        ]">
                          {{ crypto.is_active ? 'Active' : 'Inactive' }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            
            <div class="text-center">
              <router-link to="/cryptocurrencies" class="btn-primary">
                View All {{ dashboardStats.crypto_stats?.total_count || 200 }}+ Cryptocurrencies →
              </router-link>
            </div>
          </div>

          <!-- Price Control Tab -->
          <div v-if="activeTab === 'price-control'" class="space-y-6">
            <h3 class="text-lg font-medium text-gray-900">Manual Price Control</h3>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <!-- Manual Price Control Form -->
              <div class="bg-gray-50 p-6 rounded-lg">
                <h4 class="text-md font-medium text-gray-800 mb-4">Instant Price Control</h4>
                
                <form @submit.prevent="executeManualPriceControl" class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Target</label>
                    <select v-model="priceControlForm.target_type" class="input-field">
                      <option value="crypto">Cryptocurrency</option>
                      <option value="index">Crypto Index</option>
                    </select>
                  </div>

                  <div v-if="priceControlForm.target_type === 'crypto'">
                    <label class="block text-sm font-medium text-gray-700">Cryptocurrency</label>
                    <select v-model="priceControlForm.cryptocurrency_id" class="input-field">
                      <option value="">Select cryptocurrency...</option>
                      <option v-for="crypto in cryptocurrencies" :key="crypto.id" :value="crypto.id">
                        {{ crypto.name }} ({{ crypto.symbol }})
                      </option>
                    </select>
                  </div>

                  <div v-if="priceControlForm.target_type === 'index'">
                    <label class="block text-sm font-medium text-gray-700">Crypto Index</label>
                    <select v-model="priceControlForm.crypto_index_id" class="input-field">
                      <option value="">Select index...</option>
                      <option v-for="index in cryptoIndices" :key="index.id" :value="index.id">
                        {{ index.name }} ({{ index.symbol }})
                      </option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Price Change (%)</label>
                    <input
                      v-model.number="priceControlForm.price_change_percent"
                      type="number"
                      step="0.1"
                      class="input-field"
                      placeholder="10.0"
                      required
                    />
                    <p class="text-xs text-gray-500 mt-1">
                      Positive for gains, negative for losses (e.g., 100 = +100%, -50 = -50%)
                    </p>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Duration (seconds)</label>
                    <input
                      v-model.number="priceControlForm.duration_seconds"
                      type="number"
                      min="1"
                      class="input-field"
                      placeholder="1"
                      required
                    />
                  </div>

                  <button type="submit" :disabled="executingPriceControl" class="btn-primary w-full">
                    <span v-if="executingPriceControl">Executing...</span>
                    <span v-else>Execute Price Change</span>
                  </button>
                </form>
              </div>

              <!-- Quick Actions -->
              <div class="space-y-4">
                <h4 class="text-md font-medium text-gray-800">Quick Actions</h4>
                
                <div class="grid grid-cols-2 gap-4">
                  <button @click="quickAction('moon')" class="btn-success text-sm">
                    🚀 Bitcoin Moon (+500%)
                  </button>
                  <button @click="quickAction('crash')" class="btn-danger text-sm">
                    📉 Market Crash (-80%)
                  </button>
                  <button @click="quickAction('pump')" class="btn-primary text-sm">
                    📈 Pump All (+20%)
                  </button>
                  <button @click="quickAction('dump')" class="btn-secondary text-sm">
                    📉 Dump All (-30%)
                  </button>
                </div>

                <div class="bg-yellow-50 p-4 rounded-lg">
                  <h5 class="text-sm font-medium text-yellow-800">⚠️ Warning</h5>
                  <p class="text-sm text-yellow-700 mt-1">
                    Price changes will immediately affect all user investments. Use with caution.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Scenarios Tab -->
          <div v-if="activeTab === 'scenarios'" class="space-y-6">
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-medium text-gray-900">Profit/Loss Scenarios</h3>
              <button @click="showCreateScenarioModal = true" class="btn-primary">
                Create New Scenario
              </button>
            </div>

            <!-- Active Scenarios -->
            <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              <div v-for="scenario in scenarios" :key="scenario.id" 
                   class="bg-white border rounded-lg p-4 shadow-sm">
                <div class="flex justify-between items-start mb-2">
                  <h4 class="text-md font-medium text-gray-900">{{ scenario.name }}</h4>
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    scenario.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  ]">
                    {{ scenario.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </div>
                
                <div class="space-y-2 text-sm text-gray-600">
                  <p><strong>Change:</strong> {{ scenario.percentage_change }}%</p>
                  <p><strong>Duration:</strong> {{ scenario.time_duration }} {{ scenario.time_unit }}</p>
                  <p><strong>Target:</strong> {{ scenario.target_crypto_name || scenario.target_index_name || 'All Investments' }}</p>
                  <p><strong>Executed:</strong> {{ scenario.times_executed }} times</p>
                </div>
                
                <div class="flex space-x-2 mt-4">
                  <button @click="executeScenario(scenario.id)" 
                          :disabled="executingScenarios.includes(scenario.id)"
                          class="btn-primary text-xs flex-1">
                    <span v-if="executingScenarios.includes(scenario.id)">Executing...</span>
                    <span v-else>Execute Now</span>
                  </button>
                  <button @click="toggleScenario(scenario)" 
                          :class="scenario.is_active ? 'btn-secondary' : 'btn-primary'" 
                          class="text-xs">
                    {{ scenario.is_active ? 'Deactivate' : 'Activate' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Create Scenario Modal -->
            <div v-if="showCreateScenarioModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
              <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                <div class="mt-3">
                  <h3 class="text-lg font-medium text-gray-900 mb-4">Create New Scenario</h3>
                  
                  <form @submit.prevent="createScenario" class="space-y-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700">Scenario Name</label>
                      <input
                        v-model="newScenario.name"
                        type="text"
                        class="input-field"
                        placeholder="Bitcoin Moon"
                        required
                      />
                    </div>

                    <div>
                      <label class="block text-sm font-medium text-gray-700">Type</label>
                      <select v-model="newScenario.scenario_type" class="input-field" required>
                        <option value="profit">Profit Scenario</option>
                        <option value="loss">Loss Scenario</option>
                        <option value="mixed">Mixed Scenario</option>
                      </select>
                    </div>

                    <div>
                      <label class="block text-sm font-medium text-gray-700">Percentage Change</label>
                      <input
                        v-model.number="newScenario.percentage_change"
                        type="number"
                        step="0.1"
                        class="input-field"
                        placeholder="100"
                        required
                      />
                      <p class="text-xs text-gray-500 mt-1">
                        Positive for gains, negative for losses
                      </p>
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                      <div>
                        <label class="block text-sm font-medium text-gray-700">Duration</label>
                        <input
                          v-model.number="newScenario.time_duration"
                          type="number"
                          min="1"
                          class="input-field"
                          placeholder="30"
                          required
                        />
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-gray-700">Unit</label>
                        <select v-model="newScenario.time_unit" class="input-field" required>
                          <option value="seconds">Seconds</option>
                          <option value="minutes">Minutes</option>
                          <option value="hours">Hours</option>
                          <option value="days">Days</option>
                        </select>
                      </div>
                    </div>

                    <div class="flex items-center">
                      <input
                        v-model="newScenario.apply_to_all_investments"
                        type="checkbox"
                        class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                      />
                      <label class="ml-2 block text-sm text-gray-900">Apply to all investments</label>
                    </div>

                    <div class="flex space-x-2">
                      <button type="button" @click="showCreateScenarioModal = false" class="btn-secondary flex-1">
                        Cancel
                      </button>
                      <button type="submit" :disabled="creatingScenario" class="btn-primary flex-1">
                        <span v-if="creatingScenario">Creating...</span>
                        <span v-else>Create</span>
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>

          <!-- Deposits Tab -->
          <div v-if="activeTab === 'deposits'" class="space-y-6">
            <h3 class="text-lg font-medium text-gray-900">Deposit Management</h3>
            
            <!-- Pending Deposits -->
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
              <h4 class="text-md font-medium text-yellow-800 mb-4">
                Pending Deposits ({{ pendingDeposits.length }})
              </h4>
              
              <div v-if="pendingDeposits.length === 0" class="text-yellow-700">
                No pending deposits requiring review.
              </div>
              
              <div v-else class="space-y-4">
                <div v-for="deposit in pendingDeposits" :key="deposit.id" 
                     class="bg-white border rounded-lg p-4">
                  <div class="flex justify-between items-start">
                    <div class="flex-1">
                      <p class="font-medium text-gray-900">{{ deposit.user_email }}</p>
                      <p class="text-sm text-gray-600">
                        {{ deposit.amount }} {{ deposit.cryptocurrency_symbol }}
                      </p>
                      <p class="text-sm text-gray-600">
                        To: {{ deposit.wallet_name }} ({{ deposit.wallet_address?.substring(0, 10) }}...)
                      </p>
                      <p class="text-sm text-gray-600">
                        TX: {{ deposit.transaction_hash || 'Not provided' }}
                      </p>
                      <p class="text-xs text-gray-500">
                        Submitted: {{ formatDate(deposit.created_at) }}
                      </p>
                    </div>
                    <div class="flex space-x-2 ml-4">
                      <button @click="approveDeposit(deposit.id)" 
                              :disabled="processingDeposits.includes(deposit.id)"
                              class="btn-success text-xs">
                        <span v-if="processingDeposits.includes(deposit.id)">Approving...</span>
                        <span v-else>Approve</span>
                      </button>
                      <button @click="rejectDeposit(deposit.id)" 
                              :disabled="processingDeposits.includes(deposit.id)"
                              class="btn-danger text-xs">
                        <span v-if="processingDeposits.includes(deposit.id)">Rejecting...</span>
                        <span v-else>Reject</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Deposit Wallets Management -->
            <div class="bg-white border rounded-lg p-6">
              <div class="flex justify-between items-center mb-4">
                <h4 class="text-md font-medium text-gray-800">Deposit Wallets</h4>
                <button @click="showCreateWalletModal = true" class="btn-primary text-sm">
                  Add Wallet
                </button>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="wallet in depositWallets" :key="wallet.id" 
                     class="border rounded-lg p-4">
                  <div class="flex justify-between items-start mb-2">
                    <h5 class="font-medium text-gray-900">{{ wallet.wallet_name }}</h5>
                    <span :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      wallet.is_primary ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                    ]">
                      {{ wallet.is_primary ? 'Primary' : 'Secondary' }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 mb-1">{{ wallet.cryptocurrency_symbol }}</p>
                  <p class="text-sm font-mono text-gray-600 break-all">{{ wallet.wallet_address }}</p>
                  <p class="text-sm text-gray-500 mt-2">
                    Balance: {{ formatBTC(wallet.current_balance) }} {{ wallet.cryptocurrency_symbol }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- System Monitor Tab -->
          <div v-if="activeTab === 'monitor'" class="space-y-6">
            <h3 class="text-lg font-medium text-gray-900">System Monitor</h3>
            
            <!-- System Health -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="bg-white border rounded-lg p-6">
                <h4 class="text-md font-medium text-gray-800 mb-4">System Status</h4>
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Trading:</span>
                    <span :class="systemHealth.system_status?.trading_enabled ? 'text-green-600' : 'text-red-600'">
                      {{ systemHealth.system_status?.trading_enabled ? 'ON' : 'OFF' }}
                    </span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Maintenance:</span>
                    <span :class="systemHealth.system_status?.maintenance_mode ? 'text-yellow-600' : 'text-green-600'">
                      {{ systemHealth.system_status?.maintenance_mode ? 'ON' : 'OFF' }}
                    </span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Stuck Tasks:</span>
                    <span :class="systemHealth.system_status?.stuck_tasks > 0 ? 'text-red-600' : 'text-green-600'">
                      {{ systemHealth.system_status?.stuck_tasks || 0 }}
                    </span>
                  </div>
                </div>
              </div>

              <div class="bg-white border rounded-lg p-6">
                <h4 class="text-md font-medium text-gray-800 mb-4">Task Health</h4>
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Price Updates:</span>
                    <span :class="systemHealth.task_health?.price_updates ? 'text-green-600' : 'text-red-600'">
                      {{ systemHealth.task_health?.price_updates ? '✓' : '✗' }}
                    </span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Investments:</span>
                    <span :class="systemHealth.task_health?.investment_calculations ? 'text-green-600' : 'text-red-600'">
                      {{ systemHealth.task_health?.investment_calculations ? '✓' : '✗' }}
                    </span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Portfolios:</span>
                    <span :class="systemHealth.task_health?.portfolio_updates ? 'text-green-600' : 'text-red-600'">
                      {{ systemHealth.task_health?.portfolio_updates ? '✓' : '✗' }}
                    </span>
                  </div>
                </div>
              </div>

              <div class="bg-white border rounded-lg p-6">
                <h4 class="text-md font-medium text-gray-800 mb-4">Today's Activity</h4>
                <div class="space-y-2">
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Price Movements:</span>
                    <span class="text-gray-900">{{ dashboardStats.price_movement_stats?.movements_today || 0 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Admin Controlled:</span>
                    <span class="text-gray-900">{{ dashboardStats.price_movement_stats?.admin_controlled_today || 0 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Completed Tasks:</span>
                    <span class="text-green-600">{{ dashboardStats.task_stats?.completed_tasks_today || 0 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-600">Failed Tasks:</span>
                    <span class="text-red-600">{{ dashboardStats.task_stats?.failed_tasks_today || 0 }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Recent Price Movements -->
            <div class="bg-white border rounded-lg p-6">
              <h4 class="text-md font-medium text-gray-800 mb-4">Recent Price Movements</h4>
              
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Target</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Change</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="movement in recentMovements" :key="movement.id">
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {{ movement.cryptocurrency_symbol || movement.crypto_index_symbol }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm" 
                          :class="movement.price_change_percent >= 0 ? 'text-green-600' : 'text-red-600'">
                        {{ formatPercent(movement.price_change_percent) }}%
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span :class="[
                          'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                          getMovementTypeClass(movement.movement_type)
                        ]">
                          {{ movement.movement_type }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ formatTime(movement.timestamp) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
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

// Reactive state
const activeTab = ref('settings')
const refreshing = ref(false)
const updatingSettings = ref(false)
const executingPriceControl = ref(false)
const executingScenarios = ref([])
const processingDeposits = ref([])
const creatingScenario = ref(false)
const showCreateScenarioModal = ref(false)
const showCreateWalletModal = ref(false)

// Data
const dashboardStats = ref({})
const systemStatus = ref({})
const systemHealth = ref({})
const tradingSettings = reactive({
  trading_enabled: true,
  maintenance_mode: false,
  profit_loss_mode: 'simulated',
  default_profit_rate: 5.0,
  default_loss_rate: 2.0,
  max_profit_rate: 100.0,
  max_loss_rate: 50.0,
  index_appreciation_rate: 10.0,
  index_depreciation_rate: 5.0,
  index_volatility_factor: 1.5,
  price_update_frequency: 1,
  investment_update_frequency: 5,
  portfolio_calculation_frequency: 10
})

const cryptocurrencies = ref([])
const cryptoIndices = ref([])
const scenarios = ref([])
const pendingDeposits = ref([])
const depositWallets = ref([])
const recentMovements = ref([])

// Forms
const priceControlForm = reactive({
  target_type: 'crypto',
  cryptocurrency_id: null,
  crypto_index_id: null,
  price_change_percent: 0,
  duration_seconds: 1
})

const newScenario = reactive({
  name: '',
  scenario_type: 'profit',
  percentage_change: 0,
  time_duration: 30,
  time_unit: 'seconds',
  apply_to_all_investments: false
})

// Computed
const tabs = [
  { id: 'settings', name: 'Trading Settings' },
  { id: 'cryptocurrencies', name: 'Cryptocurrencies' },
  { id: 'price-control', name: 'Price Control' },
  { id: 'scenarios', name: 'Scenarios' },
  { id: 'deposits', name: 'Deposits' },
  { id: 'monitor', name: 'System Monitor' }
]

// Methods
const formatBTC = (value) => {
  return parseFloat(value || 0).toFixed(8)
}

const formatPercent = (value) => {
  return parseFloat(value || 0).toFixed(2)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

const formatTime = (dateString) => {
  return new Date(dateString).toLocaleTimeString()
}

const formatPrice = (price) => {
  const num = parseFloat(price) || 0
  if (num < 0.01) return num.toFixed(6)
  if (num < 1) return num.toFixed(4)
  if (num < 100) return num.toFixed(2)
  return num.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
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

const getMovementTypeClass = (type) => {
  switch (type) {
    case 'admin_controlled':
      return 'bg-purple-100 text-purple-800'
    case 'scenario_based':
      return 'bg-blue-100 text-blue-800'
    case 'natural':
      return 'bg-green-100 text-green-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const loadCryptocurrencies = async () => {
  try {
    const response = await api.admin.getCryptocurrencies()
    cryptocurrencies.value = response.data.slice(0, 10) // Top 10 for dashboard preview
  } catch (error) {
    console.error('Error loading cryptocurrencies:', error)
  }
}

const refreshDashboard = async () => {
  refreshing.value = true
  try {
    await Promise.all([
      loadDashboardStats(),
      loadSystemHealth(),
      loadTradingSettings(),
      loadCryptocurrencies(),
      loadScenarios(),
      loadPendingDeposits(),
      loadRecentMovements()
    ])
  } finally {
    refreshing.value = false
  }
}

const loadDashboardStats = async () => {
  try {
    const response = await api.admin.getDashboardStats()
    dashboardStats.value = response.data
    systemStatus.value = {
      trading_enabled: response.data.trading_stats?.trading_enabled || false,
      maintenance_mode: response.data.trading_stats?.maintenance_mode || false
    }
  } catch (error) {
    console.error('Error loading dashboard stats:', error)
  }
}

const loadSystemHealth = async () => {
  try {
    const response = await api.admin.getSystemHealth()
    systemHealth.value = response.data
  } catch (error) {
    console.error('Error loading system health:', error)
  }
}

const loadTradingSettings = async () => {
  try {
    const response = await api.admin.getTradingSettings()
    Object.assign(tradingSettings, response.data)
  } catch (error) {
    console.error('Error loading trading settings:', error)
  }
}

const updateTradingSettings = async () => {
  updatingSettings.value = true
  try {
    await api.admin.updateTradingSettings(tradingSettings)
    toast.showToast('Settings updated successfully!', 'success')
  } catch (error) {
    toast.showToast('Failed to update settings', 'error')
    console.error('Error updating settings:', error)
  } finally {
    updatingSettings.value = false
  }
}

const loadScenarios = async () => {
  try {
    const response = await api.admin.getScenarios()
    scenarios.value = response.data
  } catch (error) {
    console.error('Error loading scenarios:', error)
  }
}

const loadPendingDeposits = async () => {
  try {
    const response = await api.admin.getPendingDeposits()
    pendingDeposits.value = response.data
  } catch (error) {
    console.error('Error loading pending deposits:', error)
  }
}

const loadRecentMovements = async () => {
  try {
    const response = await api.admin.getPriceMovements()
    recentMovements.value = response.data.slice(0, 10) // Show only last 10
  } catch (error) {
    console.error('Error loading recent movements:', error)
  }
}

const executeManualPriceControl = async () => {
  executingPriceControl.value = true
  try {
    const data = {
      price_change_percent: priceControlForm.price_change_percent,
      duration_seconds: priceControlForm.duration_seconds
    }
    
    if (priceControlForm.target_type === 'crypto') {
      data.cryptocurrency_id = priceControlForm.cryptocurrency_id
    } else {
      data.crypto_index_id = priceControlForm.crypto_index_id
    }
    
    const response = await api.admin.executeManualPriceControl(data)
    toast.showToast('Price change executed successfully!', 'success')
    
    // Refresh data
    await loadRecentMovements()
    
  } catch (error) {
    toast.showToast('Failed to execute price change', 'error')
    console.error('Error executing price control:', error)
  } finally {
    executingPriceControl.value = false
  }
}

const quickAction = async (action) => {
  const actions = {
    moon: { crypto: 'BTC', change: 500, target_type: 'crypto' },
    crash: { change: -80, target_type: 'all' },
    pump: { change: 20, target_type: 'all' },
    dump: { change: -30, target_type: 'all' }
  }
  
  const actionConfig = actions[action]
  if (actionConfig.target_type === 'all') {
    // Create a scenario for all investments
    const scenarioData = {
      name: `Quick ${action.toUpperCase()}`,
      scenario_type: actionConfig.change > 0 ? 'profit' : 'loss',
      percentage_change: actionConfig.change,
      time_duration: 1,
      time_unit: 'seconds',
      apply_to_all_investments: true
    }
    
    try {
      const response = await api.admin.createScenario(scenarioData)
      await api.admin.executeScenario(response.data.id)
      toast.showToast(`${action.toUpperCase()} executed successfully!`, 'success')
    } catch (error) {
      toast.showToast(`Failed to execute ${action}`, 'error')
    }
  }
}

const executeScenario = async (scenarioId) => {
  executingScenarios.value.push(scenarioId)
  try {
    await api.admin.executeScenario(scenarioId)
    toast.showToast('Scenario executed successfully!', 'success')
    await loadScenarios()
  } catch (error) {
    toast.showToast('Failed to execute scenario', 'error')
  } finally {
    const index = executingScenarios.value.indexOf(scenarioId)
    if (index > -1) executingScenarios.value.splice(index, 1)
  }
}

const approveDeposit = async (depositId) => {
  processingDeposits.value.push(depositId)
  try {
    await api.admin.approveDeposit(depositId, 'Approved by admin')
    toast.showToast('Deposit approved successfully!', 'success')
    await loadPendingDeposits()
  } catch (error) {
    toast.showToast('Failed to approve deposit', 'error')
  } finally {
    const index = processingDeposits.value.indexOf(depositId)
    if (index > -1) processingDeposits.value.splice(index, 1)
  }
}

const rejectDeposit = async (depositId) => {
  processingDeposits.value.push(depositId)
  try {
    await api.admin.rejectDeposit(depositId, 'Rejected by admin')
    toast.showToast('Deposit rejected', 'success')
    await loadPendingDeposits()
  } catch (error) {
    toast.showToast('Failed to reject deposit', 'error')
  } finally {
    const index = processingDeposits.value.indexOf(depositId)
    if (index > -1) processingDeposits.value.splice(index, 1)
  }
}

// Lifecycle
onMounted(async () => {
  await refreshDashboard()
  
  // Auto-refresh every 30 seconds
  setInterval(() => {
    if (!refreshing.value) {
      loadDashboardStats()
      loadSystemHealth()
      loadRecentMovements()
    }
  }, 30000)
})
</script>