<script setup lang="ts">
import theme from '#build/b24ui/radio-group'
import type { SelectItem } from '@bitrix24/b24ui-nuxt'

const sizes = Object.keys(theme.variants.size) as Array<keyof typeof theme.variants.size>
const colors = Object.keys(theme.variants.color) as Array<keyof typeof theme.variants.color>
const variants = Object.keys(theme.variants.variant) as Array<keyof typeof theme.variants.variant>
const indicators = Object.keys(theme.variants.indicator) as Array<keyof typeof theme.variants.indicator>
const orientations = Object.keys(theme.variants.orientation) as Array<keyof typeof theme.variants.orientation>

const isUseBg = ref(true)

const defaultColor = (theme.defaultVariants?.color ?? colors[0]) as (typeof colors)[number]
const defaultSize = (theme.defaultVariants?.size ?? sizes[0]) as (typeof sizes)[number]
const defaultVariant = (theme.defaultVariants?.variant ?? variants[0]) as (typeof variants)[number]
const defaultIndicator = (theme.defaultVariants?.indicator ?? indicators[0]) as (typeof indicators)[number]
const defaultOrientation = (theme.defaultVariants?.orientation ?? orientations[0]) as (typeof orientations)[number]

const attrs = reactive({
  color: [defaultColor],
  size: [defaultSize],
  variant: [defaultVariant],
  indicator: [defaultIndicator],
  orientation: defaultOrientation,
  required: false,
  disabled: false
})

const literalOptions = [
  'Basic',
  'Standard',
  'Professional',
  'Enterprise'
]
const items = [
  { value: '1', label: 'Basic' },
  { value: '2', label: 'Standard' },
  { value: '3', label: 'Professional' },
  { value: '4', label: 'Enterprise' }
]

const itemsWithDescription = [
  { value: '1', label: 'Basic', description: 'includes 5 users' },
  { value: '2', label: 'Standard', description: 'includes 50 users' },
  { value: '3', label: 'Professional', description: 'includes 100 users' },
  { value: '4', label: 'Enterprise', description: 'includes 250 users' }
]

const value = ref<string | undefined>(undefined)

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
        <B24Select v-model="attrs.variant" class="w-32" :items="variants" placeholder="Variant" multiple />
        <B24Select v-model="attrs.indicator" class="w-32" :items="indicators" placeholder="Indicator" multiple />
        <B24Select v-model="attrs.orientation" class="w-32" :items="orientations" placeholder="Orientation" />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="attrs.required" label="Required" size="xs" />
        <B24Switch v-model="attrs.disabled" label="Disabled" size="xs" />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="isUseBg" label="isUseBg" size="xs" />
      </div>
    </template>

    <div class="flex items-stretch flex-wrap justify-start gap-2 min-h-0 mb-4">
      <Matrix v-slot="props" :attrs="attrs">
        <B24Card :variant="isUseBg ? 'outline-no-accent' : 'plain-no-accent'">
          <template #header>
            <ProseH5 class="mb-0">{{ [props?.size, props?.color, props?.variant, props?.indicator].join(' | ') }}</ProseH5>
          </template>

          <div class="mb-4 flex flex-wrap flex-col items-start justify-start gap-4">
            <B24RadioGroup v-model="value" :items="items" default-value="2" v-bind="props" />
            <B24Separator label="Literal options" />
            <B24RadioGroup v-model="value" :items="literalOptions" default-value="Enterprise" v-bind="props" />
            <B24Separator label="Items with description" />
            <B24RadioGroup v-model="value" :items="itemsWithDescription" v-bind="props" />
            <B24Separator label="Legend" />
            <B24RadioGroup v-model="value" legend="Legend" :items="items" v-bind="props" required />
            <B24Separator label="Legend slots" />
            <B24RadioGroup v-model="value" :items="items" v-bind="props">
              <template #legend>
                <span class="italic font-(--ui-font-weight-bold)">
                  Legend slots
                </span>
              </template>
              <template #label="{ item }">
                <span class="italic">
                  {{ item.label }}
                </span>
              </template>
            </B24RadioGroup>
          </div>
        </B24Card>
      </Matrix>
    </div>
  </PlaygroundPage>
</template>
