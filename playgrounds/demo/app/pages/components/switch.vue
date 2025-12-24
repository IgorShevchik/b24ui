<script setup lang="ts">
import theme from '#build/b24ui/switch'
import CheckIcon from '@bitrix24/b24icons-vue/main/CheckIcon'
import Cross30Icon from '@bitrix24/b24icons-vue/actions/Cross30Icon'
import type { SelectItem } from '@bitrix24/b24ui-nuxt'

const sizes = Object.keys(theme.variants.size) as Array<keyof typeof theme.variants.size>
const colors = Object.keys(theme.variants.color) as Array<keyof typeof theme.variants.color>

const defaultColor = (theme.defaultVariants?.color ?? colors[0]) as (typeof colors)[number]
const defaultSize = (theme.defaultVariants?.size ?? sizes[0]) as (typeof sizes)[number]

const showIcons = ref(false)
const checked = ref(true)

const attrs = reactive({
  color: [defaultColor],
  size: [defaultSize],
  loading: false,
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
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="showIcons" label="Icons" size="xs" />
        <B24Switch v-model="attrs.loading" label="Loading" size="xs" />
        <B24Switch v-model="attrs.disabled" label="Disabled" size="xs" />
        <B24Switch v-model="attrs.required" label="Required" size="xs" />
      </div>
    </template>

    <div class="flex items-stretch flex-wrap justify-start gap-2 min-h-0 mb-4">
      <Matrix v-slot="props" :attrs="attrs">
        <B24Card variant="outline-no-accent" class="w-80">
          <template #header>
            <ProseH5 class="mb-0">
              {{ [props?.size, props?.color].join(' | ') }}
            </ProseH5>
          </template>

          <div class="flex flex-col gap-3">
            <B24Switch
              v-model="checked"
              label="Preview"
              :unchecked-icon="showIcons ? Cross30Icon : undefined"
              :checked-icon="showIcons ? CheckIcon : undefined"
              v-bind="props"
            />
            <B24Switch
              v-model="checked"
              label="With description"
              description="This is a description"
              :unchecked-icon="showIcons ? Cross30Icon : undefined"
              :checked-icon="showIcons ? CheckIcon : undefined"
              v-bind="props"
            />
          </div>
        </B24Card>
      </Matrix>
    </div>
  </PlaygroundPage>
</template>
