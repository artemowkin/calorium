export interface Tokens {
  access_token: string
  refresh_token: string
}

export interface UserResponse {
  id: number
  email: string
  age: number | null
  height: number | null
  weight: number | null
  sex: 'male' | 'female' | null
  activity: 'lowest' | 'low' | 'middle' | 'high' | 'highest' | null
}

export const sendVerificationCode = async (email: string) => {
  const response = await fetch('/api/v1/auth/send_code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  })

  if (!response.ok) {
    const responseJson = await response.json()
    throw new Error(responseJson.detail ?? "Server error")
  }
}

export const validateVerificationCode = async (email: string, code: string): Promise<Tokens> => {
  const response = await fetch('/api/v1/auth/validate_code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, code })
  })

  const responseJson = await response.json()

  if (!response.ok) {
    throw new Error(responseJson.detail ?? "Server error")
  }

  return responseJson
}

export const getMe = async (token: string): Promise<UserResponse> => {
  const response = await fetch('/api/v1/auth/me', {
    headers: { Authorization: `Bearer ${token}` }
  })

  const responseJson = await response.json()
  return responseJson
}

export type UpdateData = {
  age: number,
  height: number,
  weight: number,
  sex: 'male' | 'female'
  activity: 'lowest' | 'low' | 'middle' | 'high' | 'highest'
}

export const updateMe = async (token: string, updateData: UpdateData): Promise<UserResponse> => {
  const response = await fetch('/api/v1/auth/me', {
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(updateData),
    method: 'PUT',
  })

  const responseJson = await response.json()

  if (!response.ok) {
    throw new Error(responseJson.detail ?? "Server error")
  }

  return responseJson
}

export const refresh = async (refreshToken: string): Promise<Tokens> => {
  const response = await fetch('/api/v1/auth/refresh', {
    headers: { Authorization: `Bearer ${refreshToken}` },
    method: "POST",
  })
  const responseJson = await response.json()

  if (!response.ok) {
    throw new Error(responseJson.detail ?? "Server error")
  }

  return responseJson
}