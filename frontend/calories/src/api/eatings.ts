export interface EatingProductData {
  id: number
  mass: number
}

export interface EatingData {
  timestamp: Date
  products: EatingProductData[]
}

export interface EatingProductResponse {
  id: number
  product_id: number
  mass: number
}

export interface EatingResponse {
  id: number
  timestamp: string
  products: EatingProductResponse[]
}

export const saveEating = async (token: string, data: EatingData): Promise<EatingResponse> => {
  const response = await fetch('/api/v1/eatings/', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })

  let responseJson: any = {}

  try {
    responseJson = await response.json()
  } catch {
    throw new Error("Server error")
  }

  if (!response.ok) {
    throw new Error(responseJson.detail)
  }

  return responseJson
}

export const getAllEatings = async (token: string): Promise<EatingResponse[]> => {
  const response = await fetch('/api/v1/eatings/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  const responseJson = await response.json()
  return responseJson
}
