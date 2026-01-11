<script setup lang="ts">
import theme from '#build/b24ui/badge'
import InfoIcon from '@bitrix24/b24icons-vue/button/InfoIcon'
import type { ToastProps } from '@bitrix24/b24ui-nuxt'

const toast = useToast()

const sizes = Object.keys(theme.variants.size)
const colors = Object.keys(theme.variants.color)

const defaultColor = theme.defaultVariants.color
const defaultSize = theme.defaultVariants.size

const attrs = reactive({
  color: [defaultColor],
  size: [defaultSize],
  inverted: false,
  useLink: false,
  useClose: false,
  square: false
})

const airColors = computed(() => {
  return colors.filter((color) => {
    return color.includes('air')
  })
})

function onClick() {
  toast.add({
    title: 'Action',
    description: 'Some action',
    color: 'air-primary' as ToastProps['color']
  })
}

function onCloseClick(event: MouseEvent) {
  const { target } = event
  if (target) {
    const parentNode = (target as HTMLElement).closest('span')
    if (parentNode) {
      parentNode.classList.add('invisible')

      setTimeout(() => {
        parentNode.classList.remove('invisible')
      }, 1000)
    }
  }
}
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <div class="flex flex-wrap items-center gap-2">
        <B24Select v-model="attrs.color" class="w-44" :items="airColors" placeholder="Color" multiple />
        <B24Select v-model="attrs.size" class="w-24" :items="sizes" placeholder="Size" multiple />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="attrs.inverted" label="Inverted" size="xs" />
        <B24Switch v-model="attrs.square" label="Square" size="xs" />
        <B24Switch v-model="attrs.useLink" label="useLink" size="xs" />
        <B24Switch v-model="attrs.useClose" label="useClose" size="xs" />
      </div>
    </template>

    <Matrix v-slot="props" :attrs="attrs">
      <PlaygroundCard>
        <template #header>
          <ProseH5 class="mb-0">
            {{ [props?.color, props?.size].join(' | ') }}
          </ProseH5>
        </template>

        <div class="flex flex-col items-start justify-start gap-3">
          <B24Badge
            label="Badge"
            v-bind="props"
            :on-close-click="onCloseClick"
            @click="onClick"
          />
          <B24Badge
            :label="props?.square ? '' : 'Icon'"
            :icon="InfoIcon"
            v-bind="props"
            :on-close-click="onCloseClick"
          />
          <B24Badge
            label="With avatar"
            v-bind="props"
            :avatar="{ src: '/b24ui/demo/avatar/employee.png', text: 'Employee' }"
            :on-close-click="onCloseClick"
          />
        </div>
      </PlaygroundCard>
    </Matrix>
  </PlaygroundPage>
</template>
