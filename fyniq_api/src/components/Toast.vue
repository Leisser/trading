<template>
  <transition name="fade">
    <div v-if="visible" :class="toastClass" class="fixed top-6 right-6 z-50 px-4 py-3 rounded shadow-lg flex items-center space-x-2">
      <span v-if="icon" v-html="icon" class="text-xl"></span>
      <span>{{ message }}</span>
      <button @click="close" class="ml-2 text-lg font-bold">&times;</button>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = defineProps({
  message: String,
  type: {
    type: String,
    default: 'info',
  },
  duration: {
    type: Number,
    default: 3000,
  },
})

const visible = ref(true)

const toastClass = computed(() => {
  switch (props.type) {
    case 'success':
      return 'bg-success-600 text-white'
    case 'error':
      return 'bg-danger-600 text-white'
    case 'warning':
      return 'bg-warning-600 text-white'
    default:
      return 'bg-primary-600 text-white'
  }
})

const icon = computed(() => {
  switch (props.type) {
    case 'success':
      return '✔️'
    case 'error':
      return '❌'
    case 'warning':
      return '⚠️'
    default:
      return 'ℹ️'
  }
})

const close = () => {
  visible.value = false
}

watch(
  () => props.message,
  () => {
    visible.value = true
    setTimeout(close, props.duration)
  },
  { immediate: true }
)
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style> 