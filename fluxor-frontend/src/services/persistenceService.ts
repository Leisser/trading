/**
 * Enhanced Persistence Service for Firebase Authentication
 * Handles long-term session storage with multiple fallback methods
 */

import { CookieService, IndexedDBService } from './cookieService'

export interface AuthData {
  access: string
  refresh: string
  user?: {
    id: string
    email: string
    full_name: string
    avatar?: string
    role: string
    is_active: boolean
    email_verified: boolean
    phone_number?: string
    created_at: string
    updated_at: string
  }
  firebase_uid?: string
  auth_provider?: string
  expires_at?: number
}

export class PersistenceService {
  private static instance: PersistenceService
  private storageMethod: 'localStorage' | 'indexedDB' | 'cookies' | 'none' = 'none'
  private readonly STORAGE_KEY = 'fluxor_auth_data'
  private readonly COOKIE_ACCESS_KEY = 'fluxor_access_token'
  private readonly COOKIE_REFRESH_KEY = 'fluxor_refresh_token'
  private readonly COOKIE_USER_KEY = 'fluxor_user_data'

  // Long-term storage settings
  private readonly ACCESS_TOKEN_EXPIRY = 24 * 60 * 60 * 1000 // 24 hours
  private readonly REFRESH_TOKEN_EXPIRY = 30 * 24 * 60 * 60 * 1000 // 30 days
  private readonly USER_DATA_EXPIRY = 30 * 24 * 60 * 60 * 1000 // 30 days

  private constructor() {
    this.initializeStorage()
  }

  public static getInstance(): PersistenceService {
    if (!PersistenceService.instance) {
      PersistenceService.instance = new PersistenceService()
    }
    return PersistenceService.instance
  }

  private initializeStorage(): void {
    // Try different storage methods in order of preference
    if (this.supportsLocalStorage()) {
      this.storageMethod = 'localStorage'
    } else if (this.supportsIndexedDB()) {
      this.storageMethod = 'indexedDB'
    } else if (this.supportsCookies()) {
      this.storageMethod = 'cookies'
    } else {
      this.storageMethod = 'none'
    }

    console.log(`Persistence service initialized with: ${this.storageMethod}`)
  }

  private supportsLocalStorage(): boolean {
    try {
      const test = '__fluxor_test__'
      localStorage.setItem(test, test)
      localStorage.removeItem(test)
      return true
    } catch {
      return false
    }
  }

  private supportsIndexedDB(): boolean {
    return 'indexedDB' in window
  }

  private supportsCookies(): boolean {
    return navigator.cookieEnabled
  }

  public getStorageMethod(): string {
    return this.storageMethod
  }

  /**
   * Save authentication data with long-term persistence
   */
  public async saveAuthData(authData: AuthData): Promise<void> {
    try {
      // Add expiration timestamps
      const dataWithExpiry = {
        ...authData,
        expires_at: Date.now() + this.USER_DATA_EXPIRY,
        saved_at: Date.now()
      }

      switch (this.storageMethod) {
        case 'localStorage':
          await this.saveToLocalStorage(dataWithExpiry)
          break
        case 'indexedDB':
          await this.saveToIndexedDB(dataWithExpiry)
          break
        case 'cookies':
          await this.saveToCookies(dataWithExpiry)
          break
        default:
          console.warn('No storage method available')
      }

      // Always save to cookies as backup
      await this.saveToCookies(dataWithExpiry)

      console.log('Auth data saved successfully')
    } catch (error) {
      console.error('Failed to save auth data:', error)
      throw error
    }
  }

  /**
   * Load authentication data with automatic fallback
   */
  public async loadAuthData(): Promise<AuthData | null> {
    try {
      let authData: AuthData | null = null

      // Try primary storage method first
      switch (this.storageMethod) {
        case 'localStorage':
          authData = await this.loadFromLocalStorage()
          break
        case 'indexedDB':
          authData = await this.loadFromIndexedDB()
          break
        case 'cookies':
          authData = await this.loadFromCookies()
          break
      }

      // If primary method fails, try fallback methods
      if (!authData) {
        authData = await this.loadFromCookies()
      }

      if (!authData) {
        authData = await this.loadFromLocalStorage()
      }

      if (!authData) {
        authData = await this.loadFromIndexedDB()
      }

      // Validate expiration
      if (authData && authData.expires_at && Date.now() > authData.expires_at) {
        console.log('Auth data expired, clearing...')
        await this.clearAuthData()
        return null
      }

      return authData
    } catch (error) {
      console.error('Failed to load auth data:', error)
      return null
    }
  }

  /**
   * Clear all authentication data
   */
  public async clearAuthData(): Promise<void> {
    try {
      // Clear from all storage methods
      await Promise.all([
        this.clearLocalStorage(),
        this.clearIndexedDB(),
        this.clearCookies()
      ])

      console.log('Auth data cleared successfully')
    } catch (error) {
      console.error('Failed to clear auth data:', error)
    }
  }

  /**
   * Check if user has valid authentication data
   */
  public async hasValidAuth(): Promise<boolean> {
    const authData = await this.loadAuthData()
    return !!authData && !!authData.access && !!authData.refresh
  }

  // LocalStorage methods
  private async saveToLocalStorage(data: AuthData): Promise<void> {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(data))
  }

  private async loadFromLocalStorage(): Promise<AuthData | null> {
    try {
      const data = localStorage.getItem(this.STORAGE_KEY)
      return data ? JSON.parse(data) : null
    } catch {
      return null
    }
  }

  private async clearLocalStorage(): Promise<void> {
    localStorage.removeItem(this.STORAGE_KEY)
  }

  // IndexedDB methods
  private async saveToIndexedDB(data: AuthData): Promise<void> {
    await IndexedDBService.saveAuthData(data)
  }

  private async loadFromIndexedDB(): Promise<AuthData | null> {
    try {
      return await IndexedDBService.getAuthData()
    } catch {
      return null
    }
  }

  private async clearIndexedDB(): Promise<void> {
    await IndexedDBService.clearAuthData()
  }

  // Cookie methods
  private async saveToCookies(data: AuthData): Promise<void> {
    // Save tokens with appropriate expiry
    CookieService.setCookie(this.COOKIE_ACCESS_KEY, data.access, 1) // 1 day
    CookieService.setCookie(this.COOKIE_REFRESH_KEY, data.refresh, 30) // 30 days

    if (data.user) {
      CookieService.setCookie(this.COOKIE_USER_KEY, JSON.stringify(data.user), 30) // 30 days
    }
  }

  private async loadFromCookies(): Promise<AuthData | null> {
    try {
      const access = CookieService.getCookie(this.COOKIE_ACCESS_KEY)
      const refresh = CookieService.getCookie(this.COOKIE_REFRESH_KEY)
      const userData = CookieService.getCookie(this.COOKIE_USER_KEY)

      if (!access || !refresh) {
        return null
      }

      const authData: AuthData = {
        access,
        refresh
      }

      if (userData) {
        try {
          authData.user = JSON.parse(userData)
        } catch {
          // Ignore invalid user data
        }
      }

      return authData
    } catch {
      return null
    }
  }

  private async clearCookies(): Promise<void> {
    CookieService.deleteCookie(this.COOKIE_ACCESS_KEY)
    CookieService.deleteCookie(this.COOKIE_REFRESH_KEY)
    CookieService.deleteCookie(this.COOKIE_USER_KEY)
  }

  /**
   * Refresh authentication data (update tokens while keeping user data)
   */
  public async refreshAuthData(newTokens: { access: string; refresh: string }): Promise<void> {
    try {
      const existingData = await this.loadAuthData()
      if (existingData) {
        const updatedData: AuthData = {
          ...existingData,
          access: newTokens.access,
          refresh: newTokens.refresh,
          expires_at: Date.now() + this.USER_DATA_EXPIRY,
          saved_at: Date.now()
        }
        await this.saveAuthData(updatedData)
      }
    } catch (error) {
      console.error('Failed to refresh auth data:', error)
    }
  }

  /**
   * Update user data while keeping tokens
   */
  public async updateUserData(userData: AuthData['user']): Promise<void> {
    try {
      const existingData = await this.loadAuthData()
      if (existingData) {
        const updatedData: AuthData = {
          ...existingData,
          user: userData,
          expires_at: Date.now() + this.USER_DATA_EXPIRY,
          saved_at: Date.now()
        }
        await this.saveAuthData(updatedData)
      }
    } catch (error) {
      console.error('Failed to update user data:', error)
    }
  }
}

export default PersistenceService
