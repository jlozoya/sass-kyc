<template>
  <section class="max-w-3xl space-y-4">
    <header>
      <h2 class="text-lg font-semibold text-slate-900">Nueva solicitud de verificación</h2>
      <p class="text-sm text-slate-500">
        Completa los datos del usuario para crear una nueva solicitud KYC.
      </p>
    </header>

    <RequestForm @submit="handleSubmit" />

    <p v-if="successMessage" class="text-sm text-emerald-600">
      {{ successMessage }}
    </p>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createRequest, type CreateRequestPayload } from '../api/requests'
import RequestForm from '../components/RequestForm.vue'

const router = useRouter()
const successMessage = ref<string | null>(null)

async function handleSubmit(payload: CreateRequestPayload) {
  const created = await createRequest(payload)
  successMessage.value = 'Solicitud creada correctamente.'
  await router.push({ name: 'requests-detail', params: { id: created.id } })
}
</script>
