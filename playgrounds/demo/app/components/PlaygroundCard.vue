<script setup lang="ts">
import type theme from '#build/b24ui/card'
import { computed } from 'vue'
import { usePlaygroundContext } from '../composables/usePlaygroundContext'

defineOptions({ inheritAttrs: false })

const props = withDefaults(defineProps<{
  onBgVariant?: keyof typeof theme.variants.variant
  offBgVariant?: keyof typeof theme.variants.variant
  applyOffBgBorderFix?: boolean
}>(), {
  onBgVariant: 'outline-no-accent',
  offBgVariant: 'plain-no-accent',
  applyOffBgBorderFix: true
})

const { isUseBg } = usePlaygroundContext()

const variant = computed(() => (isUseBg.value ? props.onBgVariant : props.offBgVariant))
const offBgClass = computed(() => {
  if (isUseBg.value || !props.applyOffBgBorderFix) {
    return undefined
  }
  return 'border-(length:--ui-design-outline-na-stroke-weight) border-transparent'
})
</script>

<template>
  <B24Card v-bind="$attrs" :variant="variant" :class="[$attrs.class, offBgClass]">
    <template v-if="$slots.header" #header>
      <slot name="header" />
    </template>

    <slot />

    <template v-if="$slots.footer" #footer>
      <slot name="footer" />
    </template>
  </B24Card>
</template>
