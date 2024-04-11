import type { PaginatedResponse } from "@/utils/types"

export interface ProductResponse {
  id: number
  title: string
  kkal: number
  file_url: string
  mass: number
}

export interface CreateProductData {
  title: string
  image?: File | null
  kkal: number
}

export const searchProducts = async (query: string = '', limit: number = 20): Promise<ProductResponse[]> => {
  const params = { query, limit: `${limit}` }
  const response = await fetch('/api/v1/products/search/' + '?' + new URLSearchParams(params))
  const responseJson = await response.json()
  return responseJson
}

export const getProducts = async ({ page = 1, perPage = 50, ids = null, my = false, token = null }: { page?: number, perPage?: number, ids?: number[] | null, my?: boolean, token?: string | null }): Promise<PaginatedResponse<ProductResponse>> => {
  const params: { page: string, per_page: string, my: string, ids?: string } = {
    page: String(page),
    per_page: String(perPage),
    my: String(my)
  }

  if (ids) params.ids = ids.join(',')

  console.log(params)
  const headers: { Authorization: string } | {} = token ? { "Authorization": `Bearer ${token}` } : {}
  const response = await fetch('/api/v1/products/' + '?' + new URLSearchParams(params), { headers })
  const responseJson = await response.json()
  return responseJson
}

export const createProduct = async (token: string, data: CreateProductData): Promise<ProductResponse> => {
  const formData = new FormData()
  formData.append("title", data.title)
  formData.append("kkal", String(data.kkal))
  if (data.image) {
    formData.append("image", data.image, data.image.name)
  }
  const response = await fetch("/api/v1/products/", {
    headers: { "Authorization": `Bearer ${token}` },
    body: formData,
    method: "POST"
  })
  const responseJson = await response.json()
  return responseJson
}