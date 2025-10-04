<template>
  <div class="bg-white rounded-lg shadow p-4">
    <h3 class="text-lg font-medium text-gray-900 mb-2">BTC/USD Price Chart</h3>
    <line-chart v-if="chartData" :chart-data="chartData" :chart-options="chartOptions" />
    <div v-else class="text-center text-gray-400 py-8">Loading chart...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import axios from 'axios'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

const chartData = ref<any>(null)
const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: false },
  },
  scales: {
    x: { display: true, title: { display: true, text: 'Time' } },
    y: { display: true, title: { display: true, text: 'Price (USD)' } },
  },
})

const fetchChartData = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/trading/price_feed/')
    // Simulate OHLCV data for the chart (replace with real endpoint if available)
    const now = new Date()
    const labels = Array.from({ length: 20 }, (_, i) => {
      const d = new Date(now.getTime() - (19 - i) * 60000)
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    })
    const prices = Array.from({ length: 20 }, () => response.data.close + (Math.random() - 0.5) * 100)
    chartData.value = {
      labels,
      datasets: [
        {
          label: 'BTC/USD',
          data: prices,
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.3,
        },
      ],
    }
  } catch (err) {
    chartData.value = null
  }
}

onMounted(fetchChartData)

// Expose for parent refresh
export { fetchChartData }
</script>

<script lang="ts">
import { defineComponent } from 'vue'
import { Line } from 'vue-chartjs'
export default defineComponent({
  name: 'PriceChart',
  components: { LineChart: Line },
})
</script> 