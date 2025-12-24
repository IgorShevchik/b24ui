<script setup lang="ts">
import { ref } from 'vue'
import theme from '#build/b24ui/range'
import type { SelectItem } from '@bitrix24/b24ui-nuxt'

const sizes = Object.keys(theme.variants.size) as Array<keyof typeof theme.variants.size>
const colors = Object.keys(theme.variants.color) as Array<keyof typeof theme.variants.color>
const orientations = Object.keys(theme.variants.orientation) as Array<keyof typeof theme.variants.orientation>

const value = ref(50)
const value2 = ref([40, 80])
const value22 = ref([40, 80])
const value3 = ref([15, 40, 80])

const isUseBg = ref(true)

const defaultColor = (theme.defaultVariants?.color ?? colors[0]) as (typeof colors)[number]
const defaultSize = (theme.defaultVariants?.size ?? sizes[0]) as (typeof sizes)[number]
const attrs = reactive({
  color: [defaultColor],
  size: [defaultSize],
  orientation: orientations[0],
  inverted: false,
  disabled: false
})

const oldColors = computed(() => {
  return colors.filter((color) => {
    return !color.includes('air')
  })
})

const airColors = computed(() => {
  return colors.filter((color) => {
    return color.includes('air')
  })
})

const colorItems = [
  [...airColors.value],
  [{ label: 'Deprecated', type: 'label' as const }, ...oldColors.value]
] satisfies SelectItem[][]
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <div class="flex flex-wrap items-center gap-2">
        <B24Select v-model="attrs.color" class="w-44" :items="colorItems" placeholder="Color" multiple />
        <B24Select v-model="attrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
        <B24Select v-model="attrs.orientation" class="w-44" :items="['horizontal', 'vertical']" placeholder="Orientation" />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="attrs.inverted" label="Inverted" size="xs" />
        <B24Switch v-model="attrs.disabled" label="Disabled" size="xs" />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="isUseBg" label="isUseBg" size="xs" />
      </div>
    </template>

    <div class="flex items-stretch flex-wrap justify-start gap-2 min-h-0 mb-4">
      <Matrix v-slot="props" :attrs="attrs">
        <B24Card :variant="isUseBg ? 'outline-no-accent' : 'plain-no-accent'">
          <template #header>
            <ProseH5 class="mb-0">
              {{ [props?.size, props?.color].join(' | ') }}
            </ProseH5>
          </template>

          <div class="flex flex-col gap-lg p-2 w-64" :class="[props?.orientation === 'vertical' && 'h-48 flex flex-row w-max gap-8']">
            <B24Range v-model="value" v-bind="props" />
            <B24Range :default-value="80" v-bind="props" />
            <B24Separator label="Multiple" :orientation="props?.orientation" />
            <B24Range :default-value="value2" v-bind="props" />
            <B24Range :model-value="value22" v-bind="props" />
            <B24Range :model-value="value3" v-bind="props" />
            <B24Separator label="Steps" :orientation="props?.orientation" />
            <B24Range :min="4" :max="12" :step="2" :model-value="6" v-bind="props" />
            <B24Range :min-steps-between-thumbs="20" :model-value="value3" v-bind="props" />
          </div>
        </B24Card>
      </Matrix>
    </div>
  </PlaygroundPage>
</template>
