<template>
  <div class="apex-candlestick-chart">
    <div class="chart-header">
      <h3 class="chart-title">{{ title }}</h3>
      <div class="chart-controls">
        <button @click="refreshData" :disabled="loading" class="control-btn">
          {{ loading ? 'Loading...' : 'Refresh' }}
        </button>
        <button @click="toggleTheme" class="control-btn theme-btn">
          {{ currentTheme === 'dark' ? '☀️' : '🌙' }}
        </button>
        <span class="last-update">
          {{ lastUpdate ? `Last: ${formatTime(lastUpdate)}` : 'No data' }}
        </span>
      </div>
    </div>

    <div class="chart-container">
      <apexchart type="candlestick" height="350" :options="chartOptions" :series="series" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

// Props
interface Props {
  title?: string
  height?: number
}

const props = withDefaults(defineProps<Props>(), {
  title: 'BTC/USD - Candlestick Chart',
  height: 350,
})

// Reactive data
const loading = ref(false)
const lastUpdate = ref<Date | null>(null)

// Theme detection
const getCurrentTheme = () => {
  if (typeof window !== 'undefined') {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) return savedTheme

    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark'
    }
  }
  return 'light'
}

const currentTheme = ref(getCurrentTheme())

// Toggle theme function
const toggleTheme = () => {
  const newTheme = currentTheme.value === 'dark' ? 'light' : 'dark'
  currentTheme.value = newTheme
  localStorage.setItem('theme', newTheme)
  document.documentElement.setAttribute('data_theme', newTheme)
}

// Listen for theme changes
onMounted(() => {
  const observer = new MutationObserver(() => {
    const newTheme = getCurrentTheme()
    if (newTheme !== currentTheme.value) {
      currentTheme.value = newTheme
    }
  })

  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data_theme'],
  })

  // Also listen for storage changes
  window.addEventListener('storage', () => {
    const newTheme = getCurrentTheme()
    if (newTheme !== currentTheme.value) {
      currentTheme.value = newTheme
    }
  })
})

// Chart data
const series = ref([
  {
    name: 'candle',
    data: [
      {
        x: new Date(1538778600000),
        y: [6629.81, 6650.5, 6623.04, 6633.33],
      },
      {
        x: new Date(1538780400000),
        y: [6632.01, 6643.59, 6620, 6630.11],
      },
      {
        x: new Date(1538782200000),
        y: [6630.71, 6648.95, 6623.34, 6635.65],
      },
      {
        x: new Date(1538784000000),
        y: [6635.65, 6651, 6629.67, 6638.24],
      },
      {
        x: new Date(1538785800000),
        y: [6638.24, 6640, 6620, 6624.47],
      },
      {
        x: new Date(1538787600000),
        y: [6624.53, 6636.03, 6621.68, 6624.31],
      },
      {
        x: new Date(1538789400000),
        y: [6624.61, 6632.2, 6617, 6626.02],
      },
      {
        x: new Date(1538791200000),
        y: [6627, 6627.62, 6584.22, 6603.02],
      },
      {
        x: new Date(1538793000000),
        y: [6605, 6608.03, 6598.95, 6604.01],
      },
      {
        x: new Date(1538794800000),
        y: [6604.5, 6614.4, 6602.26, 6608.02],
      },
      {
        x: new Date(1538796600000),
        y: [6608.02, 6610.68, 6601.99, 6608.91],
      },
      {
        x: new Date(1538798400000),
        y: [6608.91, 6618.99, 6608.01, 6612],
      },
      {
        x: new Date(1538800200000),
        y: [6612, 6615.13, 6605.09, 6612],
      },
      {
        x: new Date(1538802000000),
        y: [6612, 6624.12, 6608.43, 6622.95],
      },
      {
        x: new Date(1538803800000),
        y: [6623.91, 6623.91, 6615, 6615.67],
      },
      {
        x: new Date(1538805600000),
        y: [6618.69, 6618.74, 6610, 6610.4],
      },
      {
        x: new Date(1538807400000),
        y: [6611, 6622.78, 6610.4, 6614.9],
      },
      {
        x: new Date(1538809200000),
        y: [6614.9, 6626.2, 6613.33, 6623.45],
      },
      {
        x: new Date(1538811000000),
        y: [6623.48, 6627, 6618.38, 6620.35],
      },
      {
        x: new Date(1538812800000),
        y: [6619.43, 6620.35, 6610.05, 6615.53],
      },
      {
        x: new Date(1538814600000),
        y: [6615.53, 6617.93, 6610, 6615.19],
      },
      {
        x: new Date(1538816400000),
        y: [6615.19, 6621.6, 6608.2, 6620],
      },
      {
        x: new Date(1538818200000),
        y: [6619.54, 6625.17, 6614.15, 6620],
      },
      {
        x: new Date(1538820000000),
        y: [6620.33, 6634.15, 6617.24, 6624.61],
      },
      {
        x: new Date(1538821800000),
        y: [6625.95, 6626, 6611.66, 6617.58],
      },
      {
        x: new Date(1538823600000),
        y: [6619, 6625.97, 6595.27, 6598.86],
      },
      {
        x: new Date(1538825400000),
        y: [6598.86, 6598.88, 6570, 6587.16],
      },
      {
        x: new Date(1538827200000),
        y: [6588.86, 6600, 6580, 6593.4],
      },
      {
        x: new Date(1538829000000),
        y: [6593.99, 6598.89, 6585, 6587.81],
      },
      {
        x: new Date(1538830800000),
        y: [6587.81, 6592.73, 6567.14, 6578],
      },
      {
        x: new Date(1538832600000),
        y: [6578.35, 6581.72, 6567.39, 6579],
      },
      {
        x: new Date(1538834400000),
        y: [6579.38, 6580.92, 6566.77, 6575.96],
      },
      {
        x: new Date(1538836200000),
        y: [6575.96, 6589, 6571.77, 6588.92],
      },
      {
        x: new Date(1538838000000),
        y: [6588.92, 6594, 6577.55, 6589.22],
      },
      {
        x: new Date(1538839800000),
        y: [6589.3, 6598.89, 6589.1, 6596.08],
      },
      {
        x: new Date(1538841600000),
        y: [6597.5, 6600, 6588.39, 6596.25],
      },
      {
        x: new Date(1538843400000),
        y: [6598.03, 6600, 6588.73, 6595.97],
      },
      {
        x: new Date(1538845200000),
        y: [6595.97, 6602.01, 6588.17, 6602],
      },
      {
        x: new Date(1538847000000),
        y: [6602, 6607, 6596.51, 6599.95],
      },
      {
        x: new Date(1538848800000),
        y: [6600.63, 6601.21, 6590.39, 6591.02],
      },
      {
        x: new Date(1538850600000),
        y: [6591.02, 6603.08, 6591, 6591],
      },
      {
        x: new Date(1538852400000),
        y: [6591, 6601.32, 6585, 6592],
      },
      {
        x: new Date(1538854200000),
        y: [6593.13, 6596.01, 6590, 6593.34],
      },
      {
        x: new Date(1538856000000),
        y: [6593.34, 6604.76, 6582.63, 6593.86],
      },
      {
        x: new Date(1538857800000),
        y: [6593.86, 6604.28, 6586.57, 6600.01],
      },
      {
        x: new Date(1538859600000),
        y: [6601.81, 6603.21, 6592.78, 6596.25],
      },
      {
        x: new Date(1538861400000),
        y: [6596.25, 6604.2, 6590, 6602.99],
      },
      {
        x: new Date(1538863200000),
        y: [6602.99, 6606, 6584.99, 6587.81],
      },
      {
        x: new Date(1538865000000),
        y: [6587.81, 6595, 6583.27, 6591.96],
      },
      {
        x: new Date(1538866800000),
        y: [6591.97, 6596.07, 6585, 6588.39],
      },
      {
        x: new Date(1538868600000),
        y: [6587.6, 6598.21, 6587.6, 6594.27],
      },
      {
        x: new Date(1538870400000),
        y: [6596.44, 6601, 6590, 6596.55],
      },
      {
        x: new Date(1538872200000),
        y: [6598.91, 6605, 6596.61, 6600.02],
      },
      {
        x: new Date(1538874000000),
        y: [6600.55, 6605, 6589.14, 6593.01],
      },
      {
        x: new Date(1538875800000),
        y: [6593.15, 6605, 6592, 6603.06],
      },
      {
        x: new Date(1538877600000),
        y: [6603.07, 6604.5, 6599.09, 6603.89],
      },
      {
        x: new Date(1538879400000),
        y: [6604.44, 6604.44, 6600, 6603.5],
      },
      {
        x: new Date(1538881200000),
        y: [6603.5, 6603.99, 6597.5, 6603.86],
      },
      {
        x: new Date(1538883000000),
        y: [6603.85, 6605, 6600, 6604.07],
      },
      {
        x: new Date(1538884800000),
        y: [6604.98, 6606, 6604.07, 6606],
      },
    ],
  },
])

// Chart options
const chartOptions = computed(() => {
  const isDark = currentTheme.value === 'dark'

  return {
    chart: {
      height: props.height,
      type: 'candlestick',
      background: isDark ? '#1f2937' : '#ffffff',
      foreColor: isDark ? '#f9fafb' : '#1f2937',
      animations: {
        enabled: true,
        easing: 'easeinout',
        speed: 800,
        animateGradually: {
          enabled: true,
          delay: 150,
        },
        dynamicAnimation: {
          enabled: true,
          speed: 350,
        },
      },
    },
    title: {
      text: props.title,
      align: 'left',
      style: {
        fontSize: '16px',
        fontWeight: '600',
        color: isDark ? '#f9fafb' : '#1f2937',
      },
    },
    annotations: {
      xaxis: [
        {
          x: 'Oct 06 14:00',
          borderColor: '#00E396',
          label: {
            borderColor: '#00E396',
            style: {
              fontSize: '12px',
              color: '#fff',
              background: '#00E396',
            },
            orientation: 'horizontal',
            offsetY: 7,
            text: 'Annotation Test',
          },
        },
      ],
    },
    tooltip: {
      enabled: true,
      theme: isDark ? 'dark' : 'light',
      style: {
        fontSize: '12px',
      },
      y: {
        formatter: function (value: number) {
          return '$' + value.toFixed(2)
        },
      },
    },
    xaxis: {
      type: 'category',
      labels: {
        formatter: function (val: number) {
          return new Date(val).toLocaleDateString('en-US', {
            month: 'short',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
          })
        },
        style: {
          colors: isDark ? '#9ca3af' : '#6b7280',
          fontSize: '12px',
        },
      },
      axisBorder: {
        color: isDark ? '#374151' : '#e5e7eb',
      },
      axisTicks: {
        color: isDark ? '#374151' : '#e5e7eb',
      },
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
      labels: {
        formatter: function (value: number) {
          return '$' + value.toFixed(0)
        },
        style: {
          colors: isDark ? '#9ca3af' : '#6b7280',
          fontSize: '12px',
        },
      },
    },
    grid: {
      borderColor: isDark ? '#374151' : '#e5e7eb',
      strokeDashArray: 4,
    },
    plotOptions: {
      candlestick: {
        colors: {
          upward: '#10b981',
          downward: '#ef4444',
        },
        wick: {
          useFillColor: true,
        },
      },
    },
  }
})

// Generate new data
const generateNewData = () => {
  const newData = []
  const basePrice = 45000
  let currentPrice = basePrice

  const startDate = new Date()
  startDate.setDate(startDate.getDate() - 50)

  for (let i = 0; i < 50; i++) {
    const date = new Date(startDate)
    date.setDate(date.getDate() + i)

    // Generate realistic price movement
    const volatility = 0.03
    const trend = Math.sin(i / 10) * 0.01
    const randomFactor = (Math.random() - 0.5) * volatility

    const open = currentPrice
    const change = currentPrice * (trend + randomFactor)
    const close = open + change

    const spread = Math.abs(change) * 0.3 + Math.random() * currentPrice * 0.01
    const high = Math.max(open, close) + spread
    const low = Math.min(open, close) - spread

    newData.push({
      x: date.getTime(),
      y: [
        Number(open.toFixed(2)),
        Number(high.toFixed(2)),
        Number(low.toFixed(2)),
        Number(close.toFixed(2)),
      ],
    })

    currentPrice = close
  }

  return newData
}

// Refresh data
const refreshData = async () => {
  loading.value = true
  try {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    const newData = generateNewData()
    series.value = [
      {
        name: 'candle',
        data: newData,
      },
    ]

    lastUpdate.value = new Date()
    console.log('Data refreshed:', newData.length, 'points')
  } catch (error) {
    console.error('Failed to refresh data:', error)
  } finally {
    loading.value = false
  }
}

// Format time
const formatTime = (date: Date): string => {
  return date.toLocaleTimeString()
}

// Initialize
onMounted(() => {
  lastUpdate.value = new Date()
  console.log('ApexCandlestickChart initialized with', series.value[0].data.length, 'data points')
})
</script>

<style scoped>
.apex-candlestick-chart {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: background-color 0.3s ease;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.control-btn {
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.control-btn:hover:not(:disabled) {
  background: #2563eb;
}

.control-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.theme-btn {
  min-width: 40px;
  font-size: 1.2rem;
  padding: 8px 12px;
}

.last-update {
  font-size: 0.875rem;
  color: #6b7280;
}

.chart-container {
  width: 100%;
  position: relative;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .apex-candlestick-chart {
    background: #1f2937;
  }

  .chart-title {
    color: #f9fafb;
  }

  .last-update {
    color: #9ca3af;
  }
}

/* Dynamic dark mode support */
[data_theme='dark'] .apex-candlestick-chart {
  background: #1f2937;
}

[data_theme='dark'] .chart-title {
  color: #f9fafb;
}

[data_theme='dark'] .last-update {
  color: #9ca3af;
}
</style>
