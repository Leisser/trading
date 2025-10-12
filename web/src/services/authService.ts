import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signInWithPopup, 
  signOut, 
  User,
  UserCredential 
} from 'firebase/auth';
import { auth, googleProvider, githubProvider } from '@/config/firebase';

export interface UserRegistrationData {
  name: string;
  email: string;
  password: string;
  idFrontImage?: File;
  idBackImage?: File;
  passportImage?: File;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  user?: any;
}

export interface BackendUser {
  id: string;
  email: string;
  name: string;
  isVerified: boolean;
  createdAt: string;
}

class AuthService {
  private baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

  // Firebase Authentication Methods
  async registerWithEmail(data: UserRegistrationData): Promise<UserCredential> {
    try {
      const userCredential = await createUserWithEmailAndPassword(
        auth, 
        data.email, 
        data.password
      );
      
      // Update display name
      if (userCredential.user && 'updateProfile' in userCredential.user) {
        await (userCredential.user as any).updateProfile({
          displayName: data.name
        });
      }

      return userCredential;
    } catch (error: any) {
      throw new Error(this.getFirebaseErrorMessage(error.code));
    }
  }

  async signInWithEmail(email: string, password: string): Promise<UserCredential> {
    try {
      return await signInWithEmailAndPassword(auth, email, password);
    } catch (error: any) {
      throw new Error(this.getFirebaseErrorMessage(error.code));
    }
  }

  async signInWithGoogle(): Promise<UserCredential> {
    try {
      return await signInWithPopup(auth, googleProvider);
    } catch (error: any) {
      throw new Error(this.getFirebaseErrorMessage(error.code));
    }
  }

  async signInWithGithub(): Promise<UserCredential> {
    try {
      return await signInWithPopup(auth, githubProvider);
    } catch (error: any) {
      throw new Error(this.getFirebaseErrorMessage(error.code));
    }
  }

  async signOut(): Promise<void> {
    try {
      await signOut(auth);
    } catch (error: any) {
      throw new Error('Failed to sign out');
    }
  }

  // File Upload Methods
  async uploadIdImage(file: File, type: 'front' | 'back' | 'passport', firebaseToken: string): Promise<number> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('document_type', type);

      const response = await fetch(`${this.baseURL}/upload/kyc/upload/`, {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${firebaseToken}`
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to upload ID image');
      }

      const result = await response.json();
      return result.upload.id; // Return the KYC upload ID
    } catch (error) {
      throw new Error('Failed to upload ID image');
    }
  }

  // Sync Firebase user with backend
  // This is the ONLY method needed - it handles both new and existing users
  async syncFirebaseUser(firebaseUser: User): Promise<AuthTokens> {
    try {
      console.log('Syncing Firebase user:', firebaseUser.email); // Debug log
      
      // Get Firebase ID token
      const idToken = await firebaseUser.getIdToken();
      console.log('Got Firebase ID token'); // Debug log

      // Send token to backend - backend will:
      // 1. Verify token with Firebase Admin SDK
      // 2. Check if user exists by email
      // 3. If exists: return tokens and user details
      // 4. If not: create user and return tokens and user details
      const tokens = await this.convertToken(idToken);
      
      console.log('Received tokens from backend:', tokens); // Debug log
      
      // Store tokens in localStorage
      this.setTokens(tokens);
      
      console.log('Tokens should be stored now'); // Debug log
      
      return tokens;
    } catch (error: any) {
      console.error('syncFirebaseUser error:', error); // Debug log
      throw new Error(error.message || 'Authentication failed');
    }
  }

  async convertToken(firebaseToken: string): Promise<AuthTokens> {
    try {
      const response = await fetch(`${this.baseURL}/convert-token/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          token: firebaseToken
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Authentication failed');
      }

      const data = await response.json();
      
      console.log('Backend response:', data); // Debug log
      
      // Map response to AuthTokens interface
      const tokens = {
        accessToken: data.access_token || '',
        refreshToken: data.refresh_token || '',
        user: data.user || null
      };
      
      console.log('Mapped tokens:', tokens); // Debug log
      
      return tokens;
    } catch (error: any) {
      console.error('Convert token error:', error); // Debug log
      throw new Error(error.message || 'Failed to convert token');
    }
  }

  async refreshToken(refreshToken: string): Promise<AuthTokens> {
    try {
      const response = await fetch(`${this.baseURL}/refresh-token/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          refresh_token: refreshToken
        })
      });

      if (!response.ok) {
        throw new Error('Token refresh failed');
      }

      return await response.json();
    } catch (error: any) {
      throw new Error('Failed to refresh token');
    }
  }

  // Utility Methods
  private getFirebaseErrorMessage(errorCode: string): string {
    switch (errorCode) {
      case 'auth/email-already-in-use':
        return 'This email is already registered';
      case 'auth/weak-password':
        return 'Password should be at least 6 characters';
      case 'auth/invalid-email':
        return 'Invalid email address';
      case 'auth/user-not-found':
        return 'No account found with this email';
      case 'auth/wrong-password':
        return 'Incorrect password';
      case 'auth/too-many-requests':
        return 'Too many failed attempts. Please try again later';
      case 'auth/network-request-failed':
        return 'Network error. Please check your connection';
      default:
        return 'Authentication failed. Please try again';
    }
  }

  // Token Management
  setTokens(tokens: AuthTokens): void {
    console.log('Setting tokens:', tokens); // Debug log
    if (!tokens.accessToken || !tokens.refreshToken) {
      console.error('Invalid tokens provided to setTokens:', tokens);
      return;
    }
    localStorage.setItem('access_token', tokens.accessToken);
    localStorage.setItem('refresh_token', tokens.refreshToken);
    console.log('Tokens stored successfully'); // Debug log
    console.log('Access token:', localStorage.getItem('access_token')); // Verify storage
    
    // Dispatch custom event to notify components that auth state changed
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new Event('authChanged'));
    }
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  clearTokens(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    // Dispatch custom event to notify components that auth state changed
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new Event('authChanged'));
    }
  }

  // API Request Helper
  async makeAuthenticatedRequest(url: string, options: RequestInit = {}): Promise<Response> {
    const accessToken = this.getAccessToken();
    
    if (!accessToken) {
      throw new Error('No access token available');
    }

    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
      ...options.headers
    };

    const response = await fetch(url, {
      ...options,
      headers
    });

    // Handle token refresh if needed
    if (response.status === 401) {
      const refreshToken = this.getRefreshToken();
      if (refreshToken) {
        try {
          const newTokens = await this.refreshToken(refreshToken);
          this.setTokens(newTokens);
          
          // Retry the original request
          return fetch(url, {
            ...options,
            headers: {
              ...headers,
              'Authorization': `Bearer ${newTokens.accessToken}`
            }
          });
        } catch (error) {
          this.clearTokens();
          throw new Error('Session expired. Please sign in again');
        }
      } else {
        this.clearTokens();
        throw new Error('Session expired. Please sign in again');
      }
    }

    return response;
  }
}

export const authService = new AuthService();
export default authService;
