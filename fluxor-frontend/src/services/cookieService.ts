/**
 * Cookie Service for managing browser cookies
 */
export class CookieService {
  private static readonly COOKIE_PREFIX = 'fluxor_'
  private static readonly DEFAULT_EXPIRY_DAYS = 30

  /**
   * Set a cookie with the given name, value, and options
   */
  static setCookie(
    name: string,
    value: string,
    options: {
      expires?: Date
      maxAge?: number
      path?: string
      domain?: string
      secure?: boolean
      sameSite?: 'strict' | 'lax' | 'none'
    } = {}
  ): void {
    const {
      expires,
      maxAge,
      path = '/',
      domain,
      secure = window.location.protocol === 'https:',
      sameSite = 'lax'
    } = options

    let cookieString = `${this.COOKIE_PREFIX}${name}=${encodeURIComponent(value)}`

    if (expires) {
      cookieString += `; expires=${expires.toUTCString()}`
    } else if (maxAge) {
      cookieString += `; max-age=${maxAge}`
    } else {
      // Default expiry
      const defaultExpiry = new Date()
      defaultExpiry.setDate(defaultExpiry.getDate() + this.DEFAULT_EXPIRY_DAYS)
      cookieString += `; expires=${defaultExpiry.toUTCString()}`
    }

    cookieString += `; path=${path}`
    if (domain) cookieString += `; domain=${domain}`
    if (secure) cookieString += `; secure`
    cookieString += `; samesite=${sameSite}`

    document.cookie = cookieString
  }

  /**
   * Get a cookie value by name
   */
  static getCookie(name: string): string | null {
    const cookieName = `${this.COOKIE_PREFIX}${name}`
    const cookies = document.cookie.split(';')

    for (let cookie of cookies) {
      cookie = cookie.trim()
      if (cookie.startsWith(`${cookieName}=`)) {
        return decodeURIComponent(cookie.substring(cookieName.length + 1))
      }
    }

    return null
  }

  /**
   * Remove a cookie by name
   */
  static removeCookie(name: string, path: string = '/'): void {
    this.setCookie(name, '', {
      expires: new Date(0),
      path
    })
  }

  /**
   * Check if a cookie exists
   */
  static hasCookie(name: string): boolean {
    return this.getCookie(name) !== null
  }

  /**
   * Get all cookies as an object
   */
  static getAllCookies(): Record<string, string> {
    const cookies: Record<string, string> = {}
    const cookieArray = document.cookie.split(';')

    for (let cookie of cookieArray) {
      cookie = cookie.trim()
      if (cookie.startsWith(this.COOKIE_PREFIX)) {
        const [name, value] = cookie.split('=', 2)
        if (name && value) {
          const cleanName = name.substring(this.COOKIE_PREFIX.length)
          cookies[cleanName] = decodeURIComponent(value)
        }
      }
    }

    return cookies
  }

  /**
   * Clear all Fluxor cookies
   */
  static clearAllCookies(): void {
    const cookies = this.getAllCookies()
    Object.keys(cookies).forEach(name => {
      this.removeCookie(name)
    })
  }
}

/**
 * IndexedDB Service for managing browser IndexedDB storage
 */
export class IndexedDBService {
  private static readonly DB_NAME = 'FluxorAuth'
  private static readonly DB_VERSION = 1
  private static readonly STORE_NAME = 'authData'

  /**
   * Open IndexedDB database
   */
  private static async openDB(): Promise<IDBDatabase> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.DB_NAME, this.DB_VERSION)

      request.onerror = () => reject(request.error)
      request.onsuccess = () => resolve(request.result)

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result
        if (!db.objectStoreNames.contains(this.STORE_NAME)) {
          db.createObjectStore(this.STORE_NAME, { keyPath: 'id' })
        }
      }
    })
  }

  /**
   * Store data in IndexedDB
   */
  static async setItem(key: string, value: any): Promise<void> {
    try {
      const db = await this.openDB()
      const transaction = db.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)

      return new Promise((resolve, reject) => {
        const request = store.put({ id: key, data: value, timestamp: Date.now() })
        request.onsuccess = () => resolve()
        request.onerror = () => reject(request.error)
      })
    } catch (error) {
      console.warn('IndexedDB not available:', error)
      throw error
    }
  }

  /**
   * Get data from IndexedDB
   */
  static async getItem(key: string): Promise<any> {
    try {
      const db = await this.openDB()
      const transaction = db.transaction([this.STORE_NAME], 'readonly')
      const store = transaction.objectStore(this.STORE_NAME)

      return new Promise((resolve, reject) => {
        const request = store.get(key)
        request.onsuccess = () => {
          const result = request.result
          resolve(result ? result.data : null)
        }
        request.onerror = () => reject(request.error)
      })
    } catch (error) {
      console.warn('IndexedDB not available:', error)
      return null
    }
  }

  /**
   * Remove data from IndexedDB
   */
  static async removeItem(key: string): Promise<void> {
    try {
      const db = await this.openDB()
      const transaction = db.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)

      return new Promise((resolve, reject) => {
        const request = store.delete(key)
        request.onsuccess = () => resolve()
        request.onerror = () => reject(request.error)
      })
    } catch (error) {
      console.warn('IndexedDB not available:', error)
      throw error
    }
  }

  /**
   * Clear all data from IndexedDB
   */
  static async clear(): Promise<void> {
    try {
      const db = await this.openDB()
      const transaction = db.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)

      return new Promise((resolve, reject) => {
        const request = store.clear()
        request.onsuccess = () => resolve()
        request.onerror = () => reject(request.error)
      })
    } catch (error) {
      console.warn('IndexedDB not available:', error)
      throw error
    }
  }

  /**
   * Check if IndexedDB is available
   */
  static isAvailable(): boolean {
    return typeof indexedDB !== 'undefined'
  }
}
