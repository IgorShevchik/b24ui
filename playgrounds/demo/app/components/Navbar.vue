<script setup lang="ts">
import { useRoute, useRouter } from '#imports'
import { upperName } from '../utils'
import ChevronLeftLIcon from '@bitrix24/b24icons-vue/outline/ChevronLeftLIcon'
import ChevronRightLIcon from '@bitrix24/b24icons-vue/outline/ChevronRightLIcon'
import ExpandIcon from '@bitrix24/b24icons-vue/main/ExpandIcon'

const route = useRoute()
const router = useRouter()

defineProps<{
  to?: string
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
  <div class="base-mode bg-(--ui-color-bg-content-primary) backdrop-blur-sm backdrop-brightness-110 px-[15px] py-xs2 flex flex-col items-start justify-between gap-lg">
    <div class="w-full flex flex-row items-center justify-between gap-lg">
      <div class="flex-1 flex flex-row items-center justify-start gap-sm">
        <B24FieldGroup size="sm">
          <B24Button
            :icon="ChevronLeftLIcon"
            color="air-selection"
            :disabled="index === 0"
            @click="navigate(index - 1)"
          />
          <B24Button
            :icon="ChevronRightLIcon"
            color="air-selection"
            :disabled="index === (components?.length ?? 0) - 1"
            @click="navigate(index + 1)"
          />
        </B24FieldGroup>

        <ProseH1 class="text-label leading-[29px] font-(--ui-font-weight-semi-bold) mb-0">
          {{ title }}
        </ProseH1>

        <slot name="trailing">
          <B24Button
            :icon="ExpandIcon"
            :to="to || `https://bitrix24.github.io/b24ui/docs/components/${componentName}`"
            color="air-tertiary"
            aria-label="Open component in docs"
          />
        </slot>
      </div>
    </div>
    <div>
      <slot name="controls">
        <MockSidebarLayoutMenu orientation="horizontal" />
      </slot>
    </div>
  </div>
</template>
