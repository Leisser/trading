/**
 * Firebase Authentication Service
 * Handles Google, Apple, Email/Password, and Phone authentication
 */

import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  OAuthProvider,
  signOut,
  onAuthStateChanged,
  sendEmailVerification,
  sendPasswordResetEmail,
  updateProfile,
  User as FirebaseUser,
  AuthError
} from 'firebase/auth'
import { auth } from '@/config/firebase'

// Auth providers
export const googleProvider = new GoogleAuthProvider()
export const appleProvider = new OAuthProvider('apple.com')

// Configure providers
googleProvider.addScope('email')
googleProvider.addScope('profile')

appleProvider.addScope('email')
appleProvider.addScope('name')

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
  /**
   * Sign in with email and password
   */
  async signInWithEmail(email: string, password: string): Promise<AuthResult> {
    try {
      const result = await signInWithEmailAndPassword(auth, email, password)
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
      const result = await createUserWithEmailAndPassword(auth, email, password)

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
      const result = await signInWithPopup(auth, googleProvider)
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
      const result = await signInWithPopup(auth, appleProvider)
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
    await signOut(auth)
  }

  /**
   * Send password reset email
   */
  async sendPasswordReset(email: string): Promise<AuthResult> {
    try {
      await sendPasswordResetEmail(auth, email)
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
  getCurrentUser(): FirebaseUser | null {
    return auth.currentUser
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
    return onAuthStateChanged(auth, (user) => {
      callback(user ? this.formatUser(user) : null)
    })
  }

  /**
   * Format Firebase user to our interface
   */
  private formatUser(user: FirebaseUser): FirebaseAuthUser {
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
  private getErrorMessage(error: AuthError): string {
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
