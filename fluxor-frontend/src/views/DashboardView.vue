<template>
  <div class="dashboard_container">
    <!-- Enhanced Header -->
    <header class="dashboard_header">
      <div class="header_content">
        <div class="header_left">
          <h1 class="header_title"><span class="gradient-text">Fluxor</span> Trading</h1>
          <div class="header_nav">
            <router-link v-if="authStore.isAdmin" to="/admin" class="nav_link">
              <svg class="nav_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              Admin
            </router-link>
          </div>
        </div>
        <div class="header_right">
          <div class="user_info">
            <div class="user_avatar">
              <svg class="avatar_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </div>
            <div class="user_details">
              <span class="user_name">{{ authStore.user?.full_name }}</span>
              <span class="user_role">{{ authStore.user?.role }}</span>
            </div>
          </div>
          <div class="header_actions">
            <button
              @click="toggleTheme"
              class="action_btn theme_btn"
              :title="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
            >
              <svg
                v-if="theme === 'dark'"
                class="action_icon"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
              </svg>
              <svg v-else class="action_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4.22 2.47a1 1 0 011.42 1.42l-.7.7a1 1 0 11-1.42-1.42l.7-.7zM18 9a1 1 0 100 2h-1a1 1 0 100-2h1zM5.64 4.22a1 1 0 00-1.42 1.42l.7.7a1 1 0 101.42-1.42l-.7-.7zM4 10a1 1 0 100 2H3a1 1 0 100-2h1zm1.64 7.78a1 1 0 001.42-1.42l-.7-.7a1 1 0 10-1.42 1.42l.7.7zM10 16a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zm7-6a7 7 0 11-14 0 7 7 0 0114 0z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </button>
            <router-link to="/profile" class="action_btn">
              <svg class="action_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </router-link>
            <router-link to="/analytics" class="action_btn">
              <svg class="action_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"
                ></path>
              </svg>
              Analytics
            </router-link>
            <router-link to="/live-trade" class="action_btn">
              <svg class="action_icon" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path>
              </svg>
              Live Trade
            </router-link>
            <button @click="authStore.logout" class="action_btn logout_btn">
              <svg class="action_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>

    <div class="dashboard_content">
      <!-- Wallet Section -->
      <div class="wallet_section" style="margin-top: 2rem; margin-bottom: 2rem;">
        <div class="section_header" @click="toggleWalletAccordion" style="cursor: pointer;">
          <div class="header_left">
            <h3 class="section_title">My Crypto Wallets</h3>
            <span class="wallet_count">({{ tradingStore.cryptoWallets.length }} wallets)</span>
          </div>
          <div class="header_right">
            <button @click.stop="showCreateWalletModal = true" class="action_btn">
              <svg class="action_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              Create Wallet
            </button>
            <button @click.stop="refreshWallets" class="action_btn">
              <svg class="action_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              Refresh
            </button>
            <div class="accordion_icon" :class="{ expanded: walletAccordionOpen }">
              <svg fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </div>
          </div>
        </div>

        <!-- Accordion Content -->
        <div class="accordion_content" :class="{ expanded: walletAccordionOpen }">
          <!-- Wallet Summary -->
          <div class="wallet_summary">
            <div class="summary_card">
              <div class="summary_icon">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </div>
              <div class="summary_content">
                <h4 class="summary_title">Total Portfolio Value</h4>
                <p class="summary_value">{{ formatCurrency(tradingStore.totalPortfolioValue) }}</p>
              </div>
            </div>

            <div class="summary_card">
              <div class="summary_icon">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </div>
              <div class="summary_content">
                <h4 class="summary_title">Active Wallets</h4>
                <p class="summary_value">{{ tradingStore.cryptoWallets.length }}</p>
              </div>
            </div>

            <div class="summary_card">
              <div class="summary_icon">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </div>
              <div class="summary_content">
                <h4 class="summary_title">24h Change</h4>
                <p class="summary_value" :class="portfolioChange >= 0 ? 'positive' : 'negative'">
                  {{ portfolioChange >= 0 ? '+' : '' }}{{ portfolioChange.toFixed(2) }}%
                </p>
              </div>
            </div>
          </div>

          <!-- Wallet Grid -->
          <div v-if="tradingStore.cryptoWallets.length > 0" class="wallet_grid">
            <div v-for="wallet in tradingStore.cryptoWallets" :key="wallet.id" class="wallet_card">
              <div class="wallet_header">
                <div class="wallet_icon" :class="getWalletIconClass(wallet.wallet_type)">
                  <svg class="crypto_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 000 2h6a1 1 0 100-2H7z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                </div>
                <div class="wallet_info">
                  <h4 class="wallet_type">{{ wallet.wallet_type.toUpperCase() }}</h4>
                  <p class="wallet_label" v-if="wallet.label">{{ wallet.label }}</p>
                  <p class="wallet_address">{{ formatAddress(wallet.address) }}</p>
                </div>
                <div class="wallet_status">
                  <span class="status_badge" :class="wallet.is_active ? 'active' : 'inactive'">
                    {{ wallet.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </div>
              </div>

              <div class="wallet_balance_section">
                <div class="balance_info">
                  <span class="balance_amount">{{ formatCrypto(wallet.balance, wallet.wallet_type.toUpperCase()) }}</span>
                  <span class="balance_usd" v-if="getWalletUSDValue(wallet) > 0">
                    ≈ {{ formatCurrency(getWalletUSDValue(wallet)) }}
                  </span>
                </div>
                <div class="balance_change" v-if="getWalletPriceChange(wallet) !== 0">
                  <span :class="getWalletPriceChange(wallet) >= 0 ? 'positive' : 'negative'">
                    {{ getWalletPriceChange(wallet) >= 0 ? '+' : '' }}{{ getWalletPriceChange(wallet).toFixed(2) }}%
                  </span>
                </div>
              </div>

              <div class="wallet_actions">
                <button class="wallet_btn copy_btn" @click="copyAddress(wallet.address)" :title="`Copy ${wallet.wallet_type.toUpperCase()} address`">
                  <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z"></path>
                    <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z"></path>
                  </svg>
                  Copy
                </button>
                <button class="wallet_btn qr_btn" @click="showQRCode(wallet.address)" :title="`Show QR code for ${wallet.wallet_type.toUpperCase()}`">
                  <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M3 4a1 1 0 011-1h4a1 1 0 010 2H6.414l2.293 2.293a1 1 0 11-1.414 1.414L5 6.414V8a1 1 0 01-2 0V4zm9 1a1 1 0 010-2h4a1 1 0 011 1v4a1 1 0 01-2 0V6.414l-2.293-2.293a1 1 0 111.414-1.414L13.586 5H12zm-9 7a1 1 0 012 0v1.586l2.293-2.293a1 1 0 111.414 1.414L6.414 15H8a1 1 0 010 2H4a1 1 0 01-1-1v-4zm13-1a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 010-2h1.586l-2.293-2.293a1 1 0 111.414-1.414L15 13.586V12a1 1 0 011-1z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                  QR
                </button>
                <button class="wallet_btn deposit_btn" @click="showDepositModal(wallet)" :title="`Deposit ${wallet.wallet_type.toUpperCase()}`">
                  <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                  Deposit
                </button>
                <button class="wallet_btn withdraw_btn" @click="showWithdrawModal(wallet)" :title="`Withdraw ${wallet.wallet_type.toUpperCase()}`">
                  <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                  Withdraw
                </button>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="empty_state">
            <div class="empty_icon">
              <svg fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </div>
            <h3 class="empty_title">No Wallets Yet</h3>
            <p class="empty_description">Create your first crypto wallet to start trading and managing your digital assets.</p>
            <button @click="showCreateWalletModal = true" class="empty_action_btn">
              <svg class="action_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              Create Your First Wallet
            </button>
          </div>
        </div>
      </div>

      <!-- Stats Overview -->
      <div class="stats_grid">
        <div class="stat_card">
          <div class="stat_icon">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"
              ></path>
            </svg>
          </div>
          <div class="stat_content">
            <h3 class="stat_title">Portfolio Value</h3>
            <p class="stat_value">
              ${{
                formatPrice(
                  parseFloat(tradingStore.wallet?.balance || '0') *
                    (tradingStore.currentPrice?.binance || 0),
                )
              }}
            </p>
            <span class="stat_change positive">+2.45%</span>
          </div>
        </div>

        <div class="stat_card">
          <div class="stat_icon">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
          <div class="stat_content">
            <h3 class="stat_title">24h P&L</h3>
            <p class="stat_value">$1,234.56</p>
            <span class="stat_change positive">+5.67%</span>
          </div>
        </div>

        <div class="stat_card">
          <div class="stat_icon">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
          <div class="stat_content">
            <h3 class="stat_title">Total Trades</h3>
            <p class="stat_value">{{ tradingStore.trades.length }}</p>
            <span class="stat_change">This month</span>
          </div>
        </div>

        <div class="stat_card">
          <div class="stat_icon">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
          <div class="stat_content">
            <h3 class="stat_title">Win Rate</h3>
            <p class="stat_value">78.5%</p>
            <span class="stat_change positive">+2.1%</span>
          </div>
        </div>
      </div>

      <!-- ApexCharts Candlestick -->
      <div class="chart_section">
        <ApexCandlestickChart title="BTC/USD - Live Candlestick Chart" :height="400" />
      </div>

      <!-- Live Price Feed -->
      <div class="price_feed_section">
        <div class="section_header">
          <h2 class="section_title">Live Market Data</h2>
          <div class="section_actions">
            <button @click="tradingStore.fetchCurrentPrice" class="action_btn">
              <svg class="action_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </button>
            <button @click="togglePriceFeed" class="live_btn" :class="{ active: priceFeedActive }">
              <div class="live_indicator"></div>
              {{ priceFeedActive ? 'Stop' : 'Start' }} Live
            </button>
          </div>
        </div>

        <div v-if="tradingStore.currentPrice" class="price_grid">
          <div class="price_card">
            <div class="price_source">
              <div class="source_icon binance"></div>
              <span class="source_name">Binance</span>
            </div>
            <div class="price_value">${{ formatPrice(tradingStore.currentPrice.binance) }}</div>
            <div class="price_change positive">+1.23%</div>
          </div>

          <div class="price_card">
            <div class="price_source">
              <div class="source_icon coingecko"></div>
              <span class="source_name">CoinGecko</span>
            </div>
            <div class="price_value">${{ formatPrice(tradingStore.currentPrice.coingecko) }}</div>
            <div class="price_change positive">+1.18%</div>
          </div>

          <div class="price_card signal">
            <div class="price_source">
              <div class="source_icon signal_icon" :class="tradingStore.tradeSignal?.signal"></div>
              <span class="source_name">Signal</span>
            </div>
            <div class="price_value" :class="signalColor">
              {{ tradingStore.tradeSignal?.signal?.toUpperCase() || 'N/A' }}
            </div>
            <div class="price_change">RSI: 65</div>
          </div>
        </div>

        <div v-else class="loading_state">
          <div class="loading_spinner"></div>
          <p>Loading market data...</p>
        </div>
      </div>

      <!-- Trading Interface -->
      <div class="trading_interface">
        <div class="interface_grid">
          <!-- Trade Form -->
          <div class="trade_section">
            <div class="section_header">
              <h3 class="section_title">Crypto Trading</h3>
              <div class="trade_type_selector">
                <button
                  @click="tradeForm.trade_type = 'swap'"
                  class="type_btn"
                  :class="{ active: tradeForm.trade_type === 'swap' }"
                >
                  <svg class="type_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                  Token Swap
                </button>
                <button
                  @click="tradeForm.trade_type = 'spot'"
                  class="type_btn"
                  :class="{ active: tradeForm.trade_type === 'spot' }"
                >
                  <svg class="type_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                  Spot Buy
                </button>
              </div>
            </div>

            <!-- Token Swap Form -->
            <form v-if="tradeForm.trade_type === 'swap'" @submit.prevent="executeTrade" class="trade_form">
              <div class="form_group">
                <label class="form_label">From Token</label>
                <div class="token_selector">
                  <select v-model="tradeForm.from_token" class="token_select">
                    <option value="BTC">Bitcoin (BTC)</option>
                    <option value="ETH">Ethereum (ETH)</option>
                    <option value="SOL">Solana (SOL)</option>
                    <option value="ADA">Cardano (ADA)</option>
                    <option value="DOT">Polkadot (DOT)</option>
                    <option value="LINK">Chainlink (LINK)</option>
                  </select>
                </div>
              </div>

              <div class="form_group">
                <label class="form_label">Amount</label>
                <div class="input_wrapper">
                  <input
                    v-model.number="tradeForm.amount"
                    type="number"
                    step="0.00000001"
                    min="0"
                    class="trade_input"
                    placeholder="0.00"
                  ></input>
                  <span class="token_symbol">{{ tradeForm.from_token }}</span>
                </div>
              </div>

              <div class="swap_arrow">
                <svg class="swap_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </div>

              <div class="form_group">
                <label class="form_label">To Token</label>
                <div class="token_selector">
                  <select v-model="tradeForm.to_token" class="token_select">
                    <option value="ETH">Ethereum (ETH)</option>
                    <option value="BTC">Bitcoin (BTC)</option>
                    <option value="SOL">Solana (SOL)</option>
                    <option value="ADA">Cardano (ADA)</option>
                    <option value="DOT">Polkadot (DOT)</option>
                    <option value="LINK">Chainlink (LINK)</option>
                  </select>
                </div>
              </div>

              <div class="trade_summary">
                <div class="summary_item">
                  <span>You'll receive:</span>
                  <span>{{ calculateSwapOutput() }} {{ tradeForm.to_token }}</span>
                </div>
                <div class="summary_item">
                  <span>Exchange Rate:</span>
                  <span>1 {{ tradeForm.from_token }} = {{ getExchangeRate() }} {{ tradeForm.to_token }}</span>
                </div>
                <div class="summary_item">
                  <span>Network Fee:</span>
                  <span>~$2.50</span>
                </div>
              </div>

              <button
                type="submit"
                :disabled="tradingStore.loading"
                class="execute_btn swap"
              >
                <span v-if="tradingStore.loading" class="loading_spinner"></span>
                <span v-else>Swap {{ tradeForm.from_token }} → {{ tradeForm.to_token }}</span>
              </button>
            </form>

            <!-- Spot Buy Form -->
            <form v-else @submit.prevent="executeTrade" class="trade_form">
              <div class="form_group">
                <label class="form_label">Buy Token</label>
                <div class="token_selector">
                  <select v-model="tradeForm.buy_token" class="token_select">
                    <option value="BTC">Bitcoin (BTC)</option>
                    <option value="ETH">Ethereum (ETH)</option>
                    <option value="SOL">Solana (SOL)</option>
                    <option value="ADA">Cardano (ADA)</option>
                    <option value="DOT">Polkadot (DOT)</option>
                    <option value="LINK">Chainlink (LINK)</option>
                  </select>
                </div>
              </div>

              <div class="form_group">
                <label class="form_label">Amount (USD)</label>
                <div class="input_wrapper">
                  <span class="input_prefix">$</span>
                  <input
                    v-model.number="tradeForm.usd_amount"
                    type="number"
                    step="0.01"
                    min="0"
                    class="trade_input"
                    placeholder="0.00"
                  ></input>
                </div>
              </div>

              <div class="trade_summary">
                <div class="summary_item">
                  <span>You'll get:</span>
                  <span>{{ calculateSpotAmount() }} {{ tradeForm.buy_token }}</span>
                </div>
                <div class="summary_item">
                  <span>Current Price:</span>
                  <span>${{ getTokenPrice() }}</span>
                </div>
                <div class="summary_item">
                  <span>Trading Fee:</span>
                  <span>${{ (tradeForm.usd_amount * 0.001).toFixed(2) }}</span>
                </div>
              </div>

              <button
                type="submit"
                :disabled="tradingStore.loading"
                class="execute_btn spot"
              >
                <span v-if="tradingStore.loading" class="loading_spinner"></span>
                <span v-else>Buy {{ tradeForm.buy_token }}</span>
              </button>
            </form>

            <div v-if="tradingStore.error" class="error_message">
              <svg class="error_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              {{ tradingStore.error }}
            </div>
          </div>

          <div class="wallet_section">
            <div class="section_header">
              <h3 class="section_title">Wallet</h3>
              <button @click="refreshWallet" class="refresh_btn">
                <svg class="refresh_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </button>
            </div>

            <div v-if="tradingStore.wallet" class="wallet_content">
              <div class="wallet_balance">
                <div class="balance_icon">
                  <svg fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                </div>
                <div class="balance_info">
                  <span class="balance_label">Available Balance</span>
                  <span class="balance_amount">{{ tradingStore.wallet.balance }} BTC</span>
                  <span class="balance_usd"
                    >≈ ${{
                      formatPrice(
                        parseFloat(tradingStore.wallet?.balance || '0') *
                          (tradingStore.currentPrice?.binance || 0),
                      )
                    }}</span
                  >
                </div>
              </div>

              <div class="wallet_address">
                <span class="address_label">Wallet Address</span>
                <div class="address_display">
                  <span class="address_text">{{ tradingStore.wallet.address }}</span>
                  <button class="copy_btn">
                    <svg class="copy_icon" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z"></path>
                      <path
                        d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z"></path>
                    </svg>
                  </button>
                </div>
              </div>

              <div class="wallet_actions">
                <button @click="checkDeposits" class="wallet_btn secondary">
                  <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                  Check Deposits
                </button>
                <button @click="showWithdrawModal = true" class="wallet_btn primary">
                  <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                  Withdraw
                </button>
              </div>
            </div>

            <div v-else class="loading_state">
              <div class="loading_spinner"></div>
              <p>Loading wallet...</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Trade History -->
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">Trade History</h3>
          <button @click="tradingStore.fetchTrades" class="btn-secondary text-sm">Refresh</button>
        </div>

        <div v-if="tradingStore.trades.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Type
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Amount
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Price
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Status
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Date
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="trade in tradingStore.trades" :key="trade.id">
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="trade.trade_type === 'buy' ? 'text-green-600' : 'text-red-600'"
                    class="font-medium"
                  >
                    {{ trade.trade_type.toUpperCase() }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ trade.btc_amount }} BTC
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${{ trade.usd_price }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800"
                  >
                    {{ trade.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(trade.timestamp) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-center py-8">
          <p class="text-gray-500">No trades found</p>
        </div>
      </div>

      <!-- Create Wallet Modal -->
      <div v-if="showCreateWalletModal" class="modal_overlay" @click="showCreateWalletModal = false">
        <div class="modal_content" @click.stop>
          <div class="modal_header">
            <h3 class="modal_title">Create New Wallet</h3>
            <button @click="showCreateWalletModal = false" class="modal_close">
              <svg class="close_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </button>
    </div>

          <form @submit.prevent="createWallet" class="modal_form">
            <div class="form_group">
              <label class="form_label">Wallet Type</label>
              <select v-model="newWalletForm.wallet_type" class="form_select" required>
                <option value="bitcoin">Bitcoin (BTC)</option>
                <option value="ethereum">Ethereum (ETH)</option>
                <option value="solana">Solana (SOL)</option>
                <option value="cardano">Cardano (ADA)</option>
                <option value="polkadot">Polkadot (DOT)</option>
                <option value="chainlink">Chainlink (LINK)</option>
              </select>
            </div>

            <div class="form_group">
              <label class="form_label">Wallet Label (Optional)</label>
              <input
                v-model="newWalletForm.label"
                type="text"
                class="form_input"
                placeholder="e.g., My Trading Wallet"
              />
            </div>

            <div class="modal_footer">
              <button type="button" @click="showCreateWalletModal = false" class="btn_secondary">
                Cancel
              </button>
              <button type="submit" :disabled="tradingStore.loading" class="btn_primary">
                <span v-if="tradingStore.loading" class="loading_spinner"></span>
                <span v-else>Create Wallet</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTradingStore } from '@/stores/trading'
import { useToast } from '@/composables/useToast'
import ApexCandlestickChart from '@/components/ApexCandlestickChart.vue'
import Toast from '@/components/Toast.vue'

const router = useRouter()
const authStore = useAuthStore()
const tradingStore = useTradingStore()
const { showToast } = useToast()

// Reactive state
const theme = ref('light')
const priceFeedActive = ref(false)

// Trade form for crypto swaps and spot trading
const tradeForm = reactive({
  trade_type: 'swap' as 'swap' | 'spot',
  // Swap fields
  from_token: 'BTC',
  to_token: 'ETH',
  amount: 0,
  // Spot fields
  buy_token: 'BTC',
  usd_amount: 0,
})

// Crypto wallet management
const showCreateWalletModal = ref(false)
const newWalletForm = reactive({
  wallet_type: 'ethereum',
  label: ''
})

// Crypto payment
const showPaymentModal = ref(false)
const paymentForm = reactive({
  amount_usd: 0,
  cryptocurrency: 'BTC'
})

// Computed properties
const isDarkMode = computed(() => theme.value === 'dark')

// Methods
const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  localStorage.setItem('theme', theme.value)
  document.documentElement.setAttribute('data_theme', theme.value)
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}

const formatPrice = (price: number) => {
  return price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const togglePriceFeed = () => {
  if (priceFeedActive.value) {
    tradingStore.disconnectPriceFeed()
    priceFeedActive.value = false
  } else {
    tradingStore.connectPriceFeed()
    priceFeedActive.value = true
  }
}

const executeTrade = async () => {
  try {
    if (tradeForm.trade_type === 'swap') {
      // Execute crypto swap
      const fromToken = tradingStore.supportedTokens.find(t => t.symbol === tradeForm.from_token)
      const toToken = tradingStore.supportedTokens.find(t => t.symbol === tradeForm.to_token)

      if (!fromToken || !toToken) {
        showToast('Invalid token selection', 'error')
        return
      }

      await tradingStore.executeSwap(fromToken.id, toToken.id, tradeForm.amount)
      showToast('Swap executed successfully!', 'success')

    // Reset form
    tradeForm.amount = 0
    } else {
      // Execute spot buy
      const buyToken = tradingStore.supportedTokens.find(t => t.symbol === tradeForm.buy_token)

      if (!buyToken) {
        showToast('Invalid token selection', 'error')
        return
      }

      await tradingStore.executeTrade({
        cryptocurrency_id: buyToken.id,
        trade_type: 'buy',
        amount: parseFloat(calculateSpotAmount()),
        leverage: 1
      })
      showToast('Spot buy executed successfully!', 'success')

      // Reset form
      tradeForm.usd_amount = 0
    }
  } catch (error) {
    showToast(error instanceof Error ? error.message : 'Trade execution failed', 'error')
  }
}

const createWallet = async () => {
  try {
    await tradingStore.createCryptoWallet(newWalletForm.wallet_type)
    showToast('Wallet created successfully!', 'success')
    showCreateWalletModal.value = false
    newWalletForm.label = ''
    newWalletForm.wallet_type = 'ethereum'
  } catch (error) {
    showToast(error instanceof Error ? error.message : 'Failed to create wallet', 'error')
  }
}

const createPayment = async () => {
  try {
    const result = await tradingStore.createPayment(paymentForm.amount_usd, paymentForm.cryptocurrency)
    showToast('Payment created successfully!', 'success')
    showPaymentModal.value = false
    paymentForm.amount_usd = 0

    // Open payment URL in new tab
    if (result.payment?.payment_url) {
      window.open(result.payment.payment_url, '_blank')
    }
  } catch (error) {
    showToast(error instanceof Error ? error.message : 'Failed to create payment', 'error')
  }
}



const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

const formatCrypto = (amount: number, symbol: string) => {
  return `${amount.toFixed(8)} ${symbol}`
}

// Swap calculation functions
const calculateSwapOutput = () => {
  // This would get real rates from the backend
  const rates: Record<string, number> = {
    'BTC-ETH': 15.5,
    'BTC-SOL': 1200,
    'BTC-ADA': 45000,
    'BTC-DOT': 1800,
    'BTC-LINK': 1200,
    'ETH-BTC': 0.064,
    'ETH-SOL': 77,
    'ETH-ADA': 2900,
    'ETH-DOT': 116,
    'ETH-LINK': 77,
    'SOL-BTC': 0.00083,
    'SOL-ETH': 0.013,
    'SOL-ADA': 37.5,
    'SOL-DOT': 1.5,
    'SOL-LINK': 1,
    'ADA-BTC': 0.000022,
    'ADA-ETH': 0.00034,
    'ADA-SOL': 0.027,
    'ADA-DOT': 0.04,
    'ADA-LINK': 0.027,
    'DOT-BTC': 0.00056,
    'DOT-ETH': 0.0086,
    'DOT-SOL': 0.67,
    'DOT-ADA': 25,
    'DOT-LINK': 0.67,
    'LINK-BTC': 0.00083,
    'LINK-ETH': 0.013,
    'LINK-SOL': 1,
    'LINK-ADA': 37.5,
    'LINK-DOT': 1.5,
  }

  const pair = `${tradeForm.from_token}-${tradeForm.to_token}`
  const rate = rates[pair] || 1
  return (tradeForm.amount * rate).toFixed(8)
}

const getExchangeRate = () => {
  const rates: Record<string, number> = {
    'BTC-ETH': 15.5,
    'BTC-SOL': 1200,
    'BTC-ADA': 45000,
    'BTC-DOT': 1800,
    'BTC-LINK': 1200,
    'ETH-BTC': 0.064,
    'ETH-SOL': 77,
    'ETH-ADA': 2900,
    'ETH-DOT': 116,
    'ETH-LINK': 77,
    'SOL-BTC': 0.00083,
    'SOL-ETH': 0.013,
    'SOL-ADA': 37.5,
    'SOL-DOT': 1.5,
    'SOL-LINK': 1,
    'ADA-BTC': 0.000022,
    'ADA-ETH': 0.00034,
    'ADA-SOL': 0.027,
    'ADA-DOT': 0.04,
    'ADA-LINK': 0.027,
    'DOT-BTC': 0.00056,
    'DOT-ETH': 0.0086,
    'DOT-SOL': 0.67,
    'DOT-ADA': 25,
    'DOT-LINK': 0.67,
    'LINK-BTC': 0.00083,
    'LINK-ETH': 0.013,
    'LINK-SOL': 1,
    'LINK-ADA': 37.5,
    'LINK-DOT': 1.5,
  }

  const pair = `${tradeForm.from_token}-${tradeForm.to_token}`
  return rates[pair] || 1
}

const calculateSpotAmount = () => {
  const prices: Record<string, number> = {
    'BTC': 45000,
    'ETH': 2900,
    'SOL': 58,
    'ADA': 0.45,
    'DOT': 7.5,
    'LINK': 7.5,
  }

  const price = prices[tradeForm.buy_token] || 1
  return (tradeForm.usd_amount / price).toFixed(8)
}

const getTokenPrice = () => {
  const prices: Record<string, number> = {
    'BTC': 45000,
    'ETH': 2900,
    'SOL': 58,
    'ADA': 0.45,
    'DOT': 7.5,
    'LINK': 7.5,
  }

  return prices[tradeForm.buy_token] || 1
}

// Lifecycle hooks
onMounted(async () => {
  // Initialize theme
  const savedTheme = localStorage.getItem('theme') || 'light'
  theme.value = savedTheme
  document.documentElement.setAttribute('data_theme', savedTheme)

  // Initialize trading data
  await tradingStore.initializeData()

  // Connect to price feed
  tradingStore.connectPriceFeed()
})

onUnmounted(() => {
  tradingStore.disconnectPriceFeed()
})

const copyAddress = async (address: string) => {
  try {
    await navigator.clipboard.writeText(address)
    showToast('Address copied to clipboard!', 'success')
  } catch (error) {
    showToast('Failed to copy address', 'error')
  }
}

const showQRCode = (address: string) => {
  // In a real app, you would show a QR code modal
  // For now, we'll just copy the address
  copyAddress(address)
}

const getWalletIconClass = (walletType: string) => {
  switch (walletType) {
    case 'bitcoin':
      return 'bitcoin'
    case 'ethereum':
      return 'ethereum'
    case 'solana':
      return 'solana'
    case 'cardano':
      return 'cardano'
    case 'polkadot':
      return 'polkadot'
    case 'chainlink':
      return 'chainlink'
    default:
      return 'default'
  }
}

const getWalletUSDValue = (wallet: any) => {
  const price = tradingStore.currentPrice?.binance || 0
  return wallet.balance * price
}

const getWalletPriceChange = (wallet: any) => {
  // For now, return a mock value since we don't have previous price data
  // In a real app, this would be calculated from historical price data
  return Math.random() * 10 - 5 // Mock change between -5% and +5%
}

const portfolioChange = computed(() => {
  // For now, return a mock value since we don't have previous portfolio value
  // In a real app, this would be calculated from historical data
  return 2.45 // Mock 2.45% increase
})

const formatAddress = (address: string) => {
  return address.length > 20 ? address.slice(0, 10) + '...' + address.slice(-10) : address
}

const showDepositModal = (wallet: any) => {
  // Implement deposit modal logic
  console.log(`Deposit ${wallet.wallet_type.toUpperCase()}`)
  showToast(`Deposit modal for ${wallet.wallet_type.toUpperCase()} would open here`, 'info')
}

const showWithdrawModal = (wallet: any) => {
  // Implement withdraw modal logic
  console.log(`Withdraw ${wallet.wallet_type.toUpperCase()}`)
  showToast(`Withdraw modal for ${wallet.wallet_type.toUpperCase()} would open here`, 'info')
}

const refreshWallets = async () => {
  try {
    await tradingStore.fetchWalletBalances()
    showToast('Wallets refreshed successfully!', 'success')
  } catch (error) {
    showToast('Failed to refresh wallets', 'error')
  }
}

const toggleWalletAccordion = () => {
  walletAccordionOpen.value = !walletAccordionOpen.value
}

const walletAccordionOpen = ref(false)
</script>

<style scoped>
.dashboard_container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.dashboard_header {
  background: var(--bg-primary);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-primary);
  box-shadow: var(--shadow-lg);
  color: var(--text-primary);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 50;
}

[data-theme="dark"] .dashboard_header {
  background: rgba(17, 24, 39, 0.95);
  border-bottom: 1px solid rgba(55, 65, 81, 0.5);
  box-shadow: var(--shadow-xl);
}

.header_content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header_left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.header_title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.025em;
}

.header_nav {
  display: flex;
  gap: 1rem;
}

.nav_link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: 0.5rem;
  transition: all 0.2s;
}

.nav_link:hover {
  color: var(--text-primary);
  background: rgba(107, 114, 128, 0.1);
}

.nav_icon {
  width: 1.25rem;
  height: 1.25rem;
}

.header_right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user_info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.5);
}

.user_avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.avatar_icon {
  width: 1.5rem;
  height: 1.5rem;
}

.user_details {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.user_name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
}

.user_role {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: capitalize;
}

.header_actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: var(--text-primary);
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 140px;
  justify-content: center;
  box-shadow: var(--shadow-sm);
}

.action_btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-colored);
}

.action_icon {
  width: 1.25rem;
  height: 1.25rem;
}

.theme_btn {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.theme_btn:hover {
  background: rgba(59, 130, 246, 0.2);
}

.logout_btn {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.logout_btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

.dashboard_content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.stats_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat_card {
  background: var(--bg-secondary);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-primary);
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  color: var(--text-primary);
}

.stat_card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl);
}

[data-theme="dark"] .stat_card {
  background: rgba(31, 41, 55, 0.9);
  border: 1px solid rgba(55, 65, 81, 0.5);
  box-shadow: var(--shadow-lg);
}

[data-theme="dark"] .stat_card:hover {
  box-shadow: var(--shadow-2xl);
}

.stat_icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.stat_icon svg {
  width: 1.5rem;
  height: 1.5rem;
}

.stat_content {
  flex: 1;
}

.stat_title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 0.5rem 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat_value {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 0.25rem 0;
}

.stat_change {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0;
}

.stat_change.positive {
  color: #10b981;
}

.chart_section {
  background: var(--bg-secondary);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-primary);
  box-shadow: var(--shadow-lg);
  color: var(--text-primary);
}

[data-theme="dark"] .chart_section {
  background: rgba(31, 41, 55, 0.9);
  border: 1px solid rgba(55, 65, 81, 0.5);
  box-shadow: var(--shadow-xl);
}

.price_feed_section {
  background: var(--bg-secondary);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-primary);
  box-shadow: var(--shadow-lg);
  color: var(--text-primary);
}

[data-theme="dark"] .price_feed_section {
  background: rgba(31, 41, 55, 0.9);
  border: 1px solid rgba(55, 65, 81, 0.5);
  box-shadow: var(--shadow-xl);
}

.section_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--bg-primary);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-primary);
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  color: var(--text-primary);
}

.section_header:hover {
  background: var(--bg-primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}

[data-theme="dark"] .section_header {
  background: rgba(31, 41, 55, 0.95);
  border: 1px solid rgba(55, 65, 81, 0.5);
  box-shadow: var(--shadow-lg);
}

[data-theme="dark"] .section_header:hover {
  background: rgba(31, 41, 55, 0.98);
  box-shadow: var(--shadow-xl);
}

.header_left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.wallet_count {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.header_right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.accordion_icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--text-secondary);
  transition: transform 0.3s ease;
  cursor: pointer;
}

.accordion_icon.expanded {
  transform: rotate(180deg);
}

.accordion_content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, opacity 0.3s ease;
  opacity: 0;
}

.accordion_content.expanded {
  max-height: 2000px;
  opacity: 1;
  margin-top: 1rem;
}

.section_title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.section_actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.live_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.5rem;
  background: rgba(107, 114, 128, 0.1);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
  font-weight: 600;
}

.live_btn:hover {
  background: rgba(107, 114, 128, 0.2);
}

.live_btn.active {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.live_indicator {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.price_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.price_card {
  background: var(--bg-tertiary);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-secondary);
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  color: var(--text-primary);
}

.price_card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

[data-theme="dark"] .price_card {
  background: rgba(31, 41, 55, 0.8);
  border: 1px solid rgba(55, 65, 81, 0.3);
  box-shadow: var(--shadow-lg);
}

[data-theme="dark"] .price_card:hover {
  box-shadow: var(--shadow-xl);
}

.price_card.signal {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.2);
}

.price_source {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.source_icon {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 0.375rem;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.source_icon.binance {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.source_icon.coingecko {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.source_icon.signal_icon {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.source_icon.signal_icon.buy {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.source_icon.signal_icon.sell {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.source_name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.price_value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
}

.price_change {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.price_change.positive {
  color: #10b981;
}

.loading_state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  color: var(--text-secondary);
}

.loading_spinner {
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(107, 114, 128, 0.2);
  border-top: 2px solid var(--text-secondary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.trading_interface {
  background: var(--bg-secondary);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-primary);
  box-shadow: var(--shadow-lg);
  color: var(--text-primary);
}

[data-theme="dark"] .trading_interface {
  background: rgba(31, 41, 55, 0.9);
  border: 1px solid rgba(55, 65, 81, 0.5);
  box-shadow: var(--shadow-xl);
}

.interface_grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.trade_section {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid rgba(229, 231, 235, 0.3);
}

.trade_type_selector {
  display: flex;
  gap: 0.5rem;
  background: rgba(107, 114, 128, 0.1);
  border-radius: 0.5rem;
  padding: 0.25rem;
}

.type_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
  font-weight: 600;
  flex: 1;
}

.type_btn:hover {
  background: rgba(255, 255, 255, 0.5);
}

.type_btn.active {
  background: white;
  color: var(--text-primary);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.type_icon {
  width: 1rem;
  height: 1rem;
}

.trade_form {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form_group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form_label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.input_wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input_prefix {
  position: absolute;
  left: 0.75rem;
  color: var(--text-secondary);
  font-weight: 600;
  z-index: 1;
}

.trade_input {
  width: 100%;
  padding: 0.75rem 0.75rem 0.75rem 1.5rem;
  border: 1px solid rgba(209, 213, 219, 0.5);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  transition: all 0.2s;
}

.trade_input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.leverage_slider {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.slider {
  flex: 1;
  height: 0.375rem;
  border-radius: 0.1875rem;
  background: rgba(209, 213, 219, 0.5);
  outline: none;
  -webkit-appearance: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.slider::-moz-range-thumb {
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.leverage_value {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  min-width: 2rem;
  text-align: center;
}

.trade_summary {
  background: rgba(107, 114, 128, 0.05);
  border-radius: 0.5rem;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.summary_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.summary_item span:first-child {
  color: var(--text-secondary);
}

.summary_item span:last-child {
  font-weight: 600;
  color: var(--text-primary);
}

.execute_btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.execute_btn.buy {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.execute_btn.buy:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.execute_btn.sell {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.execute_btn.sell:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.execute_btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.error_message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 0.5rem;
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 1rem;
}

.error_icon {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
}

.wallet_section {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid rgba(229, 231, 235, 0.3);
}

.refresh_btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border: none;
  border-radius: 0.375rem;
  background: rgba(107, 114, 128, 0.1);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.refresh_btn:hover {
  background: rgba(107, 114, 128, 0.2);
}

.refresh_icon {
  width: 1rem;
  height: 1rem;
}

.wallet_content {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.wallet_balance {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 0.5rem;
  border: 1px solid rgba(229, 231, 235, 0.3);
}

.balance_icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.balance_icon svg {
  width: 1.25rem;
  height: 1.25rem;
}

.balance_info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.balance_label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.balance_amount {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
}

.balance_usd {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.wallet_address {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.address_label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.address_display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(229, 231, 235, 0.3);
  border-radius: 0.5rem;
}

.address_text {
  flex: 1;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875rem;
  color: var(--text-secondary);
  word-break: break-all;
}

.copy_btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border: none;
  border-radius: 0.375rem;
  background: rgba(107, 114, 128, 0.1);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.copy_btn:hover {
  background: rgba(107, 114, 128, 0.2);
}

.copy_icon {
  width: 1rem;
  height: 1rem;
}

.wallet_actions {
  display: flex;
  gap: 0.75rem;
}

.wallet_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  box-shadow: var(--shadow-sm);
}

.wallet_btn.secondary {
  background: rgba(107, 114, 128, 0.1);
  color: var(--text-secondary);
}

.wallet_btn.secondary:hover {
  background: rgba(107, 114, 128, 0.2);
}

.wallet_btn.primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.wallet_btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn_icon {
  width: 1rem;
  height: 1rem;
}

.card {
  background: var(--bg-secondary);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-primary);
  box-shadow: var(--shadow-lg);
  color: var(--text-primary);
}

[data-theme="dark"] .card {
  background: rgba(31, 41, 55, 0.9);
  border: 1px solid rgba(55, 65, 81, 0.5);
  box-shadow: var(--shadow-xl);
}

.btn-secondary {
  padding: 0.5rem 1rem;
  border: 1px solid rgba(209, 213, 219, 0.5);
  border-radius: 0.375rem;
  background: rgba(255, 255, 255, 0.8);
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(107, 114, 128, 0.1);
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.input-field {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(209, 213, 219, 0.5);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  font-size: 0.875rem;
  transition: all 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Dark mode styles */
[data_theme='dark'] .dashboard_container {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
}

[data_theme='dark'] .dashboard_header {
  background: rgba(31, 41, 55, 0.95);
  border-bottom-color: rgba(75, 85, 99, 0.5);
}

[data_theme='dark'] .header_title {
  color: #f9fafb;
}

[data_theme='dark'] .nav_link {
  color: #9ca3af;
}

[data_theme='dark'] .nav_link:hover {
  color: #f9fafb;
  background: rgba(156, 163, 175, 0.1);
}

[data_theme='dark'] .user_info {
  background: rgba(31, 41, 55, 0.5);
}

[data_theme='dark'] .user_name {
  color: #f9fafb;
}

[data_theme='dark'] .user_role {
  color: #9ca3af;
}

[data_theme='dark'] .action_btn {
  background: rgba(31, 41, 55, 0.5);
  color: #9ca3af;
}

[data_theme='dark'] .action_btn:hover {
  background: rgba(156, 163, 175, 0.1);
  color: #f9fafb;
}

[data_theme='dark'] .stat_card,
[data_theme='dark'] .chart_section,
[data_theme='dark'] .price_feed_section,
[data_theme='dark'] .trading_interface,
[data_theme='dark'] .card {
  background: rgba(31, 41, 55, 0.8);
  border-color: rgba(75, 85, 99, 0.5);
}

[data_theme='dark'] .section_title {
  color: #f9fafb;
}

[data_theme='dark'] .stat_title {
  color: #9ca3af;
}

[data_theme='dark'] .stat_value {
  color: #f9fafb;
}

[data_theme='dark'] .stat_change {
  color: #9ca3af;
}

[data_theme='dark'] .price_card {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(75, 85, 99, 0.3);
}

[data_theme='dark'] .source_name {
  color: #9ca3af;
}

[data_theme='dark'] .price_value {
  color: #f9fafb;
}

[data_theme='dark'] .price_change {
  color: #9ca3af;
}

[data_theme='dark'] .trade_section,
[data_theme='dark'] .wallet_section {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(75, 85, 99, 0.3);
}

[data_theme='dark'] .form_label {
  color: #d1d5db;
}

[data_theme='dark'] .trade_input,
[data_theme='dark'] .input-field {
  background: rgba(31, 41, 55, 0.8);
  border-color: rgba(75, 85, 99, 0.5);
  color: #f9fafb;
}

[data_theme='dark'] .trade_input:focus,
[data_theme='dark'] .input-field:focus {
  border-color: #3b82f6;
}

[data_theme='dark'] .type_btn {
  color: #9ca3af;
}

[data_theme='dark'] .type_btn:hover {
  background: rgba(31, 41, 55, 0.5);
}

[data_theme='dark'] .type_btn.active {
  background: #374151;
  color: #f9fafb;
}

[data_theme='dark'] .trade_summary {
  background: rgba(75, 85, 99, 0.1);
}

[data_theme='dark'] .summary_item span:first-child {
  color: #9ca3af;
}

[data_theme='dark'] .summary_item span:last-child {
  color: #f9fafb;
}

[data_theme='dark'] .wallet_balance {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(75, 85, 99, 0.3);
}

[data_theme='dark'] .balance_label {
  color: #9ca3af;
}

[data_theme='dark'] .balance_amount {
  color: #f9fafb;
}

[data_theme='dark'] .balance_usd {
  color: #9ca3af;
}

[data_theme='dark'] .address_label {
  color: #d1d5db;
}

[data_theme='dark'] .address_display {
  background: rgba(31, 41, 55, 0.5);
  border-color: rgba(75, 85, 99, 0.3);
}

[data_theme='dark'] .address_text {
  color: #9ca3af;
}

[data_theme='dark'] .copy_btn,
[data_theme='dark'] .refresh_btn {
  background: rgba(75, 85, 99, 0.1);
  color: #9ca3af;
}

[data_theme='dark'] .copy_btn:hover,
[data_theme='dark'] .refresh_btn:hover {
  background: rgba(75, 85, 99, 0.2);
}

[data_theme='dark'] .wallet_btn.secondary {
  background: rgba(75, 85, 99, 0.1);
  color: #9ca3af;
}

[data_theme='dark'] .wallet_btn.secondary:hover {
  background: rgba(75, 85, 99, 0.2);
}

[data_theme='dark'] .btn-secondary {
  background: rgba(31, 41, 55, 0.8);
  border-color: rgba(75, 85, 99, 0.5);
  color: #9ca3af;
}

[data_theme='dark'] .btn-secondary:hover {
  background: rgba(75, 85, 99, 0.1);
}

[data_theme='dark'] .loading_state {
  color: #9ca3af;
}

[data_theme='dark'] .loading_spinner {
  border-color: rgba(156, 163, 175, 0.2);
  border-top-color: #9ca3af;
}

.token_selector {
  position: relative;
}

.token_select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(209, 213, 219, 0.5);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  transition: all 0.2s;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

.token_select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.token_symbol {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  font-weight: 600;
  font-size: 0.875rem;
  pointer-events: none;
}

.swap_arrow {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 1rem 0;
  padding: 0.5rem;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 0.5rem;
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.swap_icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #3b82f6;
  animation: pulse 2s infinite;
}

.execute_btn.swap {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.execute_btn.swap:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
}

.execute_btn.spot {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.execute_btn.spot:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

/* Dark mode styles for new elements */
[data_theme="dark"] .token_select {
  background: rgba(31, 41, 55, 0.8);
  border-color: rgba(75, 85, 99, 0.5);
  color: #f9fafb;
}

[data_theme="dark"] .token_select:focus {
  border-color: #3b82f6;
}

[data_theme="dark"] .token_symbol {
  color: #9ca3af;
}

[data_theme="dark"] .swap_arrow {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.3);
}

[data_theme="dark"] .swap_icon {
  color: #60a5fa;
}

.wallet_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
  }

.wallet_card {
  background: var(--bg-secondary);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-primary);
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  color: var(--text-primary);
}

.wallet_card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-xl);
}

[data-theme="dark"] .wallet_card {
  background: rgba(31, 41, 55, 0.9);
  border: 1px solid rgba(55, 65, 81, 0.5);
  box-shadow: var(--shadow-lg);
}

[data-theme="dark"] .wallet_card:hover {
  box-shadow: var(--shadow-2xl);
}

.wallet_header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.wallet_icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.crypto_icon {
  width: 1.5rem;
  height: 1.5rem;
}

.wallet_info {
  flex: 1;
}

.wallet_type {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 0.5rem 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.wallet_address {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
}

.wallet_actions {
  display: flex;
  gap: 0.75rem;
}

.wallet_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  box-shadow: var(--shadow-sm);
}

.wallet_btn.copy_btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.wallet_btn.copy_btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.wallet_btn.qr_btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.wallet_btn.qr_btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
}

.btn_icon {
  width: 1rem;
  height: 1rem;
}

.modal_overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal_content {
  box-shadow: var(--shadow-2xl);
  border: 1px solid var(--border-secondary);
  background: var(--bg-primary);
  color: var(--text-primary);
  padding: 2rem;
  border-radius: 1rem;
  max-width: 400px;
  width: 100%;
}

[data-theme="dark"] .modal_content {
  box-shadow: var(--shadow-2xl);
  border: 1px solid rgba(55, 65, 81, 0.2);
}

.modal_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.modal_title {
    font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.modal_close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-secondary);
  cursor: pointer;
}

.modal_form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form_group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form_label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.form_select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(209, 213, 219, 0.5);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  transition: all 0.2s;
}

.form_input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(209, 213, 219, 0.5);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  transition: all 0.2s;
}

.btn_secondary {
  padding: 0.75rem 1rem;
  border: 1px solid rgba(209, 213, 219, 0.5);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn_primary {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn_primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.loading_spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(107, 114, 128, 0.2);
  border-top: 2px solid var(--text-secondary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.modal_footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.wallet_summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.summary_card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.summary_icon {
  width: 2rem;
  height: 2rem;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.summary_content {
  flex: 1;
}

.summary_title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0;
}

.summary_value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
}

.wallet_balance_section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status_badge {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.status_badge.active {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.status_badge.inactive {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.balance_change {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.balance_change.positive {
  color: #10b981;
}

.balance_change.negative {
  color: #ef4444;
}

.wallet_icon.bitcoin {
  background: linear-gradient(135deg, #f7931a 0%, #ff9500 100%);
}

.wallet_icon.ethereum {
  background: linear-gradient(135deg, #627eea 0%, #4f6cdb 100%);
}

.wallet_icon.solana {
  background: linear-gradient(135deg, #9945ff 0%, #14f195 100%);
}

.wallet_icon.cardano {
  background: linear-gradient(135deg, #0033ad 0%, #3399ff 100%);
}

.wallet_icon.polkadot {
  background: linear-gradient(135deg, #e6007a 0%, #ff6b9d 100%);
}

.wallet_icon.chainlink {
  background: linear-gradient(135deg, #2a5ada 0%, #5a7bff 100%);
}

.wallet_icon.default {
  background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%);
}

.wallet_label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin: 0 0 0.25rem 0;
  font-style: italic;
}

.balance_info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.balance_usd {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.wallet_btn.deposit_btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.wallet_btn.deposit_btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.wallet_btn.withdraw_btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.wallet_btn.withdraw_btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.empty_state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  text-align: center;
  background: var(--bg-tertiary);
  backdrop-filter: blur(10px);
  border: 2px dashed var(--border-secondary);
  box-shadow: var(--shadow-md);
  color: var(--text-primary);
}

[data-theme="dark"] .empty_state {
  background: rgba(31, 41, 55, 0.8);
  border: 2px dashed rgba(75, 85, 99, 0.3);
  box-shadow: var(--shadow-lg);
}

.empty_icon {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.empty_icon svg {
  width: 2rem;
  height: 2rem;
}

.empty_title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.empty_description {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 0 0 1.5rem 0;
  max-width: 400px;
}

.empty_action_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.empty_action_btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px -5px rgba(59, 130, 246, 0.4);
}

.summary_value.positive {
  color: #10b981;
}

.summary_value.negative {
  color: #ef4444;
}

.balance_change.positive {
  color: #10b981;
}

.balance_change.negative {
  color: #ef4444;
}

/* Modal Styles */
.modal_overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal_content {
  box-shadow: var(--shadow-2xl);
  border: 1px solid var(--border-secondary);
  background: var(--bg-primary);
  color: var(--text-primary);
  padding: 2rem;
  border-radius: 1rem;
  max-width: 400px;
  width: 100%;
}

[data-theme="dark"] .modal_content {
  box-shadow: var(--shadow-2xl);
  border: 1px solid rgba(55, 65, 81, 0.2);
}

.modal_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.modal_title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.modal_close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-secondary);
  cursor: pointer;
}

.close_icon {
  width: 1.5rem;
  height: 1.5rem;
}

.modal_form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form_group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form_label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.form_select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(209, 213, 219, 0.5);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  transition: all 0.2s;
}

.form_input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(209, 213, 219, 0.5);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  transition: all 0.2s;
}

.btn_secondary {
  padding: 0.75rem 1rem;
  border: 1px solid rgba(209, 213, 219, 0.5);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn_primary {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn_primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.loading_spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(107, 114, 128, 0.2);
  border-top: 2px solid var(--text-secondary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.modal_footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.accordion_icon {
  width: 1rem;
  height: 1rem;
  transition: transform 0.3s ease;
}

.accordion_icon.expanded {
  transform: rotate(180deg);
}

.accordion_content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.accordion_content.expanded {
  max-height: 1000px;
}

[data-theme="dark"] {
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.4);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.6), 0 10px 10px -5px rgba(0, 0, 0, 0.5);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
  --shadow-colored: 0 10px 15px -3px rgba(59, 130, 246, 0.4), 0 4px 6px -2px rgba(59, 130, 246, 0.2);

  /* Dark mode colors - lighter version */
  --text-primary: #f3f4f6;
  --text-secondary: #d1d5db;
  --text-muted: #9ca3af;
  --bg-primary: rgba(31, 41, 55, 0.8);
  --bg-secondary: rgba(44, 62, 80, 0.9);
  --bg-tertiary: rgba(51, 65, 85, 0.8);
  --border-primary: rgba(71, 85, 105, 0.5);
  --border-secondary: rgba(71, 85, 105, 0.3);
}
</style>
