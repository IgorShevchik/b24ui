<script setup lang="ts">
import theme from '#build/b24ui/separator'
import Bitrix24Icon from '@bitrix24/b24icons-vue/common-service/Bitrix24Icon'

const sizes = Object.keys(theme.variants.size)
const accents = Object.keys(theme.variants.accent)
const types = Object.keys(theme.variants.type)

const defaultSize = theme.defaultVariants?.size
const defaultAccent = theme.defaultVariants?.accent
const defaultType = theme.defaultVariants?.type

const attrs = reactive({
  size: [defaultSize],
  accent: [defaultAccent],
  type: [defaultType],
  label: 'Preview',
  useIcon: true,
  useLabel: true
})
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Select v-model="attrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
      <B24Select v-model="attrs.accent" class="w-44" :items="accents" placeholder="Accent" multiple />
      <B24Select v-model="attrs.type" class="w-32" :items="types" placeholder="Type" multiple />
      <B24Separator orientation="vertical" class="h-10" />
      <B24Input v-model="attrs.label" placeholder="Label" />
      <B24Separator orientation="vertical" class="h-10" />
      <B24Switch v-model="attrs.useIcon" label="icon" size="xs" />
      <B24Switch v-model="attrs.useLabel" label="label" size="xs" />
    </template>

    <Matrix v-slot="props" :attrs="attrs">
      <PlaygroundCard>
        <template #header>
          <ProseH5 class="mb-0">
            {{ [props?.size, props?.accent, props?.type].join(' | ') }}
          </ProseH5>
        </template>

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
      </PlaygroundCard>
    </Matrix>
  </PlaygroundPage>
</template>
