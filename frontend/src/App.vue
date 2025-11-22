<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <header class="bg-white border-b border-slate-200">
      <div class="mx-auto max-w-6xl px-4 py-4 flex items-center justify-between">
        <h1 class="text-xl font-semibold tracking-tight">REM · KYC Backoffice</h1>
        <nav class="space-x-4 text-sm">
          <RouterLink to="/requests" class="text-slate-600 hover:text-slate-900">
            Solicitudes
          </RouterLink>
          <RouterLink
            to="/requests/new"
            class="inline-flex items-center rounded-md bg-slate-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-slate-800"
          >
            Nueva solicitud
          </RouterLink>
        </nav>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-4 py-6">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>
