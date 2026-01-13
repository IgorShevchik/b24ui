<script setup lang="ts">
import theme from '#build/b24ui/badge'
import InfoIcon from '@bitrix24/b24icons-vue/button/InfoIcon'
import type { ToastProps } from '@bitrix24/b24ui-nuxt'

const toast = useToast()

const sizes = Object.keys(theme.variants.size)
const colors = Object.keys(theme.variants.color)

const attrs = reactive({
  color: [theme.defaultVariants.color],
  size: [theme.defaultVariants.size],
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
      <B24Select v-model="attrs.color" class="w-44" :items="airColors" placeholder="Color" multiple />
      <B24Select v-model="attrs.size" class="w-24" :items="sizes" placeholder="Size" multiple />
      <B24Separator orientation="vertical" class="h-10" />
      <B24Switch v-model="attrs.inverted" label="Inverted" size="xs" />
      <B24Switch v-model="attrs.square" label="Square" size="xs" />
      <B24Switch v-model="attrs.useLink" label="useLink" size="xs" />
      <B24Switch v-model="attrs.useClose" label="useClose" size="xs" />
    </template>

    <Matrix v-slot="props" :attrs="attrs">
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
    </Matrix>
  </PlaygroundPage>
</template>
