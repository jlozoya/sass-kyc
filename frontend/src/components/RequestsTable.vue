<template>
  <div class="bg-white shadow-sm rounded-lg border border-slate-200">
    <table class="min-w-full divide-y divide-slate-200">
      <thead class="bg-slate-50">
        <tr>
          <th
            scope="col"
            class="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider"
          >
            Nombre
          </th>
          <th
            scope="col"
            class="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider"
          >
            Email
          </th>
          <th
            scope="col"
            class="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider"
          >
            País
          </th>
          <th
            scope="col"
            class="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider"
          >
            Estado
          </th>
          <th
            scope="col"
            class="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider"
          >
            Creado
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-200 bg-white">
        <tr
          v-for="item in items"
          :key="item.id"
          class="cursor-pointer hover:bg-slate-50"
          @click="$emit('row-click', item)"
        >
          <td class="px-4 py-3 text-sm font-medium text-slate-900">
            {{ item.full_name }}
          </td>
          <td class="px-4 py-3 text-sm text-slate-600">
            {{ item.email }}
          </td>
          <td class="px-4 py-3 text-sm text-slate-600">
            {{ item.country }}
          </td>
          <td class="px-4 py-3 text-sm">
            <StatusBadge :status="item.status" />
          </td>
          <td class="px-4 py-3 text-sm text-slate-500">
            {{ formatDate(item.created_at) }}
          </td>
        </tr>

        <tr v-if="!items.length && !loading">
          <td colspan="5" class="px-4 py-6 text-center text-sm text-slate-500">
            No se encontraron solicitudes.
          </td>
        </tr>
      </tbody>
    </table>

    <div
      v-if="loading"
      class="border-t border-slate-100 px-4 py-3 text-sm text-slate-500"
    >
      Cargando solicitudes...
    </div>
    <div
      v-if="error"
      class="border-t border-rose-100 bg-rose-50 px-4 py-3 text-sm text-rose-600"
    >
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import type { VerificationRequest } from '../types/request'
import StatusBadge from './StatusBadge.vue'

defineProps<{
  items: VerificationRequest[]
  loading?: boolean
  error?: string | null
}>()

defineEmits<{
  (e: 'row-click', item: VerificationRequest): void
}>()

function formatDate(value: string): string {
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return value
  return d.toLocaleString()
}
</script>
