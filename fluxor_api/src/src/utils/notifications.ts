import { ref, reactive } from 'vue'

export type NotificationType = 'success' | 'error' | 'warning' | 'info'

export interface Notification {
  id: string
  type: NotificationType
  title: string
  message: string
  duration?: number
  persistent?: boolean
  actions?: Array<{
    label: string
    action: () => void
    style?: 'primary' | 'secondary'
  }>
  createdAt: Date
}

// Global notification state
const notifications = ref<Notification[]>([])

// Generate unique ID
const generateId = () => Math.random().toString(36).substring(2, 15)

// Default durations for different types
const defaultDurations = {
  success: 5000,
  info: 5000,
  warning: 8000,
  error: 0 // Persistent by default
}

export const useNotifications = () => {
  const showNotification = (options: Omit<Notification, 'id' | 'createdAt'>) => {
    const notification: Notification = {
      id: generateId(),
      createdAt: new Date(),
      duration: options.duration ?? defaultDurations[options.type],
      ...options
    }

    notifications.value.push(notification)

    // Auto-remove non-persistent notifications
    if (notification.duration && notification.duration > 0 && !notification.persistent) {
      setTimeout(() => {
        removeNotification(notification.id)
      }, notification.duration)
    }

    return notification.id
  }

  const removeNotification = (id: string) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const clearAllNotifications = () => {
    notifications.value.splice(0, notifications.value.length)
  }

  // Convenience methods
  const showSuccess = (title: string, message: string, options?: Partial<Notification>) => {
    return showNotification({ type: 'success', title, message, ...options })
  }

  const showError = (title: string, message: string, options?: Partial<Notification>) => {
    return showNotification({ type: 'error', title, message, ...options })
  }

  const showWarning = (title: string, message: string, options?: Partial<Notification>) => {
    return showNotification({ type: 'warning', title, message, ...options })
  }

  const showInfo = (title: string, message: string, options?: Partial<Notification>) => {
    return showNotification({ type: 'info', title, message, ...options })
  }

  return {
    notifications: notifications,
    showNotification,
    removeNotification,
    clearAllNotifications,
    showSuccess,
    showError,
    showWarning,
    showInfo
  }
}

// Export the global notifications for use in components
export { notifications }