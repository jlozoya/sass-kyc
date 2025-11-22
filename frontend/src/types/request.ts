export type RequestStatus = 'pending' | 'approved' | 'rejected' | 'requires_info'
export type RiskLevel = 'low' | 'medium' | 'high'

export interface VerificationRequest {
  id: string
  full_name: string
  email: string
  phone: string
  country: string
  document_type: string
  document_number: string
  document_image_url: string
  status: RequestStatus
  risk_score: number
  risk_level: RiskLevel
  created_at: string
}
