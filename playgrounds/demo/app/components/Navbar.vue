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

const title = computed(() => {
  if (route.path === '/') {
    return ''
  }
  if (route.path.startsWith('/components/prose/')) {
    return 'Prose'
  }
  const lastSegment = route.path.split('/').filter(Boolean).pop()
  return lastSegment ? upperName(lastSegment) : ''
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
  <B24Container class="backdrop-blur-sm backdrop-brightness-110 px-[15px] py-[10px] flex flex-col items-start justify-between gap-[20px]">
    <div class="w-full flex flex-row items-center justify-between gap-[20px]">
      <div class="flex-1 flex flex-row items-center justify-start gap-[12px]">
        <B24FieldGroup size="sm">
          <B24Button
            :icon="ChevronLeftLIcon"
            color="air-selection"
            variant="outline"
            :disabled="index === 0"
            class="ring-default"
            aria-label="Previous component"
            @click="navigate(index - 1)"
          />
          <B24Button
            :icon="ChevronRightLIcon"
            color="air-selection"
            variant="outline"
            :disabled="index === (components?.length ?? 0) - 1"
            class="ring-default"
            aria-label="Next component"
            @click="navigate(index + 1)"
          />
        </B24FieldGroup>

        <ProseH1 class="text-(--b24ui-typography-label-color) leading-[29px] font-(--ui-font-weight-semi-bold) mb-0">
          {{ title }}
        </ProseH1>

        <slot name="trailing">
          <B24Button
            :icon="ExpandIcon"
            :to="to || `https://bitrix24.github.io/b24ui/docs/components/${name}`"
            color="link"
            variant="outline"
            aria-label="Open component in docs"
          />
        </slot>
      </div>
    </div>
    <div>
      <MockSidebarLayoutMenu orientation="horizontal" />
    </div>
  </B24Container>
</template>
