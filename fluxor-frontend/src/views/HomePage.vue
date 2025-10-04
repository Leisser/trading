<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 relative overflow-hidden">
    <!-- Animated Background Elements -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl animate-pulse delay-500"></div>
    </div>

    <!-- Navigation -->
    <nav class="relative bg-black/30 backdrop-blur-xl border-b border-white/20 shadow-2xl">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-20">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl flex items-center justify-center shadow-lg">
              <span class="text-white font-bold text-lg">F</span>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-white tracking-tight">Fluxor</h1>
              <span class="text-xs text-purple-300 font-medium">Professional Trading</span>
            </div>
          </div>
          <div class="flex items-center space-x-6">
            <router-link 
              to="/login" 
              class="text-white/90 hover:text-white transition-all duration-300 font-medium relative group"
            >
              Sign In
              <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-purple-400 group-hover:w-full transition-all duration-300"></span>
            </router-link>
            <router-link 
              to="/register" 
              class="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-6 py-3 rounded-xl transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              Get Started
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32">
      <div class="text-center relative z-10">
        <div class="inline-flex items-center bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 mb-8">
          <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse mr-2"></span>
          <span class="text-white/90 text-sm font-medium">Live Market Data</span>
        </div>
        
        <h1 class="text-6xl md:text-7xl font-bold text-white mb-8 leading-tight">
          <span class="bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
            Advanced
          </span>
          <br>
          <span class="text-white">Cryptocurrency Trading</span>
        </h1>
        
        <p class="text-xl md:text-2xl text-purple-200 mb-12 max-w-4xl mx-auto leading-relaxed">
          Trade cryptocurrencies with <span class="text-purple-300 font-semibold">professional-grade tools</span>, 
          <span class="text-blue-300 font-semibold">real-time market data</span>, and 
          <span class="text-pink-300 font-semibold">advanced trading features</span>.
        </p>
        
        <div class="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6">
          <router-link 
            to="/register" 
            class="group bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 hover:from-purple-700 hover:via-pink-700 hover:to-blue-700 text-white px-10 py-4 rounded-2xl text-lg font-bold transition-all duration-300 shadow-2xl hover:shadow-purple-500/25 transform hover:-translate-y-1 hover:scale-105"
          >
            <span class="flex items-center">
              Start Trading
              <svg class="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
              </svg>
            </span>
          </router-link>
          
          <button 
            @click="scrollToFeatures" 
            class="group border-2 border-white/30 text-white hover:bg-white/10 px-10 py-4 rounded-2xl text-lg font-bold transition-all duration-300 backdrop-blur-sm hover:border-white/50"
          >
            <span class="flex items-center">
              Learn More
              <svg class="ml-2 w-5 h-5 group-hover:translate-y-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
              </svg>
            </span>
          </button>
        </div>
        
        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20 max-w-4xl mx-auto">
          <div class="text-center">
            <div class="text-4xl font-bold text-white mb-2">$2.4T+</div>
            <div class="text-purple-300">Total Market Cap</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold text-white mb-2">10,000+</div>
            <div class="text-purple-300">Active Traders</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold text-white mb-2">99.9%</div>
            <div class="text-purple-300">Uptime</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Market Data Section -->
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div class="text-center mb-16">
        <h2 class="text-5xl font-bold text-white mb-4">
          <span class="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
            Live Market Data
          </span>
        </h2>
        <p class="text-xl text-purple-200 max-w-2xl mx-auto">
          Real-time cryptocurrency prices and market insights
        </p>
      </div>
      
      <!-- Top 4 Cryptocurrencies Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
        <div 
          v-for="(crypto, index) in marketData.slice(0, 4)" 
          :key="crypto.symbol"
          class="group bg-white/10 backdrop-blur-xl rounded-2xl p-6 border border-white/20 hover:border-white/40 transition-all duration-300 hover:transform hover:-translate-y-2 hover:shadow-2xl"
          :style="{ animationDelay: `${index * 100}ms` }"
        >
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center space-x-3">
              <div class="w-12 h-12 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-lg">
                {{ crypto.rank }}
              </div>
              <div>
                <span class="text-white font-bold text-lg">{{ crypto.symbol }}</span>
                <div class="text-xs text-purple-300 font-medium">{{ crypto.name }}</div>
              </div>
            </div>
            <div class="text-right">
              <span :class="crypto.change_24h >= 0 ? 'text-green-400' : 'text-red-400'" class="text-lg font-bold">
                {{ crypto.change_24h >= 0 ? '+' : '' }}{{ crypto.change_24h.toFixed(1) }}%
              </span>
              <div class="text-xs text-purple-300">24h</div>
            </div>
          </div>
          
          <div class="space-y-3">
            <div class="text-3xl font-bold text-white">${{ formatPrice(crypto.price) }}</div>
            <div class="space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-purple-300">Volume</span>
                <span class="text-white font-medium">${{ formatVolume(crypto.volume_24h) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-purple-300">Market Cap</span>
                <span class="text-white font-medium">${{ formatVolume(crypto.market_cap) }}</span>
              </div>
            </div>
          </div>
          
          <!-- Progress bar for market cap -->
          <div class="mt-4">
            <div class="w-full bg-white/10 rounded-full h-1">
              <div 
                class="bg-gradient-to-r from-purple-400 to-blue-400 h-1 rounded-full transition-all duration-1000"
                :style="{ width: `${Math.min((crypto.market_cap / marketData[0].market_cap) * 100, 100)}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Complete Market Data Table -->
      <div class="bg-white/5 backdrop-blur-xl rounded-2xl border border-white/20 overflow-hidden shadow-2xl">
        <div class="p-6 border-b border-white/10">
          <h3 class="text-2xl font-bold text-white">Market Overview</h3>
          <p class="text-purple-300 mt-1">Complete cryptocurrency market data</p>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-white/10 to-white/5">
              <tr class="text-purple-300">
                <th class="px-6 py-4 text-left font-bold text-sm uppercase tracking-wider">#</th>
                <th class="px-6 py-4 text-left font-bold text-sm uppercase tracking-wider">Coin</th>
                <th class="px-6 py-4 text-right font-bold text-sm uppercase tracking-wider">Price</th>
                <th class="px-6 py-4 text-right font-bold text-sm uppercase tracking-wider">1h</th>
                <th class="px-6 py-4 text-right font-bold text-sm uppercase tracking-wider">24h</th>
                <th class="px-6 py-4 text-right font-bold text-sm uppercase tracking-wider">7d</th>
                <th class="px-6 py-4 text-right font-bold text-sm uppercase tracking-wider">30d</th>
                <th class="px-6 py-4 text-right font-bold text-sm uppercase tracking-wider">Volume</th>
                <th class="px-6 py-4 text-right font-bold text-sm uppercase tracking-wider">Market Cap</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr 
                v-for="(crypto, index) in marketData" 
                :key="crypto.symbol"
                class="hover:bg-white/5 transition-all duration-200 group"
              >
                <td class="px-6 py-4 text-purple-300 font-medium">{{ crypto.rank }}</td>
                <td class="px-6 py-4">
                  <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-xl flex items-center justify-center text-white font-bold shadow-lg">
                      {{ crypto.symbol.charAt(0) }}
                    </div>
                    <div>
                      <div class="text-white font-bold text-lg">{{ crypto.symbol }}</div>
                      <div class="text-purple-300 text-sm">{{ crypto.name }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-white font-bold text-right text-lg">${{ formatPrice(crypto.price) }}</td>
                <td class="px-6 py-4 text-right">
                  <span :class="crypto.change_1h >= 0 ? 'text-green-400 bg-green-400/10' : 'text-red-400 bg-red-400/10'" 
                        class="px-2 py-1 rounded-lg text-sm font-medium">
                    {{ crypto.change_1h >= 0 ? '+' : '' }}{{ crypto.change_1h.toFixed(1) }}%
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <span :class="crypto.change_24h >= 0 ? 'text-green-400 bg-green-400/10' : 'text-red-400 bg-red-400/10'" 
                        class="px-2 py-1 rounded-lg text-sm font-medium">
                    {{ crypto.change_24h >= 0 ? '+' : '' }}{{ crypto.change_24h.toFixed(1) }}%
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <span :class="crypto.change_7d >= 0 ? 'text-green-400 bg-green-400/10' : 'text-red-400 bg-red-400/10'" 
                        class="px-2 py-1 rounded-lg text-sm font-medium">
                    {{ crypto.change_7d >= 0 ? '+' : '' }}{{ crypto.change_7d.toFixed(1) }}%
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <span :class="crypto.change_30d >= 0 ? 'text-green-400 bg-green-400/10' : 'text-red-400 bg-red-400/10'" 
                        class="px-2 py-1 rounded-lg text-sm font-medium">
                    {{ crypto.change_30d >= 0 ? '+' : '' }}{{ crypto.change_30d.toFixed(1) }}%
                  </span>
                </td>
                <td class="px-6 py-4 text-purple-300 text-right font-medium">${{ formatVolume(crypto.volume_24h) }}</td>
                <td class="px-6 py-4 text-white font-bold text-right text-lg">${{ formatVolume(crypto.market_cap) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div id="features" class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="text-center mb-20">
        <h2 class="text-5xl font-bold text-white mb-6">
          <span class="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
            Trading Features
          </span>
        </h2>
        <p class="text-xl text-purple-200 max-w-3xl mx-auto">
          Professional-grade tools and features for serious cryptocurrency traders
        </p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div class="group bg-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 hover:border-white/40 transition-all duration-300 hover:transform hover:-translate-y-2 hover:shadow-2xl">
          <div class="w-16 h-16 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-white mb-4">Real-time Trading</h3>
          <p class="text-purple-200 text-lg leading-relaxed">Execute trades instantly with real-time market data and lightning-fast order processing.</p>
        </div>

        <div class="group bg-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 hover:border-white/40 transition-all duration-300 hover:transform hover:-translate-y-2 hover:shadow-2xl">
          <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-white mb-4">Advanced Analytics</h3>
          <p class="text-purple-200 text-lg leading-relaxed">Professional charting tools, technical indicators, and market analysis to make informed decisions.</p>
        </div>

        <div class="group bg-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 hover:border-white/40 transition-all duration-300 hover:transform hover:-translate-y-2 hover:shadow-2xl">
          <div class="w-16 h-16 bg-gradient-to-r from-green-600 to-emerald-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-white mb-4">Secure & Compliant</h3>
          <p class="text-purple-200 text-lg leading-relaxed">Bank-grade security with regulatory compliance and insurance protection for your assets.</p>
        </div>

        <div class="group bg-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 hover:border-white/40 transition-all duration-300 hover:transform hover:-translate-y-2 hover:shadow-2xl">
          <div class="w-16 h-16 bg-gradient-to-r from-yellow-600 to-orange-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-white mb-4">Portfolio Management</h3>
          <p class="text-purple-200 text-lg leading-relaxed">Track your investments, analyze performance, and manage your crypto portfolio efficiently.</p>
        </div>

        <div class="group bg-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 hover:border-white/40 transition-all duration-300 hover:transform hover:-translate-y-2 hover:shadow-2xl">
          <div class="w-16 h-16 bg-gradient-to-r from-red-600 to-pink-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM4.828 7l2.586 2.586a2 2 0 002.828 0L12.828 7H4.828zm0 10l2.586-2.586a2 2 0 012.828 0L12.828 17H4.828z"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-white mb-4">Risk Management</h3>
          <p class="text-purple-200 text-lg leading-relaxed">Advanced risk controls, stop-loss orders, and position sizing to protect your capital.</p>
        </div>

        <div class="group bg-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 hover:border-white/40 transition-all duration-300 hover:transform hover:-translate-y-2 hover:shadow-2xl">
          <div class="w-16 h-16 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-white mb-4">High Performance</h3>
          <p class="text-purple-200 text-lg leading-relaxed">Low latency execution, high-frequency trading support, and institutional-grade infrastructure.</p>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="relative bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 rounded-3xl p-16 text-center overflow-hidden">
        <!-- Background decoration -->
        <div class="absolute inset-0 bg-gradient-to-r from-purple-600/50 via-pink-600/50 to-blue-600/50"></div>
        <div class="absolute -top-20 -right-20 w-40 h-40 bg-white/10 rounded-full blur-2xl"></div>
        <div class="absolute -bottom-20 -left-20 w-40 h-40 bg-white/10 rounded-full blur-2xl"></div>
        
        <div class="relative z-10">
          <h2 class="text-5xl md:text-6xl font-bold text-white mb-6">Ready to Start Trading?</h2>
          <p class="text-xl md:text-2xl text-purple-100 mb-12 max-w-3xl mx-auto leading-relaxed">
            Join thousands of traders using Fluxor for their cryptocurrency investments. 
            <span class="text-white font-semibold">Start your journey today.</span>
          </p>
          <div class="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6">
            <router-link 
              to="/register" 
              class="group bg-white text-purple-600 hover:bg-purple-50 px-12 py-4 rounded-2xl text-xl font-bold transition-all duration-300 shadow-2xl hover:shadow-white/25 transform hover:-translate-y-1 hover:scale-105"
            >
              <span class="flex items-center">
                Create Free Account
                <svg class="ml-2 w-6 h-6 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                </svg>
              </span>
            </router-link>
            <button class="text-white border-2 border-white/30 hover:bg-white/10 px-12 py-4 rounded-2xl text-xl font-bold transition-all duration-300 backdrop-blur-sm">
              View Demo
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="relative bg-black/50 backdrop-blur-xl border-t border-white/20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-12">
          <div class="md:col-span-1">
            <div class="flex items-center space-x-3 mb-6">
              <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl flex items-center justify-center shadow-lg">
                <span class="text-white font-bold text-xl">F</span>
              </div>
              <div>
                <h3 class="text-2xl font-bold text-white">Fluxor</h3>
                <span class="text-sm text-purple-300">Professional Trading</span>
              </div>
            </div>
            <p class="text-purple-300 leading-relaxed mb-6">
              Professional cryptocurrency trading platform with advanced features, security, and institutional-grade infrastructure.
            </p>
            <div class="flex space-x-4">
              <a href="#" class="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                </svg>
              </a>
              <a href="#" class="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"/>
                </svg>
              </a>
              <a href="#" class="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
            </div>
          </div>
          
          <div>
            <h4 class="text-white font-bold text-lg mb-6">Trading</h4>
            <ul class="space-y-3 text-purple-300">
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">Spot Trading</a></li>
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">Futures</a></li>
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">Options</a></li>
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">Margin Trading</a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="text-white font-bold text-lg mb-6">Support</h4>
            <ul class="space-y-3 text-purple-300">
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">Help Center</a></li>
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">Contact Us</a></li>
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">API Documentation</a></li>
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">Status</a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="text-white font-bold text-lg mb-6">Legal</h4>
            <ul class="space-y-3 text-purple-300">
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">Terms of Service</a></li>
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">Privacy Policy</a></li>
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">Risk Disclosure</a></li>
              <li><a href="#" class="hover:text-white transition-colors duration-300 hover:translate-x-1 transform inline-block">Compliance</a></li>
            </ul>
          </div>
        </div>
        
        <div class="border-t border-white/10 mt-12 pt-8">
          <div class="flex flex-col md:flex-row justify-between items-center">
            <p class="text-purple-300 mb-4 md:mb-0">&copy; 2024 Fluxor. All rights reserved.</p>
            <div class="flex items-center space-x-6 text-sm text-purple-300">
              <span>Licensed & Regulated</span>
              <span>•</span>
              <span>Bank-Grade Security</span>
              <span>•</span>
              <span>24/7 Support</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Real cryptocurrency market data
const marketData = ref([
  { 
    rank: 1, 
    symbol: 'BTC', 
    name: 'Bitcoin', 
    price: 122104, 
    change_1h: 0.1, 
    change_24h: 0.5, 
    change_7d: 11.5, 
    change_30d: 11.0, 
    volume_24h: 36459039042, 
    circulating_supply: 19928203, 
    total_supply: 19930000, 
    market_cap: 2433318759440 
  },
  { 
    rank: 2, 
    symbol: 'ETH', 
    name: 'Ethereum', 
    price: 4486.01, 
    change_1h: 0.4, 
    change_24h: 1.3, 
    change_7d: 12.0, 
    change_30d: 4.9, 
    volume_24h: 21603209113, 
    circulating_supply: 120702395, 
    total_supply: 120700000, 
    market_cap: 541077386471 
  },
  { 
    rank: 3, 
    symbol: 'XRP', 
    name: 'XRP', 
    price: 2.95, 
    change_1h: 0.3, 
    change_24h: 2.8, 
    change_7d: 5.8, 
    change_30d: 5.9, 
    volume_24h: 3997658883, 
    circulating_supply: 59871700035, 
    total_supply: 99990000000, 
    market_cap: 176729111579 
  },
  { 
    rank: 4, 
    symbol: 'USDT', 
    name: 'Tether', 
    price: 1.00, 
    change_1h: 0.0, 
    change_24h: 0.0, 
    change_7d: 0.0, 
    change_30d: 0.0, 
    volume_24h: 72647530609, 
    circulating_supply: 176241404874, 
    total_supply: 176240000000, 
    market_cap: 176302387916 
  },
  { 
    rank: 5, 
    symbol: 'BNB', 
    name: 'BNB', 
    price: 1148.90, 
    change_1h: 0.4, 
    change_24h: 1.8, 
    change_7d: 18.6, 
    change_30d: 36.3, 
    volume_24h: 2966782382, 
    circulating_supply: 139184915, 
    total_supply: 139180000, 
    market_cap: 160129362550 
  },
  { 
    rank: 6, 
    symbol: 'SOL', 
    name: 'Solana', 
    price: 227.85, 
    change_1h: 0.4, 
    change_24h: 2.4, 
    change_7d: 13.0, 
    change_30d: 12.1, 
    volume_24h: 4858307248, 
    circulating_supply: 545359468, 
    total_supply: 611160000, 
    market_cap: 124277857925 
  },
  { 
    rank: 7, 
    symbol: 'USDC', 
    name: 'USDC', 
    price: 1.00, 
    change_1h: 0.0, 
    change_24h: 0.0, 
    change_7d: 0.0, 
    change_30d: 0.0, 
    volume_24h: 10227412498, 
    circulating_supply: 75366144659, 
    total_supply: 75370000000, 
    market_cap: 75384493126 
  },
  { 
    rank: 8, 
    symbol: 'STETH', 
    name: 'Lido Staked Ether', 
    price: 4481.47, 
    change_1h: 0.3, 
    change_24h: 1.2, 
    change_7d: 12.3, 
    change_30d: 4.9, 
    volume_24h: 14825050, 
    circulating_supply: 8524860, 
    total_supply: 8520000, 
    market_cap: 38199942698 
  },
  { 
    rank: 9, 
    symbol: 'DOGE', 
    name: 'Dogecoin', 
    price: 0.2501, 
    change_1h: 0.4, 
    change_24h: 3.9, 
    change_7d: 9.1, 
    change_30d: 18.6, 
    volume_24h: 2033001875, 
    circulating_supply: 151186236384, 
    total_supply: 151210000000, 
    market_cap: 37829049657 
  },
  { 
    rank: 10, 
    symbol: 'TRX', 
    name: 'TRON', 
    price: 0.3401, 
    change_1h: 0.0, 
    change_24h: 0.7, 
    change_7d: 0.7, 
    change_30d: 1.5, 
    volume_24h: 463902500, 
    circulating_supply: 94667155456, 
    total_supply: 94670000000, 
    market_cap: 32187004998 
  }
])

// Formatting functions
const formatPrice = (price: number): string => {
  if (price >= 1000) {
    return price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
  } else if (price >= 1) {
    return price.toFixed(2)
  } else {
    return price.toFixed(4)
  }
}

const formatVolume = (volume: number): string => {
  if (volume >= 1e12) {
    return (volume / 1e12).toFixed(1) + 'T'
  } else if (volume >= 1e9) {
    return (volume / 1e9).toFixed(1) + 'B'
  } else if (volume >= 1e6) {
    return (volume / 1e6).toFixed(1) + 'M'
  } else if (volume >= 1e3) {
    return (volume / 1e3).toFixed(1) + 'K'
  } else {
    return volume.toFixed(0)
  }
}

const formatSupply = (supply: number): string => {
  if (supply >= 1e12) {
    return (supply / 1e12).toFixed(1) + 'T'
  } else if (supply >= 1e9) {
    return (supply / 1e9).toFixed(1) + 'B'
  } else if (supply >= 1e6) {
    return (supply / 1e6).toFixed(1) + 'M'
  } else if (supply >= 1e3) {
    return (supply / 1e3).toFixed(1) + 'K'
  } else {
    return supply.toFixed(0)
  }
}

const scrollToFeatures = () => {
  document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
  // In production, fetch real market data from the API
  console.log('HomePage mounted - ready to fetch market data')
})
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
