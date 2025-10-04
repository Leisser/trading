<template>
  <div class="relative h-full">
    <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white dark:bg-gray-800 bg-opacity-50">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>
    
    <canvas
      ref="chartRef"
      :class="{ 'opacity-50': loading }"
    ></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

// Props
interface Props {
  data?: any[]
  period: string
}

const props = withDefaults(defineProps<Props>(), {
  data: () => []
})

// Emits
const emit = defineEmits<{
  loading: [loading: boolean]
}>()

// Refs
const chartRef = ref<HTMLCanvasElement>()
const chartInstance = ref<ChartJS | null>(null)
const loading = ref(false)

// Mock data generation
const generateMockData = (period: string) => {
  const now = new Date()
  const dataPoints: { time: Date; value: number }[] = []
  let baseValue = 125000
  let intervals: number
  let timeStep: number

  // Determine intervals and time step based on period
  switch (period) {
    case '1D':
      intervals = 390 // Market minutes in a day
      timeStep = 60 * 1000 // 1 minute
      break
    case '1W':
      intervals = 35 // 5 trading days * 7 data points per day
      timeStep = 2 * 60 * 60 * 1000 // 2 hours
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

  // Generate random walk data
  for (let i = 0; i < intervals; i++) {
    const time = new Date(now.getTime() - (intervals - i - 1) * timeStep)
    const change = (Math.random() - 0.48) * 1000 // Slightly upward bias
    baseValue += change
    dataPoints.push({ time, value: Math.max(baseValue, 50000) }) // Minimum value
  }

  return dataPoints
}

// Chart creation
const createChart = () => {
  if (!chartRef.value) return

  const isDark = document.documentElement.classList.contains('dark')
  
  const mockData = generateMockData(props.period)
  const labels = mockData.map(point => point.time)
  const values = mockData.map(point => point.value)
  
  // Calculate if portfolio is up or down
  const isPositive = values[values.length - 1] > values[0]
  
  const gradientFill = chartRef.value.getContext('2d')!.createLinearGradient(0, 0, 0, 400)
  if (isPositive) {
    gradientFill.addColorStop(0, 'rgba(34, 197, 94, 0.2)')
    gradientFill.addColorStop(1, 'rgba(34, 197, 94, 0.02)')
  } else {
    gradientFill.addColorStop(0, 'rgba(239, 68, 68, 0.2)')
    gradientFill.addColorStop(1, 'rgba(239, 68, 68, 0.02)')
  }

  chartInstance.value = new ChartJS(chartRef.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Portfolio Value',
          data: values,
          borderColor: isPositive ? 'rgb(34, 197, 94)' : 'rgb(239, 68, 68)',
          backgroundColor: gradientFill,
          borderWidth: 2,
          fill: true,
          pointRadius: 0,
          pointHoverRadius: 4,
          pointBackgroundColor: isPositive ? 'rgb(34, 197, 94)' : 'rgb(239, 68, 68)',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          tension: 0.1,
        },
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
              const date = new Date(context[0].label!)
              return formatTooltipDate(date, props.period)
            },
            label: (context) => {
              const value = context.parsed.y
              const change = value - values[0]
              const changePercent = (change / values[0]) * 100
              return [
                `Value: ${formatCurrency(value)}`,
                `Change: ${formatCurrency(change)} (${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(2)}%)`
              ]
            },
          },
        },
      },
      scales: {
        x: {
          display: true,
          grid: {
            display: false,
          },
          ticks: {
            color: isDark ? '#9ca3af' : '#6b7280',
            maxTicksLimit: 6,
            callback: function(value, index) {
              const date = new Date(labels[index])
              return formatAxisDate(date, props.period)
            },
          },
        },
        y: {
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
      },
      interaction: {
        mode: 'index',
        intersect: false,
      },
      hover: {
        mode: 'index',
        intersect: false,
      },
      elements: {
        point: {
          hoverRadius: 6,
        },
      },
    },
  })
}

// Utility functions
const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount)
}

const formatAxisDate = (date: Date, period: string) => {
  switch (period) {
    case '1D':
      return date.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: false 
      })
    case '1W':
      return date.toLocaleDateString('en-US', { 
        weekday: 'short',
        hour: 'numeric'
      })
    case '1M':
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      })
    case '3M':
    case '1Y':
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      })
    default:
      return date.toLocaleDateString('en-US')
  }
}

const formatTooltipDate = (date: Date, period: string) => {
  switch (period) {
    case '1D':
      return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      })
    case '1W':
      return date.toLocaleString('en-US', {
        weekday: 'long',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      })
    default:
      return date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
  }
}

// Destroy and recreate chart
const updateChart = async () => {
  loading.value = true
  emit('loading', true)
  
  // Simulate loading delay
  await new Promise(resolve => setTimeout(resolve, 500))
  
  if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }
  
  await nextTick()
  createChart()
  
  loading.value = false
  emit('loading', false)
}

// Watch for period changes
watch(() => props.period, updateChart)

// Handle theme changes
const handleThemeChange = () => {
  updateChart()
}

// Lifecycle
onMounted(async () => {
  await nextTick()
  createChart()
  
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