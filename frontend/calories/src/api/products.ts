export interface ProductResponse {
  id: number
  title: string
  kkal: number
  file_url: string
  mass: number
}

export const searchProducts = async (query: string = '', limit: number = 20): Promise<ProductResponse[]> => {
  const params = { query, limit: `${limit}` }
  const response = await fetch('/api/v1/products/search/' + '?' + new URLSearchParams(params))
  const responseJson = await response.json()
  return responseJson
}

export const getProducts = async (ids: number[] | null): Promise<ProductResponse[]> => {
  if (ids) {
    const params = { ids: ids.join(',') }
    const response = await fetch('/api/v1/products/' + '?' + new URLSearchParams(params))
    const responseJson = await response.json()
    return responseJson
  }

  const response = await fetch('/api/v1/products/')
  const responseJson = await response.json()
  return responseJson
}