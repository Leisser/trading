import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, GithubAuthProvider } from 'firebase/auth';
import { getStorage } from 'firebase/storage';
import { getAnalytics } from 'firebase/analytics';

const firebaseConfig = {
  apiKey: "AIzaSyC2EjPY7nG7uFyu6l2ymNlTGxTecOD69gU",
  authDomain: "fluxor-434ed.firebaseapp.com",
  projectId: "fluxor-434ed",
  storageBucket: "fluxor-434ed.firebasestorage.app",
  messagingSenderId: "665456308175",
  appId: "1:665456308175:web:a990ace4d8dcaf91b62cba",
  measurementId: "G-6Y3S97KP7T"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);

// Initialize Firebase Storage
export const storage = getStorage(app);

// Initialize Firebase Analytics (only in browser environment)
export const analytics = typeof window !== 'undefined' ? getAnalytics(app) : null;

// Initialize providers
export const googleProvider = new GoogleAuthProvider();
export const githubProvider = new GithubAuthProvider();

// Configure providers
googleProvider.addScope('email');
googleProvider.addScope('profile');

githubProvider.addScope('user:email');

export default app;
