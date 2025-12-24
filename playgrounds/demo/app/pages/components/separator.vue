<script setup lang="ts">
import theme from '#build/b24ui/separator'
import Bitrix24Icon from '@bitrix24/b24icons-vue/common-service/Bitrix24Icon'

const sizes = Object.keys(theme.variants.size) as Array<keyof typeof theme.variants.size>
const accents = Object.keys(theme.variants.accent) as Array<keyof typeof theme.variants.accent>
const types = Object.keys(theme.variants.type) as Array<keyof typeof theme.variants.type>
const orientations = Object.keys(theme.variants.orientation) as Array<keyof typeof theme.variants.orientation>

const defaultSize = (theme.defaultVariants?.size ?? sizes[0]) as (typeof sizes)[number]
const defaultAccent = (theme.defaultVariants?.accent ?? accents[0]) as (typeof accents)[number]
const defaultType = (theme.defaultVariants?.type ?? types[0]) as (typeof types)[number]

const attrs = reactive({
  size: [defaultSize],
  accent: [defaultAccent],
  type: [defaultType],
  orientation: [orientations[0]!],
  label: 'Preview',
  useIcon: true,
  useLabel: true
})
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <div class="flex flex-wrap items-center gap-2">
        <B24Select v-model="attrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
        <B24Select v-model="attrs.accent" class="w-44" :items="accents" placeholder="Accent" multiple />
        <B24Select v-model="attrs.type" class="w-32" :items="['solid', 'dashed', 'dotted', 'double']" placeholder="Type" multiple />
        <B24Select v-model="attrs.orientation" class="w-44" :items="['horizontal', 'vertical']" placeholder="Orientation" multiple />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Input v-model="attrs.label" placeholder="Label" />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="attrs.useIcon" label="icon" size="xs" />
        <B24Switch v-model="attrs.useLabel" label="label" size="xs" />
      </div>
    </template>

    <div class="flex items-stretch flex-wrap justify-start gap-2 min-h-0 mb-4">
      <Matrix v-slot="props" :attrs="attrs">
        <B24Card variant="outline-no-accent">
          <template #header>
            <ProseH5 class="mb-0">
              {{ [props?.size, props?.accent, props?.type, props?.orientation].join(' | ') }}
            </ProseH5>
          </template>

          <div class="p-2" :class="[props?.orientation === 'vertical' ? 'h-24 flex items-center' : '']">
            <div class="h-24 flex gap-4 items-center">
              <div class="flex-1 text-center">
                <ProseP>Blog</ProseP>
              </div>

              <B24Separator :avatar="props?.useIcon ? { src: '/b24ui/demo/avatar/assistant.png' } : undefined" v-bind="props" orientation="vertical" :label="props?.useLabel ? props?.label : undefined" />

              <div class="flex-1 text-center">
                <ProseP>Docs</ProseP>
              </div>

              <B24Separator v-bind="props" orientation="vertical" :label="props?.useLabel ? props?.label : undefined">
                <B24Avatar v-if="props?.useIcon" size="sm" src="/b24ui/demo/avatar/employee.png" />
              </B24Separator>

              <div class="flex-1 text-center">
                <ProseP>Source</ProseP>
              </div>
            </div>
            <B24Separator
              v-bind="props"
              :icon="props?.useIcon ? Bitrix24Icon : undefined"
              :label="props?.useLabel ? props?.label : undefined"
            />
          </div>
        </B24Card>
      </Matrix>
    </div>
  </PlaygroundPage>
</template>
