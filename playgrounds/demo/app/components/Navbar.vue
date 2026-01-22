<script setup lang="ts">
import type { CardProps } from '@bitrix24/b24ui-nuxt'
import { useRoute, useRouter } from '#imports'
import { upperName } from '../utils'
import ChevronLeftLIcon from '@bitrix24/b24icons-vue/outline/ChevronLeftLIcon'
import ChevronRightLIcon from '@bitrix24/b24icons-vue/outline/ChevronRightLIcon'
import GoToLIcon from '@bitrix24/b24icons-vue/outline/GoToLIcon'

const route = useRoute()
const router = useRouter()

defineProps<{
  to?: string
  b24ui?: CardProps['b24ui']
}>()

defineSlots<{
  controls?: () => any
  trailing?: () => any
}>()

const componentName = computed(() => route.path.split('/').filter(Boolean).pop() ?? '')

const title = computed(() => {
  if (componentName.value.includes('prose')) {
    return 'Prose'
  }
  return upperName(componentName.value)
})

const components = inject<{ to: string, label: string }[]>('components')

const index = computed(() => components?.findIndex(component => component.to === route.path) ?? -1)

function navigate(index: number) {
  router.push(components?.[index]?.to as string)
}

defineShortcuts({
  j: () => navigate(index.value + 1),
  k: () => navigate(index.value - 1)
})
</script>

// TODO: remove duplicate code
<template>
  <Teleport to="header">
    <div class="flex lg:hidden flex-row items-center justify-start absolute top-1/2 -translate-y-1/2 left-14 z-20">
      <B24FieldGroup size="sm">
        <B24Button
          :icon="ChevronLeftLIcon"
          size="sm"
          color="air-secondary-accent"
          :disabled="index === 0"
          @click="navigate(index - 1)"
        />
        <B24Button
          :icon="ChevronRightLIcon"
          color="air-secondary-accent"
          :disabled="index === (components?.length ?? 0) - 1"
          @click="navigate(index + 1)"
        />
      </B24FieldGroup>

      <ProseH1 class="text-label leading-7 font-(--ui-font-weight-semi-bold) mb-0 ml-3 text-(length:--ui-font-size-3xl)">
        {{ title }}
      </ProseH1>

      <B24Button
        :icon="GoToLIcon"
        :to="to || `https://bitrix24.github.io/b24ui/docs/components/${componentName}/`"
        target="_blank"
        color="air-tertiary"
      />
    </div>
  </Teleport>
  <B24Card
    :b24ui="{
      root: 'backdrop-blur-xl border-0 md:sticky top-0 z-10 rounded-none lg:rounded-(--ui-border-radius-md)',
      header: 'p-0 sm:p-0 border-b-0 lg:border-b-1',
      body: 'p-3',
      ...b24ui
    }"
  >
    <template #header>
      <div class="hidden lg:flex flex-row items-center justify-start p-4">
        <B24FieldGroup size="sm">
          <B24Button
            :icon="ChevronLeftLIcon"
            color="air-secondary-accent"
            :disabled="index === 0"
            @click="navigate(index - 1)"
          />
          <B24Button
            :icon="ChevronRightLIcon"
            color="air-secondary-accent"
            :disabled="index === (components?.length ?? 0) - 1"
            @click="navigate(index + 1)"
          />
        </B24FieldGroup>

        <ProseH1 class="text-label leading-7 font-(--ui-font-weight-semi-bold) mb-0 ml-3">
          {{ title }}
        </ProseH1>

        <B24Button
          :icon="GoToLIcon"
          :to="to || `https://bitrix24.github.io/b24ui/docs/components/${componentName}/`"
          target="_blank"
          color="air-tertiary"
        />
      </div>
    </template>
    <template #default>
      <div class="w-full flex flex-row flex-wrap items-center justify-between gap-3">
        <slot name="controls" />
        <div class="flex flex-wrap flex-row items-center justify-end gap-3">
          <slot name="trailing" />
        </div>
      </div>
    </template>
  </B24Card>
</template>
