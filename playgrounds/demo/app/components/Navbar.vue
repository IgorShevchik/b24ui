<script setup lang="ts">
import type { CardProps } from '@bitrix24/b24ui-nuxt'
import { useMediaQuery } from '@vueuse/core'

const isLargeScreen = useMediaQuery('(min-width: 1024px)')

defineProps<{
  b24ui?: CardProps['b24ui']
}>()

const slots = defineSlots<{
  controls?: () => any
  trailing?: () => any
}>()
</script>

<template>
  <Teleport to="body" :disabled="isLargeScreen">
    <NavbarHeader class="lg:hidden absolute top-3 left-14" />
  </Teleport>
  <B24Card
    :b24ui="{
      root: 'backdrop-blur-xl border-0 md:sticky top-0 z-10 rounded-none lg:rounded-(--ui-border-radius-md)',
      header: 'p-0 sm:p-0 border-b-0 lg:border-b-1',
      body: 'w-full flex flex-row flex-wrap items-center justify-between gap-3 py-3',
      ...b24ui
    }"
  >
    <template #header>
      <NavbarHeader class="hidden lg:flex p-4" />
    </template>
    <slot name="controls" />
    <div v-if="slots.trailing" class="flex flex-wrap flex-row items-center justify-end gap-3">
      <slot name="trailing" />
    </div>
  </B24Card>
</template>
