s<!-- src/components/RequestForm.vue -->
<template>
  <form class="space-y-4" @submit.prevent="onSubmit">
    <div v-if="errors.length" class="rounded-md bg-rose-50 p-3 text-sm text-rose-700">
      <p class="font-medium mb-1">Por favor corrige los siguientes campos:</p>
      <ul class="list-disc list-inside space-y-0.5">
        <li v-for="(err, idx) in errors" :key="idx">{{ err }}</li>
      </ul>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-slate-700"> Nombre completo </label>
        <input
          v-model="form.full_name"
          name="full_name"
          type="text"
          class="mt-1 block w-full rounded-md border-slate-300 shadow-sm text-sm focus:border-slate-900 focus:ring-slate-900"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700"> Email </label>
        <input
          v-model="form.email"
          name="email"
          type="email"
          class="mt-1 block w-full rounded-md border-slate-300 shadow-sm text-sm focus:border-slate-900 focus:ring-slate-900"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700"> Teléfono </label>
        <input
          v-model="form.phone"
          name="phone"
          type="tel"
          class="mt-1 block w-full rounded-md border-slate-300 shadow-sm text-sm focus:border-slate-900 focus:ring-slate-900"
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
          class="mt-1 block w-full rounded-md border-slate-300 shadow-sm text-sm focus:border-slate-900 focus:ring-slate-900"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700"> Tipo de documento </label>
        <select
          v-model="form.document_type"
          name="document_type"
          class="mt-1 block w-full rounded-md border-slate-300 shadow-sm text-sm focus:border-slate-900 focus:ring-slate-900"
          required
        >
          <option value="" disabled>Selecciona...</option>
          <option value="INE">INE</option>
          <option value="PASSPORT">Pasaporte</option>
          <option value="DRIVER_LICENSE">Licencia</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700"> Número de documento </label>
        <input
          v-model="form.document_number"
          name="document_number"
          type="text"
          class="mt-1 block w-full rounded-md border-slate-300 shadow-sm text-sm focus:border-slate-900 focus:ring-slate-900"
          required
        />
      </div>

      <div class="md:col-span-2">
        <label class="block text-sm font-medium text-slate-700">
          URL de imagen del documento/selfie
        </label>
        <input
          v-model="form.document_image_url"
          name="document_image_url"
          type="url"
          class="mt-1 block w-full rounded-md border-slate-300 shadow-sm text-sm focus:border-slate-900 focus:ring-slate-900"
          required
        />
      </div>
    </div>

    <div class="pt-2 flex items-center justify-end space-x-3">
      <p v-if="submitError" class="text-sm text-rose-600 mr-auto">
        {{ submitError }}
      </p>
      <button
        type="submit"
        class="inline-flex items-center rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-60"
        :disabled="submitting"
      >
        <span v-if="!submitting">Crear solicitud</span>
        <span v-else>Creando...</span>
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import type { CreateRequestPayload } from '../api/requests'

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
  document_image_url: ''
})

const errors = ref<string[]>([])
const submitting = ref(false)
const submitError = ref<string | null>(null)

function validate(): boolean {
  errors.value = []
  submitError.value = null

  if (!form.full_name.trim()) errors.value.push('El nombre es obligatorio.')
  if (!/^\S+@\S+\.\S+$/.test(form.email)) errors.value.push('El email no tiene un formato válido.')
  if (form.phone.trim().length < 8) errors.value.push('El teléfono debe tener al menos 8 dígitos.')
  if (!form.country.trim()) errors.value.push('El país es obligatorio.')
  if (!form.document_type) errors.value.push('El tipo de documento es obligatorio.')
  if (!form.document_number.trim()) errors.value.push('El número de documento es obligatorio.')
  if (!form.document_image_url.trim()) errors.value.push('La URL de la imagen es obligatoria.')

  return errors.value.length === 0
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
</script>
