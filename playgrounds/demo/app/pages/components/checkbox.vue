<script setup lang="ts">
import theme from '#build/b24ui/checkbox'
import type { SelectItem } from '@bitrix24/b24ui-nuxt'

const sizes = Object.keys(theme.variants.size) as Array<keyof typeof theme.variants.size>
const colors = Object.keys(theme.variants.color) as Array<keyof typeof theme.variants.color>
const variants = Object.keys(theme.variants.variant) as Array<keyof typeof theme.variants.variant>
const indicators = Object.keys(theme.variants.indicator) as Array<keyof typeof theme.variants.indicator>

const checked = ref(true)
const isUseBg = ref(true)

const defaultColor = (theme.defaultVariants?.color ?? colors[0]) as (typeof colors)[number]
const defaultSize = (theme.defaultVariants?.size ?? sizes[0]) as (typeof sizes)[number]
const defaultVariant = (theme.defaultVariants?.variant ?? variants[0]) as (typeof variants)[number]
const defaultIndicator = (theme.defaultVariants?.indicator ?? indicators[0]) as (typeof indicators)[number]

const attrs = reactive({
  color: [defaultColor],
  size: [defaultSize],
  variant: [defaultVariant],
  indicator: [defaultIndicator],
  disabled: false,
  required: false
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
        <B24Select v-model="attrs.variant" class="w-40" :items="variants" placeholder="Variant" multiple />
        <B24Select v-model="attrs.indicator" class="w-44" :items="indicators" placeholder="Indicator" multiple />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="attrs.disabled" label="Disabled" size="xs" />
        <B24Switch v-model="attrs.required" label="Required" size="xs" />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="checked" label="Checked" size="xs" />
        <B24Switch v-model="isUseBg" label="isUseBg" size="xs" />
      </div>
    </template>

    <div class="flex flex-wrap justify-start items-stretch gap-2 min-h-0">
      <Matrix v-slot="props" :attrs="attrs">
        <B24Card :variant="isUseBg ? 'outline-no-accent' : 'plain-no-accent'">
          <template #header>
            <ProseH5 class="mb-0">
              {{ [props?.size, props?.color, props?.variant, props?.indicator].join(' | ') }}
            </ProseH5>
          </template>

          <div class="flex flex-col items-start justify-start gap-3">
            <B24Checkbox
              v-model="checked"
              label="Check me"
              name="matrix"
              v-bind="props"
            />
            <B24Checkbox
              v-model="checked"
              label="With description"
              description="This is a description"
              name="matrix_desc"
              v-bind="props"
            />
          </div>
        </B24Card>
      </Matrix>
    </div>
  </PlaygroundPage>
</template>
