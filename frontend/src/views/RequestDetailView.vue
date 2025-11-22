<template>
  <section class="space-y-4 max-w-4xl">
    <header class="flex items-center justify-between gap-3">
      <div>
        <h2 class="text-lg font-semibold text-slate-900">Detalle de solicitud</h2>
        <p class="text-sm text-slate-500" v-if="item">{{ item.full_name }} • {{ item.email }}</p>
      </div>
      <RouterLink to="/requests" class="text-sm text-slate-500 hover:text-slate-800">
        ← Volver al listado
      </RouterLink>
    </header>

    <div v-if="loading" class="text-sm text-slate-500">Cargando solicitud...</div>
    <div v-if="error" class="text-sm text-rose-600">
      {{ error }}
    </div>

    <div v-if="item" class="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
      <div class="md:col-span-2 space-y-4">
        <div class="bg-white border border-slate-200 rounded-lg p-4 space-y-3">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-slate-900">Información del usuario</p>
              <p class="text-xs text-slate-500">ID: {{ item.id }}</p>
            </div>
            <StatusBadge :status="item.status" />
          </div>

          <dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-2 text-sm">
            <div>
              <dt class="text-slate-500">Nombre completo</dt>
              <dd class="text-slate-900">{{ item.full_name }}</dd>
            </div>
            <div>
              <dt class="text-slate-500">Email</dt>
              <dd class="text-slate-900">{{ item.email }}</dd>
            </div>
            <div>
              <dt class="text-slate-500">Teléfono</dt>
              <dd class="text-slate-900">{{ item.phone }}</dd>
            </div>
            <div>
              <dt class="text-slate-500">País</dt>
              <dd class="text-slate-900">{{ item.country }}</dd>
            </div>
            <div>
              <dt class="text-slate-500">Tipo de documento</dt>
              <dd class="text-slate-900">{{ item.document_type }}</dd>
            </div>
            <div>
              <dt class="text-slate-500">Número de documento</dt>
              <dd class="text-slate-900">{{ item.document_number }}</dd>
            </div>
            <div class="sm:col-span-2">
              <dt class="text-slate-500">URL de documento/selfie</dt>
              <dd class="text-slate-900 break-all">
                <a
                  :href="item.document_image_url"
                  target="_blank"
                  rel="noreferrer"
                  class="text-sky-600 hover:underline"
                >
                  {{ item.document_image_url }}
                </a>
              </dd>
            </div>
            <div>
              <dt class="text-slate-500">Fecha de creación</dt>
              <dd class="text-slate-900">{{ formatDate(item.created_at) }}</dd>
            </div>
          </dl>
        </div>

        <div class="bg-white border border-slate-200 rounded-lg p-4 space-y-3">
          <p class="text-sm font-medium text-slate-900">Estado de la solicitud</p>
          <div class="flex flex-col sm:flex-row sm:items-center gap-3">
            <select
              v-model="statusToUpdate"
              class="block w-full sm:w-60 rounded-md border-slate-300 shadow-sm text-sm focus:border-slate-900 focus:ring-slate-900"
            >
              <option value="pending">Pendiente</option>
              <option value="approved">Aprobada</option>
              <option value="rejected">Rechazada</option>
              <option value="requires_info">Requiere información</option>
            </select>
            <button
              type="button"
              class="inline-flex items-center rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-60"
              :disabled="statusUpdating"
              @click="onUpdateStatus"
            >
              <span v-if="!statusUpdating">Actualizar estado</span>
              <span v-else>Actualizando...</span>
            </button>
          </div>
          <p v-if="statusError" class="text-sm text-rose-600">
            {{ statusError }}
          </p>
          <p v-if="statusSuccess" class="text-sm text-emerald-600">
            {{ statusSuccess }}
          </p>
        </div>
      </div>

      <div class="space-y-4">
        <div class="bg-white border border-slate-200 rounded-lg p-4 space-y-2">
          <p class="text-sm font-medium text-slate-900">Nivel de riesgo</p>
          <p class="text-3xl font-semibold" :class="riskColorClass">
            {{ riskLabel }}
          </p>
          <p class="text-xs text-slate-500">
            Score: <span class="font-mono">{{ item.risk_score }}</span>
          </p>
          <p class="text-xs text-slate-500">
            Clasificación calculada en backend a partir de reglas simples (dominio de correo, país
            restringido, longitud de documento, etc.).
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { getRequest, updateRequestStatus } from '../api/requests'
import StatusBadge from '../components/StatusBadge.vue'
import type { RequestStatus, VerificationRequest } from '../types/request'

const route = useRoute()

const item = ref<VerificationRequest | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const statusToUpdate = ref<RequestStatus>('pending')
const statusUpdating = ref(false)
const statusError = ref<string | null>(null)
const statusSuccess = ref<string | null>(null)

async function load() {
  loading.value = true
  error.value = null
  statusError.value = null
  statusSuccess.value = null

  try {
    const id = route.params.id as string
    const data = await getRequest(id)
    item.value = data
    statusToUpdate.value = data.status
  } catch (err: any) {
    error.value = err?.message ?? 'No se pudo cargar la solicitud.'
  } finally {
    loading.value = false
  }
}

async function onUpdateStatus() {
  if (!item.value) return

  statusUpdating.value = true
  statusError.value = null
  statusSuccess.value = null

  try {
    const updated = await updateRequestStatus(item.value.id, statusToUpdate.value)
    item.value = updated
    statusSuccess.value = 'Estado actualizado correctamente.'
  } catch (err: any) {
    statusError.value = err?.message ?? 'No se pudo actualizar el estado.'
  } finally {
    statusUpdating.value = false
  }
}

function formatDate(value: string): string {
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return value
  return d.toLocaleString()
}

const riskLabel = computed(() => {
  if (!item.value) return ''
  if (item.value.risk_level === 'low') return 'Bajo'
  if (item.value.risk_level === 'medium') return 'Medio'
  return 'Alto'
})

const riskColorClass = computed(() => {
  if (!item.value) return 'text-slate-900'
  switch (item.value.risk_level) {
    case 'low':
      return 'text-emerald-600'
    case 'medium':
      return 'text-amber-600'
    case 'high':
      return 'text-rose-600'
    default:
      return 'text-slate-900'
  }
})

onMounted(load)
</script>
