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

<template>
  <B24Card variant="outline-alt" class="backdrop-blur-[14px] border-0" :b24ui="b24ui">
    <template #header>
      <div class="w-full flex flex-row items-center justify-between gap-1">
        <div class="flex flex-row items-center justify-start gap-3">
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

          <ProseH1 class="text-label leading-7 font-(--ui-font-weight-semi-bold) mb-0">
            {{ title }}
          </ProseH1>

          <B24Button
            :icon="GoToLIcon"
            :to="to || `https://bitrix24.github.io/b24ui/docs/components/${componentName}/`"
            target="_blank"
            color="air-tertiary"
          />
        </div>
        <div class="flex flex-wrap flex-row items-center justify-end gap-3">
          <slot name="head-trailing" />
        </div>
      </div>
    </template>
    <template #default>
      <slot name="controls" />
    </template>
  </B24Card>
</template>
