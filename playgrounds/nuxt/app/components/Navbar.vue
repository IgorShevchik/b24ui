<script setup lang="ts">
import type { CardProps } from '@bitrix24/b24ui-nuxt'
import { useMediaQuery } from '@vueuse/core'

const isLargeScreen = useMediaQuery('(min-width: 1024px)')

defineProps<{
  to?: string
  b24ui?: CardProps['b24ui']
}>()

const slots = defineSlots<{
  controls?: () => any
  trailing?: () => any
}>()

const hasTrailingInBody = computed(() => slots.trailing && !isLargeScreen.value)
const hasBodyContent = computed(() => slots.controls || hasTrailingInBody.value)
</script>

<template>
  <!-- <ClientOnly> -->
  <Teleport to="body" :disabled="isLargeScreen">
    <NavbarHeader :to="to" class="lg:hidden absolute top-3 left-14 z-2" />
  </Teleport>
  <!-- </ClientOnly> -->
  <B24Card
    :b24ui="{
      root: ['backdrop-blur-xl border-0 sm:sticky top-0 z-10 rounded-none lg:rounded-(--ui-border-radius-md)', b24ui?.root],
      header: ['flex items-center justify-between', b24ui?.header],
      body: ['w-full flex flex-row flex-wrap items-center justify-between gap-3 py-3', b24ui?.body]
    }"
  >
    <template v-if="isLargeScreen" #header>
      <NavbarHeader :to="to" class="hidden lg:flex" />
      <div v-if="slots.trailing" class="flex flex-wrap flex-row items-center justify-end gap-3">
        <slot name="trailing" />
      </div>
    </template>
    <template v-if="hasBodyContent" #default>
      <slot name="controls" />
      <div v-if="hasTrailingInBody" class="flex flex-wrap flex-row items-center justify-end gap-3">
        <slot name="trailing" />
      </div>
    </template>
  </B24Card>
</template>
