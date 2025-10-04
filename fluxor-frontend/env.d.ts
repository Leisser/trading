/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Vue 3 composition API types
declare module 'vue' {
  export * from '@vue/runtime-core'
  export * from '@vue/reactivity'
  export * from '@vue/runtime-dom'
}
