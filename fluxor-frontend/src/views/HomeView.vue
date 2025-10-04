<template>
  <div class="home_container">
    <!-- Header -->
    <div class="home_header_area">
      <div class="header_content">
        <div class="header_left">
          <h1 class="header_title">
            <span class="gradient-text">Fluxor</span>
            <span class="header_title_secondary">Trading</span>
          </h1>
          <div class="header_badge">
            <span class="badge_dot"></span>
            <span class="badge_text">Advanced Trading Platform</span>
          </div>
        </div>
        <div class="header_right">
          <router-link
            to="/login"
            class="hero_btn hero_btn_secondary"
            tabindex="0"
            aria-label="Sign In"
          >
            <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M3 3a1 1 0 011 1v12a1 1 0 11-2 0V4a1 1 0 011-1zm7.707 3.293a1 1 0 010 1.414L9.414 9H17a1 1 0 110 2H9.414l1.293 1.293a1 1 0 01-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0z"
                clip-rule="evenodd"
              />
            </svg>
            <span class="btn_text">Sign In</span>
          </router-link>
          <router-link
            to="/register"
            class="hero_btn hero_btn_primary"
            tabindex="0"
            aria-label="Get Started"
          >
            <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z"
              />
            </svg>
            <span class="btn_text">Get Started</span>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Hero Section -->
    <div class="hero_section">
      <div class="hero_background">
        <div class="hero_shapes">
          <div class="hero_shape hero_shape_1"></div>
          <div class="hero_shape hero_shape_2"></div>
          <div class="hero_shape hero_shape_3"></div>
          <div class="hero_shape hero_shape_4"></div>
          <div class="hero_shape hero_shape_5"></div>
        </div>
        <div class="hero_grid">
          <div class="grid_line grid_line_1"></div>
          <div class="grid_line grid_line_2"></div>
          <div class="grid_line grid_line_3"></div>
          <div class="grid_line grid_line_4"></div>
        </div>
        <div class="hero_particles">
          <div class="particle particle_1"></div>
          <div class="particle particle_2"></div>
          <div class="particle particle_3"></div>
        </div>
      </div>
      <div class="hero_content">
        <div class="hero_text">
          <div class="hero_badge">
            <span class="badge_icon">🚀</span>
            <span class="badge_text">Next-Gen Trading</span>
          </div>
          <h1 class="hero_title">
            <span class="hero_title_line">Advanced Bitcoin</span>
            <span class="hero_title_line gradient-text">Trading Platform</span>
          </h1>
          <p class="hero_description">
            Experience the future of cryptocurrency trading with Fluxor's advanced platform. Our
            cutting-edge technology combines real-time market data from multiple exchanges,
            AI-powered trading signals, and professional risk management tools to give you the edge
            you need in today's volatile crypto markets. Whether you're a seasoned trader or just
            starting your journey, our intuitive interface and comprehensive analytics will help you
            make informed decisions and maximize your trading potential.
          </p>
          <div class="hero_buttons">
            <router-link
              to="/register"
              class="hero_btn hero_btn_primary"
              tabindex="0"
              aria-label="Start Trading"
            >
              <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                <path
                  fill-rule="evenodd"
                  d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                  clip-rule="evenodd"
                />
              </svg>
              <span class="btn_text">Start Trading</span>
            </router-link>
            <router-link
              to="/login"
              class="hero_btn hero_btn_secondary"
              tabindex="0"
              aria-label="Sign In"
            >
              <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M3 3a1 1 0 011 1v12a1 1 0 11-2 0V4a1 1 0 011-1zm7.707 3.293a1 1 0 010 1.414L9.414 9H17a1 1 0 110 2H9.414l1.293 1.293a1 1 0 01-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0z"
                  clip-rule="evenodd"
                />
              </svg>
              <span class="btn_text">Sign In</span>
            </router-link>
          </div>
          <div class="hero_stats">
            <div class="stat_item">
              <div class="stat_number">$2.5B+</div>
              <div class="stat_label">Trading Volume</div>
            </div>
            <div class="stat_item">
              <div class="stat_number">50K+</div>
              <div class="stat_label">Active Traders</div>
            </div>
            <div class="stat_item">
              <div class="stat_number">99.9%</div>
              <div class="stat_label">Uptime</div>
            </div>
          </div>
        </div>
        <div class="hero_visual">
          <div class="trading_card card-premium">
            <div class="card_header">
              <div class="card_title">BTC/USD</div>
              <div class="card_price price-up">$43,250.50</div>
            </div>
            <div class="card_chart">
              <div class="chart_line"></div>
              <div class="chart_dots">
                <div class="chart_dot chart_dot_1"></div>
                <div class="chart_dot chart_dot_2"></div>
                <div class="chart_dot chart_dot_3"></div>
                <div class="chart_dot chart_dot_4"></div>
                <div class="chart_dot chart_dot_5"></div>
              </div>
            </div>
            <div class="card_stats">
              <div class="stat">
                <span class="stat_label">24h Change</span>
                <span class="stat_value price-up">+2.45%</span>
              </div>
              <div class="stat">
                <span class="stat_label">Volume</span>
                <span class="stat_value">$1.2B</span>
              </div>
            </div>
            <div class="card_actions">
              <button class="btn-success text-sm">Buy</button>
              <button class="btn-danger text-sm">Sell</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Market Overview Section -->
    <div class="market_overview_section">
      <div class="section_container">
        <div class="section_header">
          <div class="section_badge">
            <span class="badge_icon">📊</span>
            <span class="badge_text">Live Markets</span>
          </div>
          <h2 class="section_title">Market Overview</h2>
          <p class="section_subtitle">
            Stay ahead of the market with comprehensive real-time data from major exchanges. Our
            advanced price aggregation system ensures you get the most accurate and up-to-date
            information across all major cryptocurrency pairs, helping you make informed trading
            decisions with confidence.
          </p>
          <div class="market_insights">
            <div class="insight_card">
              <div class="insight_icon">📈</div>
              <div class="insight_content">
                <h4 class="insight_title">Real-Time Data</h4>
                <p class="insight_text">Millisecond-level price updates from 15+ major exchanges</p>
              </div>
            </div>
            <div class="insight_card">
              <div class="insight_icon">🔍</div>
              <div class="insight_content">
                <h4 class="insight_title">Advanced Analytics</h4>
                <p class="insight_text">Comprehensive market depth and order book analysis</p>
              </div>
            </div>
            <div class="insight_card">
              <div class="insight_icon">⚡</div>
              <div class="insight_content">
                <h4 class="insight_title">Instant Execution</h4>
                <p class="insight_text">Sub-second trade execution with advanced order types</p>
              </div>
            </div>
          </div>
        </div>
        <div class="section_header">
          <div class="section_badge">
            <span class="badge_icon">📊</span>
            <span class="badge_text">Live Markets</span>
          </div>
          <h2 class="section_title">Market Overview</h2>
          <p class="section_subtitle">
            Stay ahead of the market with comprehensive real-time data from major exchanges. Our
            advanced price aggregation system ensures you get the most accurate and up-to-date
            information across all major cryptocurrency pairs, helping you make informed trading
            decisions with confidence.
          </p>
        </div>

        <div class="market_grid">
          <router-link
            :to="pair.link"
            class="market_card"
            v-for="pair in marketPairs"
            :key="pair.symbol"
          >
            <div class="market_card_header">
              <div class="market_info">
                <div class="market_symbol">{{ pair.symbol }}</div>
                <div class="market_name">{{ pair.name }}</div>
              </div>
              <div class="market_price" :class="pair.change >= 0 ? 'price-up' : 'price-down'">
                ${{ pair.price.toLocaleString() }}
              </div>
            </div>
            <div class="market_card_body">
              <div class="market_stats">
                <div class="market_stat">
                  <span class="stat_label">24h Change</span>
                  <span
                    class="stat_value"
                    :class="pair.change >= 0 ? 'text-green-500' : 'text-red-500'"
                  >
                    {{ pair.change >= 0 ? '+' : '' }}{{ pair.change.toFixed(2) }}%
                  </span>
                </div>
                <div class="market_stat">
                  <span class="stat_label">Volume</span>
                  <span class="stat_value">${{ pair.volume }}</span>
                </div>
                <div class="market_stat">
                  <span class="stat_label">Market Cap</span>
                  <span class="stat_value">${{ pair.marketCap }}</span>
                </div>
              </div>
              <div class="market_chart_mini">
                <div class="mini_chart" :class="pair.change >= 0 ? 'chart-up' : 'chart-down'">
                  <svg viewBox="0 0 100 30" class="chart_svg">
                    <path
                      :d="pair.chartPath"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1.5"
                    />
                  </svg>
                </div>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Trading Signals Section -->
    <div class="signals_section">
      <div class="section_container">
        <div class="section_header">
          <div class="section_badge">
            <span class="badge_icon">🎯</span>
            <span class="badge_text">AI Signals</span>
          </div>
          <h2 class="section_title">Trading Signals</h2>
          <p class="section_subtitle">
            Leverage the power of artificial intelligence to enhance your trading strategy. Our
            advanced algorithms analyze market patterns, technical indicators, and market sentiment
            to provide you with actionable trading signals. Each recommendation comes with detailed
            analysis, confidence levels, and risk management parameters to help you execute trades
            with precision and confidence.
          </p>
        </div>

        <div class="signals_grid">
          <div class="signal_card" v-for="signal in tradingSignals" :key="signal.id">
            <div class="signal_header">
              <div class="signal_pair">{{ signal.pair }}</div>
              <div class="signal_type" :class="signal.type">
                <span class="signal_icon">{{
                  signal.type === 'buy' ? '📈' : signal.type === 'sell' ? '📉' : '⏸️'
                }}</span>
                <span class="signal_text">{{ signal.type.toUpperCase() }}</span>
              </div>
            </div>
            <div class="signal_body">
              <div class="signal_strength">
                <span class="strength_label">Confidence</span>
                <div class="strength_bar">
                  <div class="strength_fill" :style="{ width: signal.confidence + '%' }"></div>
                </div>
                <span class="strength_value">{{ signal.confidence }}%</span>
              </div>
              <div class="signal_details">
                <div class="signal_detail">
                  <span class="detail_label">Target Price</span>
                  <span class="detail_value">${{ signal.targetPrice }}</span>
                </div>
                <div class="signal_detail">
                  <span class="detail_label">Stop Loss</span>
                  <span class="detail_value">${{ signal.stopLoss }}</span>
                </div>
                <div class="signal_detail">
                  <span class="detail_label">Timeframe</span>
                  <span class="detail_value">{{ signal.timeframe }}</span>
                </div>
              </div>
              <div class="signal_reason">
                <span class="reason_label">Reason</span>
                <p class="reason_text">{{ signal.reason }}</p>
              </div>
            </div>
            <div class="signal_actions">
              <router-link to="/dashboard" class="btn-primary text-sm">Follow Signal</router-link>
              <router-link to="/analytics" class="btn-secondary text-sm">View Analysis</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Market Statistics Section -->
    <div class="stats_section">
      <div class="section_container">
        <div class="section_header">
          <div class="section_badge">
            <span class="badge_icon">📈</span>
            <span class="badge_text">Market Data</span>
          </div>
          <h2 class="section_title">Market Statistics</h2>
          <p class="section_subtitle">
            Get a complete picture of the cryptocurrency market with our comprehensive analytics
            dashboard. From total market capitalization and trading volume to network metrics and
            sentiment indicators, we provide all the essential data you need to understand market
            trends and make strategic investment decisions.
          </p>
        </div>

        <div class="stats_grid">
          <router-link to="/analytics" class="stat_card">
            <div class="stat_card_header">
              <div class="stat_icon">💰</div>
              <div class="stat_title">Total Market Cap</div>
            </div>
            <div class="stat_value">$2.1T</div>
            <div class="stat_change positive">+3.2% (24h)</div>
          </router-link>

          <router-link to="/analytics" class="stat_card">
            <div class="stat_card_header">
              <div class="stat_icon">📊</div>
              <div class="stat_title">24h Volume</div>
            </div>
            <div class="stat_value">$89.5B</div>
            <div class="stat_change positive">+12.8% (24h)</div>
          </router-link>

          <router-link to="/analytics" class="stat_card">
            <div class="stat_card_header">
              <div class="stat_icon">🎯</div>
              <div class="stat_title">BTC Dominance</div>
            </div>
            <div class="stat_value">52.3%</div>
            <div class="stat_change negative">-0.8% (24h)</div>
          </router-link>

          <router-link to="/analytics" class="stat_card">
            <div class="stat_card_header">
              <div class="stat_icon">🔥</div>
              <div class="stat_title">Fear & Greed Index</div>
            </div>
            <div class="stat_value">72</div>
            <div class="stat_label">Greed</div>
          </router-link>

          <router-link to="/analytics" class="stat_card">
            <div class="stat_card_header">
              <div class="stat_icon">⚡</div>
              <div class="stat_title">Active Addresses</div>
            </div>
            <div class="stat_value">1.2M</div>
            <div class="stat_change positive">+5.4% (24h)</div>
          </router-link>

          <router-link to="/analytics" class="stat_card">
            <div class="stat_card_header">
              <div class="stat_icon">🔗</div>
              <div class="stat_title">Network Hash Rate</div>
            </div>
            <div class="stat_value">450 EH/s</div>
            <div class="stat_change positive">+2.1% (24h)</div>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Recent Trades Section -->
    <div class="trades_section">
      <div class="section_container">
        <div class="section_header">
          <div class="section_badge">
            <span class="badge_icon">🔄</span>
            <span class="badge_text">Live Trades</span>
          </div>
          <h2 class="section_title">Recent Trades</h2>
          <p class="section_subtitle">
            Monitor real-time trading activity across the platform to stay informed about market
            movements and community sentiment. Our live trade feed provides transparency and helps
            you understand market dynamics by showing actual trading patterns, volumes, and user
            behavior in real-time.
          </p>
        </div>

        <div class="trades_feed">
          <div class="trade_item" v-for="trade in recentTrades" :key="trade.id">
            <div class="trade_info">
              <div class="trade_pair">{{ trade.pair }}</div>
              <div class="trade_type" :class="trade.type">
                {{ trade.type.toUpperCase() }}
              </div>
            </div>
            <div class="trade_details">
              <div class="trade_amount">{{ trade.amount }} {{ trade.pair.split('/')[0] }}</div>
              <div class="trade_price">${{ trade.price }}</div>
              <div class="trade_time">{{ trade.time }}</div>
            </div>
            <div class="trade_user">
              <div class="user_avatar">{{ trade.user.charAt(0).toUpperCase() }}</div>
              <div class="user_name">{{ trade.user }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Performance Section -->
    <div class="performance_section">
      <div class="section_container">
        <div class="section_header">
          <div class="section_badge">
            <span class="badge_icon">📊</span>
            <span class="badge_text">Performance</span>
          </div>
          <h2 class="section_title">Platform Performance</h2>
          <p class="section_subtitle">
            Track your trading performance and platform metrics with our comprehensive analytics
            suite. From win rates and profit analysis to execution speed and signal accuracy, our
            performance dashboard provides detailed insights to help you optimize your trading
            strategy and improve your results over time.
          </p>
        </div>

        <div class="performance_grid">
          <div class="performance_card">
            <div class="performance_header">
              <h3 class="performance_title">BTC/USD Price Chart</h3>
              <div class="performance_controls">
                <button class="time_btn active">1H</button>
                <button class="time_btn">4H</button>
                <button class="time_btn">1D</button>
                <button class="time_btn">1W</button>
              </div>
            </div>
            <div class="chart_section">
              <ApexCandlestickChart title="BTC/USD - Performance Chart" :height="350" />
            </div>
          </div>

          <div class="performance_metrics">
            <router-link to="/analytics" class="metric_card">
              <div class="metric_header">
                <div class="metric_icon">📈</div>
                <div class="metric_title">Win Rate</div>
              </div>
              <div class="metric_value">68.5%</div>
              <div class="metric_change positive">+2.3% this week</div>
            </router-link>

            <router-link to="/analytics" class="metric_card">
              <div class="metric_header">
                <div class="metric_icon">💰</div>
                <div class="metric_title">Avg. Profit</div>
              </div>
              <div class="metric_value">$1,247</div>
              <div class="metric_change positive">+15.2% this month</div>
            </router-link>

            <router-link to="/analytics" class="metric_card">
              <div class="metric_header">
                <div class="metric_icon">⚡</div>
                <div class="metric_title">Execution Speed</div>
              </div>
              <div class="metric_value">0.023s</div>
              <div class="metric_change positive">-12% improvement</div>
            </router-link>

            <router-link to="/analytics" class="metric_card">
              <div class="metric_header">
                <div class="metric_icon">🎯</div>
                <div class="metric_title">Signal Accuracy</div>
              </div>
              <div class="metric_value">76.8%</div>
              <div class="metric_change positive">+4.1% this month</div>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- News & Updates Section -->
    <div class="news_section">
      <div class="section_container">
        <div class="section_header">
          <div class="section_badge">
            <span class="badge_icon">📰</span>
            <span class="badge_text">Market News</span>
          </div>
          <h2 class="section_title">Latest News & Updates</h2>
          <p class="section_subtitle">
            Stay ahead of market developments with our curated news feed featuring the latest
            cryptocurrency news, regulatory updates, and platform enhancements. Our team of analysts
            carefully selects and summarizes the most relevant information to help you make informed
            decisions and stay updated on industry trends.
          </p>
        </div>

        <div class="news_grid">
          <router-link :to="news.link" class="news_card" v-for="news in marketNews" :key="news.id">
            <div class="news_image">
              <div class="news_category">{{ news.category }}</div>
            </div>
            <div class="news_content">
              <h3 class="news_title">{{ news.title }}</h3>
              <p class="news_excerpt">{{ news.excerpt }}</p>
              <div class="news_meta">
                <span class="news_time">{{ news.time }}</span>
                <span class="news_source">{{ news.source }}</span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="features_section">
      <div class="features_container">
        <div class="features_header">
          <div class="features_badge">
            <span class="badge_icon">⚡</span>
            <span class="badge_text">Features</span>
          </div>
          <h2 class="features_title">Everything you need to trade Bitcoin</h2>
          <p class="features_subtitle">
            Discover a comprehensive suite of professional-grade trading tools designed to give you
            the competitive edge. From real-time market data and advanced charting capabilities to
            AI-powered signals and robust risk management, every feature is crafted to enhance your
            trading experience and maximize your potential for success.
          </p>
        </div>

        <div class="features_grid">
          <div class="feature_card">
            <div class="feature_icon_wrapper">
              <div class="feature_icon">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <div class="feature_icon_glow"></div>
            </div>
            <div class="feature_content">
              <h3 class="feature_title">Real-time Price Feeds</h3>
              <p class="feature_description">
                Access real-time price data from major exchanges including Binance, Coinbase, and
                Kraken through our high-performance WebSocket connections. Our advanced aggregation
                system ensures millisecond-level accuracy and 99.9% uptime, giving you the most
                reliable market data for informed trading decisions.
              </p>
              <div class="feature_badge">
                <span class="badge_dot"></span>
                Live Data
              </div>
            </div>
          </div>

          <div class="feature_card">
            <div class="feature_icon_wrapper">
              <div class="feature_icon">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                  />
                </svg>
              </div>
              <div class="feature_icon_glow"></div>
            </div>
            <div class="feature_content">
              <h3 class="feature_title">Advanced Trading Algorithms</h3>
              <p class="feature_description">
                Leverage our sophisticated AI algorithms that analyze over 50 technical indicators
                including RSI, MACD, Bollinger Bands, and custom proprietary signals. Our machine
                learning models continuously adapt to market conditions, providing you with highly
                accurate buy/sell signals and trend predictions.
              </p>
              <div class="feature_badge">
                <span class="badge_dot"></span>
                AI-Powered
              </div>
            </div>
          </div>

          <div class="feature_card">
            <div class="feature_icon_wrapper">
              <div class="feature_icon">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                  />
                </svg>
              </div>
              <div class="feature_icon_glow"></div>
            </div>
            <div class="feature_content">
              <h3 class="feature_title">Risk Management</h3>
              <p class="feature_description">
                Protect your capital with our comprehensive risk management system featuring
                automatic stop-loss orders, position sizing recommendations, portfolio
                diversification analysis, and real-time risk alerts. Our advanced algorithms help
                you maintain optimal risk-reward ratios and prevent significant losses.
              </p>
              <div class="feature_badge">
                <span class="badge_dot"></span>
                Protected
              </div>
            </div>
          </div>

          <div class="feature_card">
            <div class="feature_icon_wrapper">
              <div class="feature_icon">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div class="feature_icon_glow"></div>
            </div>
            <div class="feature_content">
              <h3 class="feature_title">Compliance & Security</h3>
              <p class="feature_description">
                Trade with confidence knowing your assets are protected by enterprise-grade security
                measures including multi-signature wallets, cold storage solutions, and
                comprehensive audit trails. Our platform maintains full regulatory compliance with
                KYC/AML requirements and undergoes regular security audits.
              </p>
              <div class="feature_badge">
                <span class="badge_dot"></span>
                Secure
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="cta_section">
      <div class="cta_background">
        <div class="cta_shapes">
          <div class="cta_shape cta_shape_1"></div>
          <div class="cta_shape cta_shape_2"></div>
        </div>
      </div>
      <div class="cta_content">
        <h2 class="cta_title">
          <span class="cta_title_line">Ready to start trading?</span>
          <span class="cta_title_line">Join thousands of traders today.</span>
        </h2>
        <p class="cta_description">
          Join thousands of successful traders who have already discovered the power of Fluxor's
          advanced trading platform. Start your journey today with our comprehensive suite of tools,
          real-time market data, and AI-powered insights designed to help you achieve your trading
          goals.
        </p>
        <router-link
          to="/register"
          class="hero_btn hero_btn_primary"
          tabindex="0"
          aria-label="Get started"
        >
          <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
            <path
              d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z"
            />
          </svg>
          <span class="btn_text">Get started</span>
        </router-link>
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer_container">
        <div class="footer_main">
          <div class="footer_brand">
            <h3 class="footer_title"><span class="gradient-text">Fluxor</span> Trading</h3>
            <p class="footer_description">
              Fluxor Trading is the premier cryptocurrency trading platform that combines
              cutting-edge technology with user-friendly design. Our mission is to democratize
              access to advanced trading tools, providing both novice and experienced traders with
              the resources they need to succeed in the dynamic world of cryptocurrency markets.
            </p>
            <div class="footer_social">
              <a href="#" class="social_link">
                <svg fill="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"
                  />
                </svg>
              </a>
              <a href="#" class="social_link">
                <svg fill="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"
                  />
                </svg>
              </a>
              <a href="#" class="social_link">
                <svg fill="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"
                  />
                </svg>
              </a>
            </div>
          </div>
          <div class="footer_links">
            <div class="footer_column">
              <h4 class="footer_column_title">Trading</h4>
              <router-link to="/dashboard" class="footer_link">Spot Trading</router-link>
              <router-link to="/dashboard" class="footer_link">Futures Trading</router-link>
              <router-link to="/dashboard" class="footer_link">Margin Trading</router-link>
              <router-link to="/dashboard" class="footer_link">API Trading</router-link>
            </div>
            <div class="footer_column">
              <h4 class="footer_column_title">Platform</h4>
              <router-link to="/" class="footer_link">Features</router-link>
              <router-link to="/" class="footer_link">Security</router-link>
              <router-link to="/" class="footer_link">API Documentation</router-link>
              <router-link to="/" class="footer_link">Status</router-link>
            </div>
            <div class="footer_column">
              <h4 class="footer_column_title">Support</h4>
              <router-link to="/" class="footer_link">Help Center</router-link>
              <router-link to="/" class="footer_link">Contact Us</router-link>
              <router-link to="/" class="footer_link">Community</router-link>
              <router-link to="/" class="footer_link">Blog</router-link>
            </div>
            <div class="footer_column">
              <h4 class="footer_column_title">Legal</h4>
              <router-link to="/" class="footer_link">Terms of Service</router-link>
              <router-link to="/" class="footer_link">Privacy Policy</router-link>
              <router-link to="/" class="footer_link">Cookie Policy</router-link>
              <router-link to="/" class="footer_link">Risk Disclosure</router-link>
            </div>
          </div>
        </div>
        <div class="footer_bottom">
          <p class="footer_copyright">© 2024 Fluxor Trading. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ApexCandlestickChart from '@/components/ApexCandlestickChart.vue'
const marketPairs = ref([
  {
    symbol: 'BTC/USD',
    name: 'Bitcoin',
    price: 43250.5,
    change: 2.45,
    volume: '1.2B',
    marketCap: '850.2B',
    chartPath: 'M0,15 L20,10 L40,12 L60,8 L80,5 L100,3',
    link: '/dashboard',
  },
  {
    symbol: 'ETH/USD',
    name: 'Ethereum',
    price: 2650.75,
    change: -1.23,
    volume: '890.5M',
    marketCap: '318.7B',
    chartPath: 'M0,20 L20,18 L40,15 L60,12 L80,10 L100,8',
    link: '/dashboard',
  },
  {
    symbol: 'ADA/USD',
    name: 'Cardano',
    price: 0.485,
    change: 5.67,
    volume: '245.3M',
    marketCap: '17.2B',
    chartPath: 'M0,25 L20,20 L40,18 L60,15 L80,12 L100,10',
    link: '/dashboard',
  },
  {
    symbol: 'SOL/USD',
    name: 'Solana',
    price: 98.45,
    change: 3.89,
    volume: '567.8M',
    marketCap: '42.1B',
    chartPath: 'M0,18 L20,15 L40,12 L60,10 L80,8 L100,5',
    link: '/dashboard',
  },
  {
    symbol: 'DOT/USD',
    name: 'Polkadot',
    price: 7.23,
    change: -0.95,
    volume: '123.4M',
    marketCap: '9.1B',
    chartPath: 'M0,22 L20,20 L40,18 L60,16 L80,14 L100,12',
    link: '/dashboard',
  },
  {
    symbol: 'LINK/USD',
    name: 'Chainlink',
    price: 15.67,
    change: 4.12,
    volume: '189.2M',
    marketCap: '8.9B',
    chartPath: 'M0,20 L20,18 L40,15 L60,12 L80,10 L100,8',
    link: '/dashboard',
  },
])

// Trading signals data with enhanced analysis
const tradingSignals = ref([
  {
    id: 1,
    pair: 'BTC/USD',
    type: 'buy',
    confidence: 85,
    targetPrice: '44,500',
    stopLoss: '42,800',
    timeframe: '4H',
    reason:
      'Strong bullish momentum detected with RSI showing oversold conditions at 28.5 and MACD crossover signaling upward trend. Volume has increased 45% above average, and the price has broken through key resistance at $42,800. Fibonacci retracement levels suggest potential target at $44,500.',
  },
  {
    id: 2,
    pair: 'ETH/USD',
    type: 'sell',
    confidence: 72,
    targetPrice: '2,580',
    stopLoss: '2,720',
    timeframe: '1H',
    reason:
      'Price has reached major resistance level at $2,720 with bearish divergence forming on RSI. Volume has declined 23% over the past 4 hours, indicating weakening buying pressure. Stochastic oscillator shows overbought conditions, and the 50-day moving average is acting as resistance.',
  },
  {
    id: 3,
    pair: 'ADA/USD',
    type: 'hold',
    confidence: 65,
    targetPrice: '0.52',
    stopLoss: '0.46',
    timeframe: '1D',
    reason:
      'Cardano is currently in a consolidation phase between $0.46 and $0.52 support/resistance levels. Mixed signals from technical indicators - RSI is neutral at 52, while MACD shows slight bearish momentum. Volume is below average, suggesting accumulation phase. Waiting for clear breakout above $0.52 or breakdown below $0.46.',
  },
  {
    id: 4,
    pair: 'SOL/USD',
    type: 'buy',
    confidence: 78,
    targetPrice: '105.00',
    stopLoss: '94.50',
    timeframe: '2H',
    reason:
      'Solana has broken out from an ascending triangle pattern that has been forming over the past 2 weeks. Volume has increased 67% on the breakout, confirming strong buying interest. RSI is at 68, showing healthy momentum without being overbought. The breakout target based on pattern measurement suggests $105.00.',
  },
])

// Recent trades data
const recentTrades = ref([
  {
    id: 1,
    pair: 'BTC/USD',
    type: 'buy',
    amount: '0.5',
    price: '43,250',
    time: '2 min ago',
    user: 'Trader_John',
  },
  {
    id: 2,
    pair: 'ETH/USD',
    type: 'sell',
    amount: '2.1',
    price: '2,650',
    time: '5 min ago',
    user: 'Crypto_Queen',
  },
  {
    id: 3,
    pair: 'SOL/USD',
    type: 'buy',
    amount: '15.0',
    price: '98.45',
    time: '8 min ago',
    user: 'Solana_Fan',
  },
  {
    id: 4,
    pair: 'ADA/USD',
    type: 'sell',
    amount: '5000',
    price: '0.485',
    time: '12 min ago',
    user: 'ADA_Holder',
  },
  {
    id: 5,
    pair: 'BTC/USD',
    type: 'buy',
    amount: '0.25',
    price: '43,245',
    time: '15 min ago',
    user: 'Bitcoin_Bull',
  },
])

// Market news data with enhanced content
const marketNews = ref([
  {
    id: 1,
    category: 'Bitcoin',
    title: 'Bitcoin Surges Past $43,000 as Institutional Adoption Grows',
    excerpt:
      'Major financial institutions including BlackRock, Fidelity, and Goldman Sachs continue to show unprecedented interest in Bitcoin as a store of value and inflation hedge. Recent filings show institutional Bitcoin holdings have increased by 34% this quarter, with over $15 billion in new investments.',
    time: '2 hours ago',
    source: 'CryptoNews',
    link: '/analytics',
  },
  {
    id: 2,
    category: 'Regulation',
    title: 'New Crypto Regulations Expected to Boost Market Confidence',
    excerpt:
      'The SEC and other global regulators are expected to announce new comprehensive cryptocurrency regulations within the next quarter. Industry experts predict these regulations will provide much-needed clarity and attract an additional $50 billion in institutional investments to the crypto space.',
    time: '4 hours ago',
    source: 'CoinDesk',
    link: '/analytics',
  },
  {
    id: 3,
    category: 'Technology',
    title: 'Ethereum Layer 2 Solutions Show Promising Growth',
    excerpt:
      'Ethereum Layer 2 solutions including Polygon, Arbitrum, and Optimism are experiencing unprecedented growth with total value locked (TVL) reaching $12 billion. These solutions have reduced gas fees by up to 90% and improved transaction speeds significantly, driving increased adoption.',
    time: '6 hours ago',
    source: 'Decrypt',
    link: '/analytics',
  },
  {
    id: 4,
    category: 'Market Analysis',
    title: 'Altcoin Season Indicators Suggest Potential Rally',
    excerpt:
      'Technical analysis from leading crypto analysts indicates that altcoins may be entering a new bullish phase relative to Bitcoin. The Bitcoin dominance index has declined from 54% to 52.3%, while altcoin market capitalization has increased by 8.5% over the past week.',
    time: '8 hours ago',
    source: 'TradingView',
    link: '/analytics',
  },
])

// Auto-refresh data every 30 seconds
onMounted(() => {
  setInterval(() => {
    // Simulate real-time updates
    marketPairs.value.forEach((pair) => {
      pair.price += (Math.random() - 0.5) * 100
      pair.change += (Math.random() - 0.5) * 2
    })
  }, 30000)
})
</script>

<style scoped>
.home_container {
  min-height: 100vh;
  overflow-x: hidden;
}

/* Header Styles */
.home_header_area {
  width: 100%;
  padding: 2.5rem 0 1.5rem 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
}
.header_content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 2rem;
}
.header_left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.75rem;
}
.header_title {
  font-size: 2.2rem;
  font-weight: 900;
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin: 0;
  letter-spacing: -0.02em;
}
.gradient-text {
  color: var(--color_primary);
  background: none;
  -webkit-background-clip: initial;
  -webkit-text-fill-color: initial;
  font-weight: 900;
}
.header_title_secondary {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color_secondary);
  opacity: 0.85;
  margin-left: 0.2rem;
}
.header_badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 1.1rem;
  background: var(--color_surface);
  border: 1.5px solid var(--color_primary);
  border-radius: 9999px;
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--color_primary);
  box-shadow: 0 2px 8px rgba(0, 234, 255, 0.08);
  letter-spacing: 0.03em;
  text-shadow: none;
}
.badge_dot {
  width: 7px;
  height: 7px;
  background: var(--color_primary);
  border-radius: 50%;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
.badge_text {
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.header_right {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn_icon {
  width: 1rem;
  height: 1rem;
  margin-right: 0.5rem;
}

/* Hero Section */
.hero_section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  overflow: hidden;
}

.hero_background {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  overflow: hidden;
}

.hero_shapes {
  position: absolute;
  inset: 0;
}

.hero_shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.hero_shape_1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.hero_shape_2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.hero_shape_3 {
  width: 100px;
  height: 100px;
  top: 30%;
  right: 30%;
  animation-delay: 4s;
}

.hero_shape_4 {
  width: 80px;
  height: 80px;
  bottom: 20%;
  left: 20%;
  animation-delay: 1s;
}

.hero_shape_5 {
  width: 60px;
  height: 60px;
  top: 80%;
  right: 5%;
  animation-delay: 3s;
}

.hero_grid {
  position: absolute;
  inset: 0;
  opacity: 0.1;
}

.hero_particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.hero_particles .particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: linear-gradient(135deg, #ffffff, #f093fb);
  border-radius: 50%;
  animation: particleFloat 12s linear infinite;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.hero_particles .particle_1 {
  top: 20%;
  left: 20%;
  animation-delay: 0s;
}

.hero_particles .particle_2 {
  top: 60%;
  right: 30%;
  animation-delay: 4s;
}

.hero_particles .particle_3 {
  bottom: 30%;
  left: 40%;
  animation-delay: 8s;
}

.grid_line {
  position: absolute;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
}

.grid_line_1 {
  top: 25%;
  left: 0;
  right: 0;
  height: 1px;
}

.grid_line_2 {
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
}

.grid_line_3 {
  top: 75%;
  left: 0;
  right: 0;
  height: 1px;
}

.grid_line_4 {
  top: 0;
  bottom: 0;
  left: 50%;
  width: 1px;
  transform: translateX(-50%);
}

.hero_content {
  position: relative;
  z-index: 10;
  max-width: 1200px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.hero_text {
  color: white;
}

.hero_badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 2rem;
}

.badge_icon {
  font-size: 1rem;
}

.hero_title {
  font-size: 3.5rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.hero_title_line {
  display: block;
}

.hero_description {
  font-size: 1.25rem;
  line-height: 1.6;
  margin-bottom: 2.5rem;
  opacity: 0.9;
}

.hero_buttons {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 3rem;
  flex-wrap: wrap;
}

.hero_btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.1rem 2.5rem;
  font-size: 1.15rem;
  font-weight: 700;
  border-radius: 1.25rem;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.18);
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
  border: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  text-decoration: none;
  min-width: 180px;
  justify-content: center;
}
.hero_btn_primary {
  background: var(--color_primary);
  color: var(--color_text_on_primary);
  border: none;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.13);
  transition:
    box-shadow 0.18s,
    transform 0.18s;
}
.hero_btn_primary:hover,
.hero_btn_primary:focus {
  background: var(--color_primary);
  color: var(--color_text_on_primary);
  box-shadow: 0 12px 32px rgba(37, 99, 235, 0.18);
  transform: translateY(-2px) scale(1.03);
}
.hero_btn_secondary {
  background: var(--color_surface);
  color: var(--color_primary);
  border: 2px solid var(--color_primary);
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.08);
  transition:
    box-shadow 0.18s,
    transform 0.18s;
}
.hero_btn_secondary:hover,
.hero_btn_secondary:focus {
  background: var(--color_surface);
  color: var(--color_primary);
  border-color: var(--color_primary);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.13);
  transform: translateY(-2px) scale(1.03);
}

.btn_icon {
  width: 1.35rem;
  height: 1.35rem;
  transition: transform 0.2s;
}
.hero_btn:hover .btn_icon,
.hero_btn:focus .btn_icon {
  transform: scale(1.15) translateX(2px);
}

.btn_text {
  display: inline-block;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.hero_btn:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.hero_stats {
  display: flex;
  gap: 2.5rem;
  margin-top: 2.5rem;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.stat_item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 120px;
  margin-right: 1.5rem;
}

.stat_number {
  font-size: 2.1rem;
  font-weight: 900;
  color: var(--color_primary);
  background: none;
  -webkit-background-clip: initial;
  -webkit-text-fill-color: initial;
  text-shadow:
    0 4px 18px rgba(0, 234, 255, 0.13),
    0 2px 8px rgba(163, 230, 53, 0.1),
    0 1px 2px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.01em;
  margin-bottom: 0.25rem;
  line-height: 1.1;
}

.stat_label {
  font-size: 1rem;
  color: var(--color_primary);
  font-weight: 600;
  letter-spacing: 0.01em;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Trading Card */
.hero_visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.trading_card {
  background: var(--color_surface);
  color: var(--color_text_on_surface);
  border: 1.5px solid var(--color_border);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.07);
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  transform: perspective(1000px) rotateY(-5deg) rotateX(5deg);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.trading_card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(147, 51, 234, 0.05));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.trading_card:hover {
  transform: perspective(1000px) rotateY(0deg) rotateX(0deg) translateY(-10px);
  box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.3);
}

.trading_card:hover::before {
  opacity: 1;
}

.card_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color_border);
}

.card_title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
}

.card_price {
  font-size: 1.5rem;
  font-weight: 800;
}

.card_chart {
  position: relative;
  height: 120px;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
  border-radius: 12px;
  overflow: hidden;
}

.chart_line {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  transform: translateY(-50%);
}

.chart_dots {
  position: absolute;
  inset: 0;
}

.chart_dot {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #3b82f6;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart_dot_1 {
  top: 20%;
  left: 10%;
}
.chart_dot_2 {
  top: 40%;
  left: 25%;
}
.chart_dot_3 {
  top: 60%;
  left: 50%;
}
.chart_dot_4 {
  top: 30%;
  left: 75%;
}
.chart_dot_5 {
  top: 10%;
  left: 90%;
}

.card_stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.stat {
  text-align: center;
}

.stat_label {
  display: block;
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.stat_value {
  font-size: 1rem;
  font-weight: 700;
}

.card_actions {
  display: flex;
  gap: 0.5rem;
}

.card_actions button {
  flex: 1;
  padding: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
}

/* Features Section */
.features_section {
  padding: 8rem 2rem;
  background: var(--color_surface);
  color: var(--color_text);
  position: relative;
  overflow: hidden;
}

.features_section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color_border), transparent);
}

.features_container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.features_header {
  text-align: center;
  margin-bottom: 5rem;
}

.features_badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 16px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color_primary);
  margin-bottom: 1.5rem;
  backdrop-filter: blur(10px);
}

.features_title {
  font-size: 3.5rem;
  font-weight: 800;
  color: var(--color_text);
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.features_subtitle {
  font-size: 1.25rem;
  color: var(--color_text_secondary);
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

.features_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2.5rem;
  padding: 1rem 0;
}

.feature_card {
  position: relative;
  background: var(--color_surface);
  color: var(--color_text);
  border: 1.5px solid var(--color_border);
  border-radius: 24px;
  padding: 2.5rem 2rem;
  text-align: left;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.feature_card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color_primary), var(--color_secondary));
  transform: scaleX(0);
  transition: transform 0.4s ease;
}

.feature_card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.12);
  border-color: var(--color_primary);
}

.feature_card:hover::before {
  transform: scaleX(1);
}

.feature_icon_wrapper {
  position: relative;
  width: 72px;
  height: 72px;
  margin-bottom: 2rem;
}

.feature_icon {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--color_primary), var(--color_secondary));
  color: var(--color_text_on_primary);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  transition: all 0.3s ease;
}

.feature_icon_glow {
  position: absolute;
  inset: -8px;
  background: linear-gradient(135deg, var(--color_primary), var(--color_secondary));
  border-radius: 28px;
  opacity: 0.3;
  filter: blur(12px);
  transition: all 0.3s ease;
  z-index: 1;
}

.feature_card:hover .feature_icon {
  transform: scale(1.1) rotate(5deg);
}

.feature_card:hover .feature_icon_glow {
  opacity: 0.6;
  filter: blur(16px);
  transform: scale(1.2);
}

.feature_content {
  position: relative;
  z-index: 2;
}

.feature_title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color_primary);
  margin-bottom: 1rem;
  line-height: 1.3;
}

.feature_description {
  color: var(--color_text_secondary);
  line-height: 1.7;
  margin-bottom: 1.5rem;
  font-size: 1rem;
}

.feature_badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--color_surface_alt);
  color: var(--color_primary);
  border: 1px solid var(--color_border);
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.feature_card:hover .feature_badge {
  background: var(--color_primary);
  color: var(--color_text_on_primary);
  border-color: var(--color_primary);
  transform: translateY(-2px);
}

.badge_dot {
  width: 6px;
  height: 6px;
  background: currentColor;
  border-radius: 50%;
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

/* CTA Section */
.cta_section {
  position: relative;
  padding: 6rem 2rem;
  background: var(--color_surface_alt);
  color: var(--color_text_on_surface);
  overflow: hidden;
}

.cta_background {
  position: absolute;
  inset: 0;
}

.cta_shapes {
  position: absolute;
  inset: 0;
}

.cta_shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 8s ease-in-out infinite;
}

.cta_shape_1 {
  width: 300px;
  height: 300px;
  top: -150px;
  right: -150px;
  animation-delay: 0s;
}

.cta_shape_2 {
  width: 200px;
  height: 200px;
  bottom: -100px;
  left: -100px;
  animation-delay: 4s;
}

.cta_content {
  position: relative;
  z-index: 10;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.cta_title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
}

.cta_title_line {
  display: block;
}

.cta_description {
  font-size: 1.25rem;
  margin-bottom: 2.5rem;
  opacity: 0.9;
}

.cta_btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.1rem 2.5rem;
  font-size: 1.15rem;
  font-weight: 700;
  border-radius: 1.25rem;
  background: var(--color_primary);
  color: var(--color_text_on_primary);
  box-shadow: 0 8px 24px rgba(0, 234, 255, 0.13);
  border: none;
  outline: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  text-decoration: none;
  min-width: 180px;
  justify-content: center;
  transition:
    background 0.18s,
    color 0.18s,
    box-shadow 0.18s;
}
.cta_btn:hover,
.cta_btn:focus {
  background: var(--color_primary_dark);
  color: var(--color_text_on_primary);
  box-shadow: 0 12px 32px rgba(0, 234, 255, 0.18);
  transform: translateY(-2px) scale(1.03);
}
.cta_btn:focus-visible {
  outline: 2px solid #00eaff;
  outline-offset: 2px;
}
.btn_icon {
  width: 1.35rem;
  height: 1.35rem;
  transition: transform 0.2s;
}
.cta_btn:hover .btn_icon,
.cta_btn:focus .btn_icon {
  transform: scale(1.15) translateX(2px);
}
.btn_text {
  display: inline-block;
  font-weight: 700;
  letter-spacing: 0.01em;
}
@media (max-width: 768px) {
  .features_section {
    padding: 4rem 1rem;
  }

  .features_title {
    font-size: 2.5rem;
  }

  .features_grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .feature_card {
    padding: 2rem 1.5rem;
  }

  .cta_btn {
    width: 100%;
    min-width: 0;
    justify-content: center;
    font-size: 1rem;
    padding: 1rem 1.25rem;
  }
}

@media (max-width: 480px) {
  .features_section {
    padding: 3rem 1rem;
  }

  .features_title {
    font-size: 2rem;
  }

  .feature_card {
    padding: 1.5rem 1rem;
  }

  .feature_icon_wrapper {
    width: 60px;
    height: 60px;
    margin-bottom: 1.5rem;
  }

  .feature_icon {
    font-size: 1.5rem;
  }
}

/* Footer */
.footer {
  background: var(--color_surface);
  color: var(--color_text_on_surface);
  padding: 4rem 2rem 2rem;
}

.footer_container {
  max-width: 1200px;
  margin: 0 auto;
}

.footer_main {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 4rem;
  margin-bottom: 3rem;
}

.footer_brand {
  max-width: 300px;
}

.footer_title {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: var(--color_primary);
}

.footer_description {
  color: #9ca3af;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.footer_social {
  display: flex;
  gap: 1rem;
}

.social_link {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  transition: all 0.3s ease;
}

.social_link:hover {
  background: #3b82f6;
  color: white;
  transform: translateY(-2px);
}

.footer_links {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

.footer_column_title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #f9fafb;
}

.footer_link {
  display: block;
  color: var(--color_text_secondary);
  text-decoration: none;
  margin-bottom: 0.5rem;
  transition: color 0.3s ease;
}

.footer_link:hover {
  color: var(--color_primary);
  text-decoration: none;
}

.footer_bottom {
  border-top: 1px solid #374151;
  padding-top: 2rem;
  text-align: center;
}

.footer_copyright {
  color: #9ca3af;
  font-size: 0.875rem;
}

/* Animations */
@keyframes float {
  0%,
  100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
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

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes particleFloat {
  0% {
    transform: translateY(0px) translateX(0px);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) translateX(50px);
    opacity: 0;
  }
}

/* Market Overview Section */
.market_overview_section {
  padding: 6rem 0;
  background: var(--color_background);
  position: relative;
}

.section_container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section_header {
  text-align: center;
  margin-bottom: 4rem;
}

.section_badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--color_surface);
  border: 1.5px solid var(--color_primary);
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--color_primary);
  margin-bottom: 1.5rem;
}

.section_title {
  font-size: 3rem;
  font-weight: 900;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--color_primary), var(--color_secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section_subtitle {
  font-size: 1.25rem;
  color: var(--color_text_secondary);
  max-width: 600px;
  margin: 0 auto 2rem auto;
  line-height: 1.6;
}

.market_insights {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 3rem;
}

.insight_card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: var(--color_surface);
  border: 1px solid var(--color_border);
  border-radius: 1rem;
  transition: all 0.3s ease;
}

.insight_card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border-color: var(--color_primary);
}

.insight_icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.insight_content {
  flex: 1;
}

.insight_title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color_text);
  margin-bottom: 0.5rem;
}

.insight_text {
  font-size: 0.875rem;
  color: var(--color_text_secondary);
  line-height: 1.4;
}

.market_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.market_card {
  background: var(--color_surface);
  border: 1px solid var(--color_border);
  border-radius: 1.5rem;
  padding: 2rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  text-decoration: none;
  display: block;
  color: inherit;
}

.market_card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border-color: var(--color_primary);
  text-decoration: none;
  color: inherit;
}

.market_card_header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.market_info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.market_symbol {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color_text);
}

.market_name {
  font-size: 0.9rem;
  color: var(--color_text_secondary);
}

.market_price {
  font-size: 1.75rem;
  font-weight: 700;
  text-align: right;
}

.price-up {
  color: #10b981;
}

.price-down {
  color: #ef4444;
}

.market_card_body {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1rem;
}

.market_stats {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
}

.market_stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat_label {
  font-size: 0.85rem;
  color: var(--color_text_secondary);
}

.stat_value {
  font-size: 0.9rem;
  font-weight: 600;
}

.text-green-500 {
  color: #10b981;
}

.text-red-500 {
  color: #ef4444;
}

.market_chart_mini {
  width: 100px;
  height: 40px;
}

.mini_chart {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-up {
  color: #10b981;
}

.chart-down {
  color: #ef4444;
}

.chart_svg {
  width: 100%;
  height: 100%;
}

/* Trading Signals Section */
.signals_section {
  padding: 6rem 0;
  background: var(--color_surface);
  position: relative;
}

.signals_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.signal_card {
  background: var(--color_background);
  border: 1px solid var(--color_border);
  border-radius: 1.5rem;
  padding: 2rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.signal_card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border-color: var(--color_primary);
}

.signal_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.signal_pair {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color_text);
}

.signal_type {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
}

.signal_type.buy {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.signal_type.sell {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.signal_type.hold {
  background: rgba(156, 163, 175, 0.1);
  color: #9ca3af;
  border: 1px solid rgba(156, 163, 175, 0.2);
}

.signal_body {
  margin-bottom: 1.5rem;
}

.signal_strength {
  margin-bottom: 1.5rem;
}

.strength_label {
  display: block;
  font-size: 0.875rem;
  color: var(--color_text_secondary);
  margin-bottom: 0.5rem;
}

.strength_bar {
  width: 100%;
  height: 8px;
  background: var(--color_border);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.strength_fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color_primary), var(--color_secondary));
  border-radius: 4px;
  transition: width 0.3s ease;
}

.strength_value {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color_text);
}

.signal_details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.signal_detail {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail_label {
  font-size: 0.8rem;
  color: var(--color_text_secondary);
}

.detail_value {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color_text);
}

.signal_reason {
  margin-bottom: 1.5rem;
}

.reason_label {
  display: block;
  font-size: 0.875rem;
  color: var(--color_text_secondary);
  margin-bottom: 0.5rem;
}

.reason_text {
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--color_text);
}

.signal_actions {
  display: flex;
  gap: 1rem;
}

.btn-primary {
  background: var(--color_primary);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-block;
}

.btn-primary:hover {
  background: var(--color_primary);
  transform: translateY(-2px);
  color: white;
  text-decoration: none;
}

.btn-secondary {
  background: var(--color_surface);
  color: var(--color_text);
  border: 1px solid var(--color_border);
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-block;
}

.btn-secondary:hover {
  background: var(--color_surface);
  border-color: var(--color_primary);
  transform: translateY(-2px);
  color: var(--color_text);
  text-decoration: none;
}

/* Market Statistics Section */
.stats_section {
  padding: 6rem 0;
  background: var(--color_background);
  position: relative;
}

.stats_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.stat_card {
  background: var(--color_surface);
  border: 1px solid var(--color_border);
  border-radius: 1.5rem;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  text-decoration: none;
  display: block;
  color: inherit;
}

.stat_card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border-color: var(--color_primary);
  text-decoration: none;
  color: inherit;
}

.stat_card_header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat_icon {
  font-size: 2.5rem;
}

.stat_title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color_text_secondary);
}

.stat_value {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--color_text);
  margin-bottom: 0.5rem;
}

.stat_change {
  font-size: 0.9rem;
  font-weight: 600;
}

.stat_change.positive {
  color: #10b981;
}

.stat_change.negative {
  color: #ef4444;
}

.stat_label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color_text_secondary);
}

/* Recent Trades Section */
.trades_section {
  padding: 6rem 0;
  background: var(--color_surface);
  position: relative;
}

.trades_feed {
  background: var(--color_background);
  border: 1px solid var(--color_border);
  border-radius: 1.5rem;
  overflow: hidden;
}

.trade_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--color_border);
  transition: background-color 0.2s ease;
}

.trade_item:last-child {
  border-bottom: none;
}

.trade_item:hover {
  background: var(--color_surface);
}

.trade_info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.trade_pair {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color_text);
}

.trade_type {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  width: fit-content;
}

.trade_type.buy {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.trade_type.sell {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.trade_details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  text-align: center;
}

.trade_amount {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color_text);
}

.trade_price {
  font-size: 0.9rem;
  color: var(--color_text_secondary);
}

.trade_time {
  font-size: 0.8rem;
  color: var(--color_text_secondary);
}

.trade_user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user_avatar {
  width: 40px;
  height: 40px;
  background: var(--color_primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
}

.user_name {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color_text);
}

/* Performance Section */
.performance_section {
  padding: 6rem 0;
  background: var(--color_background);
  position: relative;
}

.performance_grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
}

.performance_card {
  background: var(--color_surface);
  border: 1px solid var(--color_border);
  border-radius: 1.5rem;
  padding: 2rem;
  transition: all 0.3s ease;
}

.performance_card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border-color: var(--color_primary);
}

.performance_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.performance_title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color_text);
}

.performance_controls {
  display: flex;
  gap: 0.5rem;
}

.time_btn {
  padding: 0.5rem 1rem;
  border: 1px solid var(--color_border);
  background: var(--color_background);
  color: var(--color_text_secondary);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.time_btn.active,
.time_btn:hover {
  background: var(--color_primary);
  color: white;
  border-color: var(--color_primary);
}

.performance_chart {
  height: 300px;
}

.performance_metrics {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.metric_card {
  background: var(--color_surface);
  border: 1px solid var(--color_border);
  border-radius: 1rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
  text-decoration: none;
  display: block;
  color: inherit;
}

.metric_card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border-color: var(--color_primary);
  text-decoration: none;
  color: inherit;
}

.metric_header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.metric_icon {
  font-size: 1.5rem;
}

.metric_title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color_text_secondary);
}

.metric_value {
  font-size: 2rem;
  font-weight: 900;
  color: var(--color_text);
  margin-bottom: 0.5rem;
}

.metric_change {
  font-size: 0.875rem;
  font-weight: 600;
}

.metric_change.positive {
  color: #10b981;
}

/* News Section */
.news_section {
  padding: 6rem 0;
  background: var(--color_surface);
  position: relative;
}

.news_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.news_card {
  background: var(--color_background);
  border: 1px solid var(--color_border);
  border-radius: 1.5rem;
  overflow: hidden;
  transition: all 0.3s ease;
  text-decoration: none;
  display: block;
  color: inherit;
}

.news_card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border-color: var(--color_primary);
  text-decoration: none;
  color: inherit;
}

.news_image {
  height: 120px;
  background: linear-gradient(135deg, var(--color_primary), var(--color_secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.news_category {
  background: rgba(255, 255, 255, 0.9);
  color: var(--color_primary);
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
}

.news_content {
  padding: 1.5rem;
}

.news_title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color_text);
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.news_excerpt {
  font-size: 0.9rem;
  color: var(--color_text_secondary);
  line-height: 1.5;
  margin-bottom: 1rem;
}

.news_meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: var(--color_text_secondary);
}

/* Responsive Design */
@media (max-width: 768px) {
  .header_content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .hero_content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }

  .hero_title {
    font-size: 2.5rem;
  }

  .hero_buttons {
    flex-direction: column;
    align-items: center;
  }

  .hero_stats {
    justify-content: center;
  }

  .trading_card {
    transform: none;
  }

  .trading_card:hover {
    transform: translateY(-5px);
  }

  .features_grid {
    grid-template-columns: 1fr;
  }

  .footer_main {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .footer_links {
    grid-template-columns: repeat(2, 1fr);
  }

  .market_grid {
    grid-template-columns: 1fr;
  }

  .market_insights {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .insight_card {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }

  .signals_grid {
    grid-template-columns: 1fr;
  }

  .stats_grid {
    grid-template-columns: 1fr;
  }

  .performance_grid {
    grid-template-columns: 1fr;
  }

  .news_grid {
    grid-template-columns: 1fr;
  }

  .section_title {
    font-size: 2rem;
  }

  .market_card_header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .signal_details {
    grid-template-columns: 1fr;
  }

  .trade_item {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .performance_header {
    flex-direction: column;
    gap: 1rem;
  }

  .performance_controls {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .hero_title {
    font-size: 2rem;
  }

  .hero_description {
    font-size: 1rem;
  }

  .features_title {
    font-size: 2rem;
  }

  .cta_title {
    font-size: 2rem;
  }

  .footer_links {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .hero_stats {
    gap: 1.25rem;
    margin-top: 1.5rem;
  }
  .stat_item {
    min-width: 90px;
    margin-right: 0.75rem;
  }
  .stat_number {
    font-size: 1.5rem;
  }
  .stat_label {
    font-size: 0.95rem;
  }
}
</style>
