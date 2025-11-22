import type { RequestStatus, VerificationRequest } from '../types/request'
import { apiFetch } from './client'

export interface CreateRequestPayload {
  full_name: string
  email: string
  phone: string
  country: string
  document_type: string
  document_number: string
  document_image_url: string
}

export function listRequests(params?: { name?: string; status?: RequestStatus | '' }) {
  const search = new URLSearchParams()
  if (params?.name) search.append('name', params.name)
  if (params?.status) search.append('status', params.status)
  const qs = search.toString()
  return apiFetch<VerificationRequest[]>(`/requests${qs ? `?${qs}` : ''}`)
}

export function createRequest(payload: CreateRequestPayload) {
  return apiFetch<VerificationRequest>('/requests', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function getRequest(id: string) {
  return apiFetch<VerificationRequest>(`/requests/${id}`)
}

export function updateRequestStatus(id: string, status: RequestStatus) {
  return apiFetch<VerificationRequest>(`/requests/${id}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status })
  })
}
