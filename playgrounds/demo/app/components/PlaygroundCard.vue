<script setup lang="ts">
import { computed } from 'vue'
import { usePlaygroundContext } from '../composables/usePlaygroundContext'

defineOptions({ inheritAttrs: false })

const { isUseBg } = usePlaygroundContext()

const variant = computed(() => isUseBg.value ? 'outline-no-accent' : 'plain-no-accent')
const offBgClass = computed(() => isUseBg.value ? '' : 'border-(length:--ui-design-outline-na-stroke-weight) border-transparent')
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
