export interface User {
  id: number
  email: string
  full_name: string
  phone_number?: string
  date_of_birth?: string
  address?: string
  is_verified: boolean
  kyc_verified: boolean
  role: 'user' | 'admin'
  date_joined: string
  last_login?: string
  is_banned: boolean
  is_frozen: boolean
  profile?: UserProfile
}

export interface UserProfile {
  avatar?: string
  bio?: string
  website?: string
  location?: string
  timezone: string
  default_currency: string
  notifications_enabled: boolean
  two_factor_enabled: boolean
  two_factor_secret?: string
}

export interface LoginCredentials {
  email: string
  password: string
  two_factor_code?: string
}

export interface RegisterData {
  email: string
  full_name: string
  password: string
  password_confirm: string
  phone_number?: string
}

export interface LoginResponse {
  access: string
  refresh: string
  user: User
}

export interface LoginHistory {
  id: number
  ip_address: string
  user_agent: string
  login_time: string
  success: boolean
  location?: string
  device?: string
}

export interface SecurityOverview {
  two_factor_enabled: boolean
  recent_logins: LoginHistory[]
  active_sessions: number
  security_score: number
}