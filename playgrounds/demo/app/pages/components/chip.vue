<script setup lang="ts">
import theme from '#build/b24ui/chip'
import BellIcon from '@bitrix24/b24icons-vue/main/BellIcon'
import MailIcon from '@bitrix24/b24icons-vue/main/MailIcon'
import TrendUpIcon from '@bitrix24/b24icons-vue/outline/TrendUpIcon'
import type { SelectItem } from '@bitrix24/b24ui-nuxt'

const colors = Object.keys(theme.variants.color) as Array<keyof typeof theme.variants.color>
const sizes = Object.keys(theme.variants.size) as Array<keyof typeof theme.variants.size>
const positions = Object.keys(theme.variants.position) as Array<keyof typeof theme.variants.position>

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

const defaultColor = (theme.defaultVariants?.color ?? colors[0]) as (typeof colors)[number]
const defaultSize = (theme.defaultVariants?.size ?? sizes[0]) as (typeof sizes)[number]
const defaultPosition = (theme.defaultVariants?.position ?? positions[0]) as (typeof positions)[number]

const attrs = reactive({
  color: [defaultColor],
  size: [defaultSize],
  position: [defaultPosition],
  inset: false,
  inverted: false,
  hideZero: false
})
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <div class="flex flex-wrap items-center gap-2">
        <B24Select v-model="attrs.color" class="w-44" :items="colorItems" placeholder="Color" multiple />
        <B24Select v-model="attrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
        <B24Select v-model="attrs.position" class="w-44" :items="positions" placeholder="Position" multiple />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="attrs.inset" label="Inset" size="xs" />
        <B24Switch v-model="attrs.inverted" label="Inverted" size="xs" />
        <B24Switch v-model="attrs.hideZero" label="Hide zero" size="xs" />
      </div>
    </template>

    <div class="flex items-stretch flex-wrap justify-start gap-2 min-h-0 mb-4">
      <Matrix v-slot="props" :attrs="attrs">
        <B24Card variant="outline-no-accent">
          <template #header>
            <ProseH5 class="mb-0">
              {{ [props?.size, props?.color, props?.position].join(' | ') }}
            </ProseH5>
          </template>

          <div class="flex flex-wrap items-center justify-start gap-4">
            <B24Chip :text="53" :trailing-icon="TrendUpIcon" v-bind="props">
              <B24Button :icon="MailIcon" color="air-secondary-no-accent" />
            </B24Chip>
            <B24Chip :b24ui="{ base: 'style-filled-boost' }" v-bind="props">
              <B24Button :icon="BellIcon" color="air-secondary-no-accent" />
            </B24Chip>
            <B24Chip :text="0" v-bind="props">
              <B24Avatar src="/b24ui/demo/avatar/employee.png" alt="Employee" v-bind="props" />
            </B24Chip>
            <B24Chip :text="1000" v-bind="props">
              <B24Avatar src="/b24ui/demo/avatar/assistant.png" alt="Assistant" v-bind="props" />
            </B24Chip>
          </div>
        </B24Card>
      </Matrix>
    </div>
  </PlaygroundPage>
</template>
