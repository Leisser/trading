/**
 * Simplified Firebase Authentication Service
 * Uses dynamic imports to avoid module resolution issues
 */

export interface FirebaseAuthUser {
  uid: string
  email: string | null
  displayName: string | null
  photoURL: string | null
  emailVerified: boolean
  phoneNumber: string | null
}

export interface AuthResult {
  success: boolean
  user?: FirebaseAuthUser
  error?: string
  idToken?: string
}

class FirebaseAuthService {
  private auth: any = null
  private googleProvider: any = null
  private appleProvider: any = null

  /**
   * Initialize Firebase auth
   */
  private async initializeAuth() {
    if (this.auth) return this.auth

    try {
      // Dynamic imports to avoid module resolution issues
      const { initializeApp } = await import('firebase/app')
      const { getAuth, GoogleAuthProvider, OAuthProvider } = await import('firebase/auth')

      // Firebase configuration
      const firebaseConfig = {
        apiKey: "AIzaSyC2EjPY7nG7uFyu6l2ymNlTGxTecOD69gU",
        authDomain: "fluxor-434ed.firebaseapp.com",
        projectId: "fluxor-434ed",
        storageBucket: "fluxor-434ed.firebasestorage.app",
        messagingSenderId: "665456308175",
        appId: "1:665456308175:web:a990ace4d8dcaf91b62cba",
        measurementId: "G-6Y3S97KP7T"
      }

      // Initialize Firebase
      const app = initializeApp(firebaseConfig)
      this.auth = getAuth(app)

      // Configure providers
      this.googleProvider = new GoogleAuthProvider()
      this.appleProvider = new OAuthProvider('apple.com')

      this.googleProvider.addScope('email')
      this.googleProvider.addScope('profile')

      this.appleProvider.addScope('email')
      this.appleProvider.addScope('name')

      return this.auth
    } catch (error) {
      console.error('Failed to initialize Firebase auth:', error)
      throw error
    }
  }

  /**
   * Sign in with email and password
   */
  async signInWithEmail(email: string, password: string): Promise<AuthResult> {
    try {
      await this.initializeAuth()
      const { signInWithEmailAndPassword } = await import('firebase/auth')

      const result = await signInWithEmailAndPassword(this.auth, email, password)
      const idToken = await result.user.getIdToken()

      return {
        success: true,
        user: this.formatUser(result.user),
        idToken
      }
    } catch (error: any) {
      return {
        success: false,
        error: this.getErrorMessage(error)
      }
    }
  }

  /**
   * Create account with email and password
   */
  async createAccount(email: string, password: string, displayName?: string): Promise<AuthResult> {
    try {
      await this.initializeAuth()
      const { createUserWithEmailAndPassword, updateProfile, sendEmailVerification } = await import('firebase/auth')

      const result = await createUserWithEmailAndPassword(this.auth, email, password)

      // Update display name if provided
      if (displayName) {
        await updateProfile(result.user, { displayName })
      }

      // Send email verification
      await sendEmailVerification(result.user)

      const idToken = await result.user.getIdToken()

      return {
        success: true,
        user: this.formatUser(result.user),
        idToken
      }
    } catch (error: any) {
      return {
        success: false,
        error: this.getErrorMessage(error)
      }
    }
  }

  /**
   * Sign in with Google
   */
  async signInWithGoogle(): Promise<AuthResult> {
    try {
      await this.initializeAuth()
      const { signInWithPopup } = await import('firebase/auth')

      const result = await signInWithPopup(this.auth, this.googleProvider)
      const idToken = await result.user.getIdToken()

      return {
        success: true,
        user: this.formatUser(result.user),
        idToken
      }
    } catch (error: any) {
      return {
        success: false,
        error: this.getErrorMessage(error)
      }
    }
  }

  /**
   * Sign in with Apple
   */
  async signInWithApple(): Promise<AuthResult> {
    try {
      await this.initializeAuth()
      const { signInWithPopup } = await import('firebase/auth')

      const result = await signInWithPopup(this.auth, this.appleProvider)
      const idToken = await result.user.getIdToken()

      return {
        success: true,
        user: this.formatUser(result.user),
        idToken
      }
    } catch (error: any) {
      return {
        success: false,
        error: this.getErrorMessage(error)
      }
    }
  }

  /**
   * Sign out
   */
  async signOut(): Promise<void> {
    try {
      await this.initializeAuth()
      const { signOut } = await import('firebase/auth')
      await signOut(this.auth)
    } catch (error) {
      console.error('Sign out error:', error)
    }
  }

  /**
   * Send password reset email
   */
  async sendPasswordReset(email: string): Promise<AuthResult> {
    try {
      await this.initializeAuth()
      const { sendPasswordResetEmail } = await import('firebase/auth')

      await sendPasswordResetEmail(this.auth, email)
      return {
        success: true
      }
    } catch (error: any) {
      return {
        success: false,
        error: this.getErrorMessage(error)
      }
    }
  }

  /**
   * Get current user
   */
  getCurrentUser(): any {
    return this.auth?.currentUser || null
  }

  /**
   * Get current user ID token
   */
  async getCurrentUserToken(): Promise<string | null> {
    const user = this.getCurrentUser()
    if (user) {
      return await user.getIdToken()
    }
    return null
  }

  /**
   * Listen to auth state changes
   */
  onAuthStateChanged(callback: (user: FirebaseAuthUser | null) => void): () => void {
    if (!this.auth) {
      this.initializeAuth().then(() => {
        const { onAuthStateChanged } = require('firebase/auth')
        return onAuthStateChanged(this.auth, (user: any) => {
          callback(user ? this.formatUser(user) : null)
        })
      })
      return () => {}
    }

    const { onAuthStateChanged } = require('firebase/auth')
    return onAuthStateChanged(this.auth, (user: any) => {
      callback(user ? this.formatUser(user) : null)
    })
  }

  /**
   * Format Firebase user to our interface
   */
  private formatUser(user: any): FirebaseAuthUser {
    return {
      uid: user.uid,
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL,
      emailVerified: user.emailVerified,
      phoneNumber: user.phoneNumber
    }
  }

  /**
   * Get user-friendly error messages
   */
  private getErrorMessage(error: any): string {
    switch (error.code) {
      case 'auth/user-not-found':
        return 'No account found with this email address.'
      case 'auth/wrong-password':
        return 'Incorrect password.'
      case 'auth/email-already-in-use':
        return 'An account already exists with this email address.'
      case 'auth/weak-password':
        return 'Password should be at least 6 characters.'
      case 'auth/invalid-email':
        return 'Invalid email address.'
      case 'auth/user-disabled':
        return 'This account has been disabled.'
      case 'auth/too-many-requests':
        return 'Too many failed attempts. Please try again later.'
      case 'auth/network-request-failed':
        return 'Network error. Please check your connection.'
      case 'auth/popup-closed-by-user':
        return 'Sign-in popup was closed. Please try again.'
      case 'auth/cancelled-popup-request':
        return 'Sign-in popup was cancelled.'
      default:
        return error.message || 'An error occurred during authentication.'
    }
  }
}

export const firebaseAuth = new FirebaseAuthService()
export default firebaseAuth
