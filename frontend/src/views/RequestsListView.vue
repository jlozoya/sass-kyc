<template>
  <section class="space-y-4">
    <header
      class="flex flex-col md:flex-row md:items-center md:justify-between gap-3"
    >
      <div>
        <h2 class="text-lg font-semibold text-slate-900">
          Solicitudes de verificación
        </h2>
        <p class="text-sm text-slate-500">
          Registra y consulta solicitudes de onboarding KYC.
        </p>
      </div>
      <RouterLink
        to="/requests/new"
        class="inline-flex items-center rounded-md bg-slate-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-slate-800"
      >
        Nueva solicitud
      </RouterLink>
    </header>

    <form
      class="bg-white rounded-lg border border-slate-200 p-4 flex flex-col gap-3 md:flex-row md:items-end"
      @submit.prevent="loadRequests"
    >
      <div class="flex-1">
        <label class="block text-xs font-medium text-slate-600">
          Buscar por nombre
        </label>
        <input
          v-model="filters.name"
          type="text"
          class="mt-1 block w-full rounded-md border-slate-300 shadow-sm text-sm focus:border-slate-900 focus:ring-slate-900"
          placeholder="Ej. Juan Pérez"
        />
      </div>
      <div>
        <label class="block text-xs font-medium text-slate-600"> Estado </label>
        <select
          v-model="filters.status"
          class="mt-1 block w-full rounded-md border-slate-300 shadow-sm text-sm focus:border-slate-900 focus:ring-slate-900"
        >
          <option value="">Todos</option>
          <option value="pending">Pendiente</option>
          <option value="approved">Aprobada</option>
          <option value="rejected">Rechazada</option>
          <option value="requires_info">Requiere información</option>
        </select>
      </div>
      <button
        type="submit"
        class="inline-flex items-center rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800"
      >
        Aplicar filtros
      </button>
    </form>

    <RequestsTable
      :items="items"
      :loading="loading"
      :error="error"
      @row-click="goToDetail"
    />
  </section>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { listRequests } from '../api/requests'
import RequestsTable from '../components/RequestsTable.vue'
import type { RequestStatus, VerificationRequest } from '../types/request'

const router = useRouter()

const items = ref<VerificationRequest[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const filters = reactive<{
  name: string
  status: '' | RequestStatus
}>({
  name: '',
  status: ''
})

const isCameraOpen = ref(false)
let mediaStream: MediaStream | null = null

function closeCamera() {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
    mediaStream = null
  }
  isCameraOpen.value = false
}

onBeforeUnmount(() => {
  closeCamera()
})

async function loadRequests() {
  loading.value = true
  error.value = null

  try {
    items.value = await listRequests({
      name: filters.name || undefined,
      status: filters.status || undefined
    })
  } catch (err: any) {
    error.value = err?.message ?? 'Error al cargar las solicitudes.'
  } finally {
    loading.value = false
  }
}

function goToDetail(item: VerificationRequest) {
  router.push({ name: 'requests-detail', params: { id: item.id } })
}

onMounted(loadRequests)
</script>
