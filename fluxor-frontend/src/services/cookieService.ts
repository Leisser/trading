// Cookie service for secure authentication token storage
export class CookieService {
  // Set a cookie with secure options
  static setCookie(name: string, value: string, days: number = 30): void {
    const expires = new Date()
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000)

    const cookieOptions = [
      `${name}=${value}`,
      `expires=${expires.toUTCString()}`,
      'path=/',
      'SameSite=Strict',
      'Secure', // Only works with HTTPS
    ].join('; ')

    document.cookie = cookieOptions
  }

  // Get a cookie value
  static getCookie(name: string): string | null {
    const nameEQ = name + '='
    const ca = document.cookie.split(';')

    for (let i = 0; i < ca.length; i++) {
      let c = ca[i]
      while (c.charAt(0) === ' ') c = c.substring(1, c.length)
      if (c.indexOf(nameEQ) === 0) {
        return c.substring(nameEQ.length, c.length)
      }
    }
    return null
  }

  // Delete a cookie
  static deleteCookie(name: string): void {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`
  }

  // Set authentication tokens
  static setAuthTokens(accessToken: string, refreshToken: string): void {
    this.setCookie('access_token', accessToken, 1) // 1 day
    this.setCookie('refresh_token', refreshToken, 30) // 30 days
  }

  // Get authentication tokens
  static getAuthTokens(): { access: string | null; refresh: string | null } {
    return {
      access: this.getCookie('access_token'),
      refresh: this.getCookie('refresh_token'),
    }
  }

  // Clear authentication tokens
  static clearAuthTokens(): void {
    this.deleteCookie('access_token')
    this.deleteCookie('refresh_token')
  }

  // Check if user is authenticated
  static isAuthenticated(): boolean {
    return !!this.getCookie('access_token')
  }
}

// Alternative: IndexedDB for complex data storage
export class IndexedDBService {
  private static dbName = 'FluxorAuthDB'
  private static dbVersion = 1
  private static storeName = 'auth'

  static async initDB(): Promise<IDBDatabase> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.dbVersion)

      request.onerror = () => reject(request.error)
      request.onsuccess = () => resolve(request.result)

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: 'id' })
        }
      }
    })
  }

  static async saveAuthData(data: any): Promise<void> {
    const db = await this.initDB()
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([this.storeName], 'readwrite')
      const store = transaction.objectStore(this.storeName)
      const request = store.put({ id: 'auth', ...data })

      request.onerror = () => reject(request.error)
      request.onsuccess = () => resolve()
    })
  }

  static async getAuthData(): Promise<any> {
    const db = await this.initDB()
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([this.storeName], 'readonly')
      const store = transaction.objectStore(this.storeName)
      const request = store.get('auth')

      request.onerror = () => reject(request.error)
      request.onsuccess = () => resolve(request.result)
    })
  }

  static async clearAuthData(): Promise<void> {
    const db = await this.initDB()
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([this.storeName], 'readwrite')
      const store = transaction.objectStore(this.storeName)
      const request = store.delete('auth')

      request.onerror = () => reject(request.error)
      request.onsuccess = () => resolve()
    })
  }
}

// Service Worker for offline authentication
export class ServiceWorkerAuth {
  static async register(): Promise<void> {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.register('/sw-auth.js')
        console.log('Service Worker registered:', registration)
      } catch (error) {
        console.error('Service Worker registration failed:', error)
      }
    }
  }

  static async cacheAuthData(data: any): Promise<void> {
    if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage({
        type: 'CACHE_AUTH',
        data,
      })
    }
  }

  static async getCachedAuthData(): Promise<any> {
    if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
      return new Promise((resolve) => {
        const messageChannel = new MessageChannel()
        messageChannel.port1.onmessage = (event) => {
          resolve(event.data)
        }

        navigator.serviceWorker.controller.postMessage(
          {
            type: 'GET_CACHED_AUTH',
          },
          [messageChannel.port2],
        )
      })
    }
    return null
  }
}
