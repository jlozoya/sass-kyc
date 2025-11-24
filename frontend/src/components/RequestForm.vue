<template>
  <form class="space-y-4" @submit.prevent="onSubmit">
    <div
      v-if="errors.length"
      class="rounded-md bg-rose-50 p-3 text-sm text-rose-700"
    >
      <p class="mb-1 font-medium">Por favor corrige los siguientes campos:</p>
      <ul class="list-disc list-inside space-y-0.5">
        <li v-for="(err, idx) in errors" :key="idx">{{ err }}</li>
      </ul>
    </div>

    <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
      <div>
        <label class="block text-sm font-medium text-slate-700">
          Nombre completo
        </label>
        <input
          v-model="form.full_name"
          name="full_name"
          type="text"
          class="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-slate-900 focus:ring-slate-900"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700"> Email </label>
        <input
          v-model="form.email"
          name="email"
          type="email"
          class="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-slate-900 focus:ring-slate-900"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700">
          Teléfono
        </label>
        <input
          v-model="form.phone"
          name="phone"
          type="tel"
          class="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-slate-900 focus:ring-slate-900"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700"> País </label>
        <input
          v-model="form.country"
          name="country"
          type="text"
          placeholder="MX, US, etc."
          class="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-slate-900 focus:ring-slate-900"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700">
          Tipo de documento
        </label>
        <select
          v-model="form.document_type"
          name="document_type"
          class="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-slate-900 focus:ring-slate-900"
          required
        >
          <option value="" disabled>Selecciona...</option>
          <option value="INE">INE</option>
          <option value="PASSPORT">Pasaporte</option>
          <option value="DRIVER_LICENSE">Licencia</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700">
          Número de documento
        </label>
        <input
          v-model="form.document_number"
          name="document_number"
          type="text"
          class="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-slate-900 focus:ring-slate-900"
          required
        />
      </div>

      <div class="md:col-span-2 space-y-3">
        <label class="block text-sm font-medium text-slate-700">
          Documento (imagen o archivo)
        </label>

        <div v-if="!form.document_image_url" class="space-y-3">
          <div class="space-y-1">
            <input
              type="file"
              name="document_file"
              :disabled="uploading || submitting"
              accept="image/*,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              class="mt-1 block w-full text-sm text-slate-900 file:mr-4 file:rounded-md file:border-0 file:bg-slate-900 file:px-4 file:py-2 file:text-xs file:font-semibold file:text-white hover:file:bg-slate-800"
              @change="onFileSelected"
            />
            <p class="text-[11px] text-slate-500">
              Puedes subir una foto del documento o un archivo PDF/Word. El archivo
              se sube al backend y se guarda la URL resultante en
              <code>document_image_url</code>.
            </p>
          </div>

          <div class="space-y-1">
            <button
              type="button"
              class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-xs font-medium text-white hover:bg-indigo-700 disabled:opacity-60"
              :disabled="uploading || submitting"
              @click="openCamera"
            >
              Tomar foto con la cámara
            </button>
            <p class="text-[11px] text-slate-500">
              Se abrirá la cámara del dispositivo para capturar una foto del documento y
              subirla automáticamente.
            </p>
          </div>
        </div>

        <div
          v-else
          class="flex items-start justify-between rounded-md border border-slate-200 bg-slate-50 px-3 py-2"
        >
          <div class="space-y-1">
            <p class="text-xs font-medium text-slate-700">
              Documento cargado
            </p>
            <p v-if="fileInfo" class="text-xs text-slate-600">
              <span class="font-medium">{{ fileInfo.filename }}</span>
              <span class="ml-1 text-[11px] font-mono text-slate-500">
                ({{ fileInfo.contentType }})
              </span>
            </p>
            <p v-else class="text-xs text-slate-500">
              Archivo subido correctamente.
            </p>

            <div
              v-if="form.document_image_url"
              class="flex items-center justify-between rounded-md border border-slate-200 bg-slate-50 px-3 py-2"
            >
              <p class="text-xs font-medium text-slate-700">
                Archivo seleccionado:
                <span class="ml-1 font-normal text-slate-600">
                  {{ fileInfo?.filename || 'documento' }}
                </span>
              </p>

              <button
                type="button"
                class="ml-3 inline-flex h-6 w-6 items-center justify-center rounded-full border border-slate-300 text-xs font-bold text-slate-500 hover:bg-slate-100"
                @click="clearDocument"
              >
                ✕
              </button>
            </div>
          </div>

          <button
            type="button"
            class="ml-3 inline-flex h-6 w-6 items-center justify-center rounded-full border border-slate-300 text-xs font-bold text-slate-500 hover:bg-slate-100"
            @click="clearDocument"
          >
            ✕
          </button>
        </div>

        <p v-if="uploading" class="text-xs text-slate-500">
          Subiendo archivo...
        </p>
        <p v-if="uploadError" class="text-xs text-rose-600">
          {{ uploadError }}
        </p>
      </div>
    </div>

    <div class="flex items-center justify-end space-x-3 pt-2">
      <p v-if="submitError" class="mr-auto text-sm text-rose-600">
        {{ submitError }}
      </p>
      <button
        type="submit"
        class="inline-flex items-center rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-60"
        :disabled="submitting || uploading"
      >
        <span v-if="!submitting">Crear solicitud</span>
        <span v-else>Creando...</span>
      </button>
    </div>

    <div
      v-if="isCameraOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
    >
      <div
        class="w-full max-w-md space-y-4 rounded-lg bg-white p-4 shadow-lg"
      >
        <h2 class="text-sm font-semibold text-slate-900">
          Tomar foto del documento
        </h2>

        <video
          ref="videoRef"
          autoplay
          playsinline
          class="w-full rounded-md bg-black"
        ></video>

        <canvas ref="canvasRef" class="hidden"></canvas>

        <div class="flex justify-end gap-2">
          <button
            type="button"
            class="rounded-md border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50"
            @click="closeCamera"
          >
            Cancelar
          </button>
          <button
            type="button"
            class="rounded-md bg-indigo-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-indigo-700"
            @click="captureFromCamera"
          >
            Capturar y subir
          </button>
        </div>
      </div>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref, onBeforeUnmount, nextTick } from 'vue'
import type { CreateRequestPayload } from '../api/requests'
import { uploadFile, type UploadResponse } from '../api/uploads'

const emit = defineEmits<{
  (e: 'submit', payload: CreateRequestPayload): Promise<void> | void
}>()

const form = reactive<CreateRequestPayload>({
  full_name: '',
  email: '',
  phone: '',
  country: '',
  document_type: '',
  document_number: '',
  document_image_url: '',
  original_document_filename: ''
})

const errors = ref<string[]>([])
const submitting = ref(false)
const submitError = ref<string | null>(null)

const uploading = ref(false)
const uploadError = ref<string | null>(null)
const documentPreview = ref<string | null>(null)
const fileInfo = ref<{ filename: string; contentType: string } | null>(null)

const isCameraOpen = ref(false)
const videoRef = ref<HTMLVideoElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
let mediaStream: MediaStream | null = null

function validate(): boolean {
  errors.value = []
  submitError.value = null

  if (!form.full_name.trim()) errors.value.push('El nombre es obligatorio.')
  if (!/^\S+@\S+\.\S+$/.test(form.email))
    errors.value.push('El email no tiene un formato válido.')
  if (form.phone.trim().length < 8)
    errors.value.push('El teléfono debe tener al menos 8 dígitos.')
  if (!form.country.trim()) errors.value.push('El país es obligatorio.')
  if (!form.document_type)
    errors.value.push('El tipo de documento es obligatorio.')
  if (!form.document_number.trim())
    errors.value.push('El número de documento es obligatorio.')

  if (!form.document_image_url.trim()) {
    errors.value.push(
      'Debes subir una imagen o archivo del documento, o tomar una foto.'
    )
  }

  return errors.value.length === 0
}

async function onFileSelected(event: Event) {
  uploadError.value = null
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  try {
    uploading.value = true
    const res: UploadResponse = await uploadFile(file)

    form.document_image_url = res.url
    form.original_document_filename = res.filename
    fileInfo.value = {
      filename: res.filename,
      contentType: res.content_type
    }

    if (res.content_type.startsWith('image/')) {
      documentPreview.value = res.url
    } else {
      documentPreview.value = null
    }
  } catch (err: any) {
    console.error(err)
    uploadError.value = err?.message ?? 'Error al subir el archivo.'
    clearDocument()
  } finally {
    uploading.value = false
  }
}

async function onSubmit() {
  if (!validate()) return

  submitting.value = true
  submitError.value = null

  try {
    await emit('submit', { ...form })
  } catch (err: any) {
    submitError.value = err?.message ?? 'Error al crear la solicitud.'
  } finally {
    submitting.value = false
  }
}

function clearDocument() {
  form.document_image_url = ''
  fileInfo.value = null
  documentPreview.value = null
  uploadError.value = null
}

async function openCamera() {
  uploadError.value = null
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment' },
      audio: false
    })

    isCameraOpen.value = true
    await nextTick()

    if (videoRef.value) {
      videoRef.value.srcObject = mediaStream
      await videoRef.value.play()
    }
  } catch (err) {
    console.error(err)
    uploadError.value =
      'No se pudo acceder a la cámara. Revisa los permisos del navegador.'
    stopCameraStream()
    isCameraOpen.value = false
  }
}

function stopCameraStream() {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
    mediaStream = null
  }
}

function closeCamera() {
  stopCameraStream()
  isCameraOpen.value = false
}

function captureFromCamera() {
  if (!videoRef.value || !canvasRef.value) return

  const video = videoRef.value
  const canvas = canvasRef.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

  canvas.toBlob(async blob => {
    if (!blob) return

    try {
      uploading.value = true

      const file = new File([blob], 'document-camera.jpg', {
        type: 'image/jpeg'
      })

      const res: UploadResponse = await uploadFile(file)

      form.document_image_url = res.url
      form.original_document_filename = res.filename
      fileInfo.value = {
        filename: res.filename,
        contentType: res.content_type
      }

      if (res.content_type.startsWith('image/')) {
        documentPreview.value = res.url
      } else {
        documentPreview.value = null
      }
    } catch (err: any) {
      console.error(err)
      uploadError.value =
        err?.message ?? 'Error al subir la foto capturada.'
      clearDocument()
    } finally {
      uploading.value = false
      closeCamera()
    }
  }, 'image/jpeg', 0.9)
}

onBeforeUnmount(() => {
  stopCameraStream()
})
</script>
