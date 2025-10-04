<template>
  <div class="relative h-full">
    <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white dark:bg-gray-800 bg-opacity-50 z-10">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>
    
    <div v-if="!symbol" class="h-full flex items-center justify-center text-gray-500 dark:text-gray-400">
      <div class="text-center">
        <ChartBarIcon class="h-16 w-16 mx-auto mb-4 opacity-50" />
        <p class="text-lg">Select a symbol to view chart</p>
      </div>
    </div>
    
    <canvas
      v-else
      ref="chartRef"
      :class="{ 'opacity-50': loading }"
    ></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { ChartBarIcon } from '@heroicons/vue/24/outline'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import 'chartjs-adapter-date-fns'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

// Props
interface Props {
  symbol?: string
  period: string
}

const props = withDefaults(defineProps<Props>(), {
  symbol: undefined
})

// Emits
const emit = defineEmits<{
  loading: [loading: boolean]
}>()

// Refs
const chartRef = ref<HTMLCanvasElement>()
const chartInstance = ref<ChartJS | null>(null)
const loading = ref(false)

// Generate mock OHLCV data
const generateMockOHLCVData = (period: string) => {
  const now = new Date()
  const dataPoints: any[] = []
  let basePrice = 150 + Math.random() * 100 // Random base price
  let intervals: number
  let timeStep: number

  // Determine intervals and time step based on period
  switch (period) {
    case '1D':
      intervals = 390 // Market minutes in a day
      timeStep = 60 * 1000 // 1 minute
      break
    case '5D':
      intervals = 390 * 5 // 5 trading days
      timeStep = 60 * 1000 // 1 minute
      break
    case '1M':
      intervals = 22 // Trading days in a month
      timeStep = 24 * 60 * 60 * 1000 // 1 day
      break
    case '3M':
      intervals = 66 // ~3 months of trading days
      timeStep = 24 * 60 * 60 * 1000 // 1 day
      break
    case '1Y':
      intervals = 52 // Weeks in a year
      timeStep = 7 * 24 * 60 * 60 * 1000 // 1 week
      break
    default:
      intervals = 390
      timeStep = 60 * 1000
  }

  // Generate candlestick data
  for (let i = 0; i < Math.min(intervals, 200); i++) { // Limit to 200 points for performance
    const time = new Date(now.getTime() - (intervals - i - 1) * timeStep)
    
    // Random walk for price
    const change = (Math.random() - 0.5) * (basePrice * 0.02) // 2% max change
    const open = i === 0 ? basePrice : dataPoints[i - 1].close
    const close = Math.max(open + change, 1) // Ensure positive price
    
    // Generate high/low based on volatility
    const volatility = Math.random() * 0.015 + 0.005 // 0.5% to 2% volatility
    const range = Math.max(Math.abs(close - open), open * volatility)
    const high = Math.max(open, close) + (Math.random() * range * 0.5)
    const low = Math.min(open, close) - (Math.random() * range * 0.5)
    
    // Generate volume
    const avgVolume = 1000000 + Math.random() * 2000000
    const volume = Math.floor(avgVolume * (0.5 + Math.random()))
    
    dataPoints.push({
      x: time,
      open,
      high: Math.max(high, Math.max(open, close)),
      low: Math.max(low, Math.min(open, close) * 0.95), // Ensure low is not too low
      close,
      volume
    })
    
    basePrice = close
  }

  return dataPoints
}

// Custom candlestick chart renderer using line chart
const createChart = () => {
  if (!chartRef.value || !props.symbol) return

  const isDark = document.documentElement.classList.contains('dark')
  const mockData = generateMockOHLCVData(props.period)
  
  // Create datasets for high, low, open, close
  const priceData = mockData.map(point => ({
    x: point.x,
    y: point.close
  }))

  const volumeData = mockData.map(point => ({
    x: point.x,
    y: point.volume
  }))

  // Calculate price range for volume scaling
  const prices = mockData.map(p => p.close)
  const maxPrice = Math.max(...prices)
  const minPrice = Math.min(...prices)
  const priceRange = maxPrice - minPrice

  // Scale volume to 20% of price range
  const maxVolume = Math.max(...mockData.map(p => p.volume))
  const volumeScale = (priceRange * 0.2) / maxVolume

  const scaledVolumeData = volumeData.map(point => ({
    x: point.x,
    y: minPrice - priceRange * 0.1 + (point.y * volumeScale)
  }))

  chartInstance.value = new ChartJS(chartRef.value, {
    type: 'line',
    data: {
      datasets: [
        {
          label: 'Price',
          data: priceData,
          borderColor: 'rgb(34, 197, 94)',
          backgroundColor: 'rgba(34, 197, 94, 0.1)',
          borderWidth: 2,
          fill: false,
          pointRadius: 0,
          pointHoverRadius: 4,
          pointBackgroundColor: 'rgb(34, 197, 94)',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          tension: 0.1,
          yAxisID: 'price'
        },
        {
          label: 'Volume',
          data: scaledVolumeData,
          backgroundColor: 'rgba(59, 130, 246, 0.3)',
          borderColor: 'rgb(59, 130, 246)',
          borderWidth: 1,
          type: 'bar' as any,
          yAxisID: 'volume',
          barPercentage: 0.8,
          categoryPercentage: 0.9,
        }
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          backgroundColor: isDark ? 'rgba(31, 41, 55, 0.95)' : 'rgba(255, 255, 255, 0.95)',
          titleColor: isDark ? '#f9fafb' : '#111827',
          bodyColor: isDark ? '#f9fafb' : '#111827',
          borderColor: isDark ? '#374151' : '#e5e7eb',
          borderWidth: 1,
          cornerRadius: 8,
          displayColors: false,
          callbacks: {
            title: (context) => {
              const date = new Date(context[0].parsed.x)
              return formatTooltipDate(date, props.period)
            },
            label: (context) => {
              if (context.datasetIndex === 0) {
                const dataIndex = context.dataIndex
                const ohlcData = mockData[dataIndex]
                return [
                  `${props.symbol}`,
                  `Open: ${formatCurrency(ohlcData.open)}`,
                  `High: ${formatCurrency(ohlcData.high)}`,
                  `Low: ${formatCurrency(ohlcData.low)}`,
                  `Close: ${formatCurrency(ohlcData.close)}`
                ]
              } else {
                const dataIndex = context.dataIndex
                const volume = mockData[dataIndex]?.volume || 0
                return `Volume: ${formatVolume(volume)}`
              }
            },
          },
          filter: (tooltipItem) => {
            return tooltipItem.datasetIndex === 0 // Only show tooltip for price data
          }
        },
      },
      scales: {
        x: {
          type: 'time',
          time: {
            displayFormats: getTimeDisplayFormats(props.period),
          },
          grid: {
            display: false,
          },
          ticks: {
            color: isDark ? '#9ca3af' : '#6b7280',
            maxTicksLimit: 8,
          },
        },
        price: {
          type: 'linear',
          display: true,
          position: 'right',
          grid: {
            color: isDark ? 'rgba(75, 85, 99, 0.3)' : 'rgba(229, 231, 235, 0.8)',
            drawBorder: false,
          },
          ticks: {
            color: isDark ? '#9ca3af' : '#6b7280',
            callback: function(value) {
              return formatCurrency(value as number)
            },
          },
        },
        volume: {
          type: 'linear',
          display: false,
          min: minPrice - priceRange * 0.15,
          max: minPrice + priceRange * 0.05,
        },
      },
      interaction: {
        mode: 'index',
        intersect: false,
      },
      hover: {
        mode: 'index',
        intersect: false,
      },
    },
  })
}

// Utility functions
const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount)
}

const formatVolume = (volume: number) => {
  if (volume >= 1000000000) {
    return `${(volume / 1000000000).toFixed(1)}B`
  } else if (volume >= 1000000) {
    return `${(volume / 1000000).toFixed(1)}M`
  } else if (volume >= 1000) {
    return `${(volume / 1000).toFixed(1)}K`
  }
  return volume.toLocaleString()
}

const formatTooltipDate = (date: Date, period: string) => {
  switch (period) {
    case '1D':
    case '5D':
      return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      })
    default:
      return date.toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
  }
}

const getTimeDisplayFormats = (period: string) => {
  switch (period) {
    case '1D':
      return {
        minute: 'HH:mm',
        hour: 'HH:mm'
      }
    case '5D':
      return {
        hour: 'MMM d, HH:mm',
        day: 'MMM d'
      }
    case '1M':
    case '3M':
      return {
        day: 'MMM d',
        week: 'MMM d'
      }
    case '1Y':
      return {
        month: 'MMM yyyy',
        quarter: 'MMM yyyy'
      }
    default:
      return {
        day: 'MMM d'
      }
  }
}

// Chart update logic
const updateChart = async () => {
  if (!props.symbol) return
  
  loading.value = true
  emit('loading', true)
  
  // Simulate loading delay
  await new Promise(resolve => setTimeout(resolve, 800))
  
  if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }
  
  await nextTick()
  createChart()
  
  loading.value = false
  emit('loading', false)
}

// Handle theme changes
const handleThemeChange = () => {
  if (props.symbol) {
    updateChart()
  }
}

// Watchers
watch(() => props.symbol, (newSymbol) => {
  if (newSymbol) {
    updateChart()
  } else if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }
})

watch(() => props.period, () => {
  if (props.symbol) {
    updateChart()
  }
})

// Lifecycle
onMounted(async () => {
  if (props.symbol) {
    await nextTick()
    createChart()
  }
  
  // Listen for theme changes
  const observer = new MutationObserver(handleThemeChange)
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  })
})

onUnmounted(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }
})
</script>

<style scoped>
canvas {
  @apply w-full h-full;
}
</style>