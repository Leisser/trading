import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export const toastMessage = ref<string | null>(null)
export const toastType = ref<ToastType>('info')
export const toastDuration = ref(3000)

export function useToast() {
  function showToast(message: string, type: ToastType = 'info', duration = 3000) {
    toastMessage.value = message
    toastType.value = type
    toastDuration.value = duration
  }
  return { showToast }
} 