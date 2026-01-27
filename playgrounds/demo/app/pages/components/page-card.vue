<script setup lang="ts">
import type { PageCardProps } from '@bitrix24/b24ui-nuxt'
import theme from '#build/b24ui/page-card'
import PaletteIcon from '@bitrix24/b24icons-vue/outline/PaletteIcon'

const colors = Object.keys(theme.variants.highlightColor)
const variants = Object.keys(theme.variants.variant)
const orientations = Object.keys(theme.variants.orientation)

const attrs = reactive({
  variant: [theme.defaultVariants.variant]
})

const highlight = ref(false)
const highlightColor = ref<PageCardProps['highlightColor']>(theme.defaultVariants.highlightColor)

const orientation = ref('vertical' as keyof typeof theme.variants.orientation)
const reverse = ref(false)
</script>

<template>
  <PlaygroundPage :b24ui="{ body: 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5' }">
    <template #controls>
      <B24Select v-model="attrs.variant" class="w-32" :items="variants" multiple placeholder="Variant" />
      <B24Switch v-model="highlight" label="Highlight" size="xs" />
      <B24Select v-model="highlightColor" class="w-44" :items="colors" placeholder="Highlight color" />
      <B24Select v-model="orientation" class="w-44" :items="orientations" placeholder="Orientation" />
      <B24Switch v-model="reverse" label="Reverse" size="xs" />
    </template>

    <Matrix v-slot="props" :attrs="attrs" :b24ui="{ root: 'w-full max-w-[520px]' }">
      <B24PageCard
        :icon="PaletteIcon"
        title="Design system"
        description="Build faster with Bitrix24 UI's CSS-first design system powered by Tailwind CSS and its semantic color system combined with a runtime configuration."
        to="https://bitrix24.github.io/b24ui/docs/getting-started/theme/design-system/"
        target="_blank"
        :highlight="highlight"
        :highlight-color="highlightColor"
        :orientation="orientation"
        :reverse="reverse"
        v-bind="props"
      >
        <Placeholder class="size-full aspect-video" />
      </B24PageCard>
    </Matrix>
  </PlaygroundPage>
</template>
