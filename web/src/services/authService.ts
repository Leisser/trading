import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signInWithPopup, 
  signOut, 
  User,
  UserCredential 
} from 'firebase/auth';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { auth, googleProvider, githubProvider, storage } from '@/config/firebase';

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
}

export interface BackendUser {
  id: string;
  email: string;
  name: string;
  isVerified: boolean;
  createdAt: string;
}

class AuthService {
  private baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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
  async uploadIdImage(file: File, userId: string, type: 'front' | 'back' | 'passport'): Promise<string> {
    try {
      const fileName = `${type}_${Date.now()}_${file.name}`;
      const storageRef = ref(storage, `id-verification/${userId}/${fileName}`);
      
      const snapshot = await uploadBytes(storageRef, file);
      const downloadURL = await getDownloadURL(snapshot.ref);
      
      return downloadURL;
    } catch (error) {
      throw new Error('Failed to upload ID image');
    }
  }

  // Backend API Methods
  async registerUser(userData: UserRegistrationData, firebaseUser: User): Promise<BackendUser> {
    try {
      let idImages: { front?: string; back?: string; passport?: string } = {};

      // Upload ID images if provided
      if (userData.idFrontImage) {
        idImages.front = await this.uploadIdImage(userData.idFrontImage, firebaseUser.uid, 'front');
      }
      if (userData.idBackImage) {
        idImages.back = await this.uploadIdImage(userData.idBackImage, firebaseUser.uid, 'back');
      }
      if (userData.passportImage) {
        idImages.passport = await this.uploadIdImage(userData.passportImage, firebaseUser.uid, 'passport');
      }

      // Get Firebase ID token
      const idToken = await firebaseUser.getIdToken();

      const response = await fetch(`${this.baseURL}/api/register/firebase/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`
        },
        body: JSON.stringify({
          name: userData.name,
          email: userData.email,
          firebase_uid: firebaseUser.uid,
          id_images: idImages
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Registration failed');
      }

      return await response.json();
    } catch (error: any) {
      throw new Error(error.message || 'Failed to register user');
    }
  }

  async convertToken(firebaseToken: string): Promise<AuthTokens> {
    try {
      const response = await fetch(`${this.baseURL}/api/auth/convert-token/`, {
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
        throw new Error(errorData.message || 'Token conversion failed');
      }

      return await response.json();
    } catch (error: any) {
      throw new Error(error.message || 'Failed to convert token');
    }
  }

  async refreshToken(refreshToken: string): Promise<AuthTokens> {
    try {
      const response = await fetch(`${this.baseURL}/api/auth/refresh-token/`, {
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
    localStorage.setItem('access_token', tokens.accessToken);
    localStorage.setItem('refresh_token', tokens.refreshToken);
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
