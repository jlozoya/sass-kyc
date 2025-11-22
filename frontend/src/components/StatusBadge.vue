<template>
  <span
    :class="[
      'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
      colorClasses
    ]"
  >
    <span class="h-1.5 w-1.5 rounded-full mr-1.5" :class="dotClasses" />
    {{ label }}
  </span>
</template>

<script setup lang="ts">
import type { RequestStatus } from '../types/request'

const props = defineProps<{
  status: RequestStatus
}>()

const labelMap: Record<RequestStatus, string> = {
  pending: 'Pendiente',
  approved: 'Aprobada',
  rejected: 'Rechazada',
  requires_info: 'Requiere información'
}

const colorMap: Record<RequestStatus, string> = {
  pending: 'bg-amber-50 text-amber-800',
  approved: 'bg-emerald-50 text-emerald-800',
  rejected: 'bg-rose-50 text-rose-800',
  requires_info: 'bg-sky-50 text-sky-800'
}

const dotMap: Record<RequestStatus, string> = {
  pending: 'bg-amber-500',
  approved: 'bg-emerald-500',
  rejected: 'bg-rose-500',
  requires_info: 'bg-sky-500'
}

const label = labelMap[props.status]
const colorClasses = colorMap[props.status]
const dotClasses = dotMap[props.status]
</script>
