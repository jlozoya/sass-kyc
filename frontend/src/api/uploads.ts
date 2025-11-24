export interface UploadResponse {
  url: string
  filename: string
  content_type: string
}

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function uploadFile(file: File): Promise<UploadResponse> {
  const form = new FormData()
  form.append('file', file)

  const res = await fetch(`${API_BASE_URL}/uploads/document`, {
    method: 'POST',
    body: form
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || 'Error al subir el archivo')
  }

  return res.json()
}
