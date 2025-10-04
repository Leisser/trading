/**
 * Firebase Configuration for Fluxor Trading Platform
 * Handles authentication, analytics, and other Firebase services
 */

import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getAnalytics } from 'firebase/analytics'
import { getFirestore } from 'firebase/firestore'

// Your web app's Firebase configuration
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

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app)

// Initialize Cloud Firestore and get a reference to the service
export const db = getFirestore(app)

// Initialize Analytics (only in production)
export const analytics = typeof window !== 'undefined' && import.meta.env.PROD
  ? getAnalytics(app)
  : null

// Emulator connection can be added here if needed for development

export default app
