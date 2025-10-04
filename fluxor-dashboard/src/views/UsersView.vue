<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">User Management</h1>
      <p class="text-sm text-gray-600">Manage platform users, roles, and permissions</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">👥</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Total Users</dt>
                <dd class="text-lg font-medium text-gray-900">15,673</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-success-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">✓</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Active Users</dt>
                <dd class="text-lg font-medium text-gray-900">14,892</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-warning-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">⚡</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Online Now</dt>
                <dd class="text-lg font-medium text-gray-900">2,341</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">👑</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Admins</dt>
                <dd class="text-lg font-medium text-gray-900">12</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- User Management Table -->
    <div class="card">
      <div class="card-header">
        <h3 class="text-lg font-medium text-gray-900">Recent Users</h3>
      </div>
      <div class="card-body">
        <div class="text-center py-12">
          <div class="mx-auto h-12 w-12 text-gray-400">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
            </svg>
          </div>
          <h3 class="mt-2 text-sm font-medium text-gray-900">User Management</h3>
          <p class="mt-1 text-sm text-gray-500">
            This feature will be implemented in the next phase. It will include:
          </p>
          <div class="mt-4 text-sm text-gray-500 text-left max-w-md mx-auto">
            <ul class="list-disc list-inside space-y-1">
              <li>User registration and profile management</li>
              <li>Role-based access control (RBAC)</li>
              <li>Permission management</li>
              <li>User activity monitoring</li>
              <li>Account suspension and activation</li>
              <li>Password reset and security settings</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

onMounted(() => {
  console.log('Users view mounted')
})
</script>