export interface PaginatedResponse<Type> {
    page: number
    per_page: number
    pages_count: number
    total: number
    data: Type[]
}