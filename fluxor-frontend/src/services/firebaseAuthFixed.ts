/**
 * Fixed Firebase Authentication Service
 * Handles all authentication methods with proper error handling
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
  private isInitialized = false

  /**
   * Initialize Firebase auth with proper error handling
   */
  private async initializeAuth() {
    if (this.isInitialized && this.auth) return this.auth

    try {
      console.log('Initializing Firebase auth...')

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

      // Configure Google provider with proper settings
      this.googleProvider = new GoogleAuthProvider()
      this.googleProvider.addScope('email')
      this.googleProvider.addScope('profile')
      this.googleProvider.setCustomParameters({
        prompt: 'select_account'
      })


      this.isInitialized = true
      console.log('Firebase auth initialized successfully')
      return this.auth
    } catch (error) {
      console.error('Failed to initialize Firebase auth:', error)
      this.isInitialized = false
      throw error
    }
  }

  /**
   * Sign in with email and password
   */
  async signInWithEmail(email: string, password: string): Promise<AuthResult> {
    try {
      console.log('Attempting email sign-in for:', email)
      await this.initializeAuth()

      const { signInWithEmailAndPassword } = await import('firebase/auth')

      const result = await signInWithEmailAndPassword(this.auth, email, password)
      const idToken = await result.user.getIdToken()

      console.log('Email sign-in successful:', result.user.email)

      return {
        success: true,
        user: this.formatUser(result.user),
        idToken
      }
    } catch (error: any) {
      console.error('Email sign-in failed:', error)
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
      console.log('Attempting email sign-up for:', email)
      await this.initializeAuth()

      const { createUserWithEmailAndPassword, updateProfile, sendEmailVerification } = await import('firebase/auth')

      const result = await createUserWithEmailAndPassword(this.auth, email, password)

      // Update display name if provided
      if (displayName) {
        await updateProfile(result.user, { displayName })
      }

      // Send email verification
      try {
        await sendEmailVerification(result.user)
        console.log('Email verification sent')
      } catch (verificationError) {
        console.warn('Failed to send email verification:', verificationError)
        // Don't fail the sign-up if verification fails
      }

      const idToken = await result.user.getIdToken()

      console.log('Email sign-up successful:', result.user.email)

      return {
        success: true,
        user: this.formatUser(result.user),
        idToken
      }
    } catch (error: any) {
      console.error('Email sign-up failed:', error)
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
      console.log('Attempting Google sign-in...')
      await this.initializeAuth()

      const { signInWithPopup } = await import('firebase/auth')

      const result = await signInWithPopup(this.auth, this.googleProvider)
      const idToken = await result.user.getIdToken()

      console.log('Google sign-in successful:', result.user.email)

      return {
        success: true,
        user: this.formatUser(result.user),
        idToken
      }
    } catch (error: any) {
      console.error('Google sign-in failed:', error)
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
      console.log('Signing out...')
      await this.initializeAuth()

      const { signOut } = await import('firebase/auth')
      await signOut(this.auth)

      console.log('Sign out successful')
    } catch (error) {
      console.error('Sign out error:', error)
    }
  }

  /**
   * Send password reset email
   */
  async sendPasswordReset(email: string): Promise<AuthResult> {
    try {
      console.log('Sending password reset for:', email)
      await this.initializeAuth()

      const { sendPasswordResetEmail } = await import('firebase/auth')

      await sendPasswordResetEmail(this.auth, email)

      console.log('Password reset email sent')

      return {
        success: true
      }
    } catch (error: any) {
      console.error('Password reset failed:', error)
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
      try {
        return await user.getIdToken()
      } catch (error) {
        console.error('Failed to get user token:', error)
        return null
      }
    }
    return null
  }

  /**
   * Listen to auth state changes
   */
  onAuthStateChanged(callback: (user: FirebaseAuthUser | null) => void): () => void {
    if (!this.auth) {
      this.initializeAuth().then(() => {
        if (this.auth) {
          const { onAuthStateChanged } = require('firebase/auth')
          return onAuthStateChanged(this.auth, (user: any) => {
            callback(user ? this.formatUser(user) : null)
          })
        }
      }).catch(error => {
        console.error('Failed to initialize auth for state listener:', error)
      })
      return () => {}
    }

    try {
      const { onAuthStateChanged } = require('firebase/auth')
      return onAuthStateChanged(this.auth, (user: any) => {
        callback(user ? this.formatUser(user) : null)
      })
    } catch (error) {
      console.error('Failed to set up auth state listener:', error)
      return () => {}
    }
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
    console.log('Firebase error code:', error.code)

    switch (error.code) {
      case 'auth/user-not-found':
        return 'No account found with this email address. Please sign up first.'
      case 'auth/wrong-password':
        return 'Incorrect password. Please try again.'
      case 'auth/email-already-in-use':
        return 'An account already exists with this email address. Please sign in instead.'
      case 'auth/weak-password':
        return 'Password should be at least 6 characters long.'
      case 'auth/invalid-email':
        return 'Please enter a valid email address.'
      case 'auth/user-disabled':
        return 'This account has been disabled. Please contact support.'
      case 'auth/too-many-requests':
        return 'Too many failed attempts. Please try again later.'
      case 'auth/network-request-failed':
        return 'Network error. Please check your internet connection and try again.'
      case 'auth/popup-closed-by-user':
        return 'Sign-in popup was closed. Please try again.'
      case 'auth/cancelled-popup-request':
        return 'Sign-in popup was cancelled. Please try again.'
      case 'auth/operation-not-allowed':
        return 'This sign-in method is not enabled. Please contact support.'
      case 'auth/requires-recent-login':
        return 'Please sign out and sign in again to complete this action.'
      case 'auth/invalid-credential':
        return 'Invalid credentials. Please check your email and password.'
      case 'auth/account-exists-with-different-credential':
        return 'An account already exists with this email using a different sign-in method.'
      default:
        console.error('Unknown Firebase error:', error)
        return error.message || 'An unexpected error occurred. Please try again.'
    }
  }
}

export const firebaseAuth = new FirebaseAuthService()
export default firebaseAuth
