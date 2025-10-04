<template>
  <router-view />
  <Toast v-if="toastMessage" :message="toastMessage" :type="toastType" :duration="toastDuration" />
</template>

<script setup lang="ts">
import Toast from '@/components/Toast.vue'
import { toastMessage, toastType, toastDuration } from '@/composables/useToast'
</script> 