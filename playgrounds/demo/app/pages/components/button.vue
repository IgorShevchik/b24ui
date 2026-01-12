<script setup lang="ts">
import theme from '#build/b24ui/button'
import RocketIcon from '@bitrix24/b24icons-vue/main/RocketIcon'

const colors = Object.keys(theme.variants.color) as Array<keyof typeof theme.variants.color>
const sizes = Object.keys(theme.variants.size) as Array<keyof typeof theme.variants.size>

const airColors = computed(() => {
  return colors.filter((color) => {
    return color.includes('air')
  })
})

const attrs = reactive({
  color: [theme.defaultVariants.color],
  size: [theme.defaultVariants.size],
  useDropdown: false,
  rounded: false,
  loading: false
})

function onClick() {
  return new Promise<void>(res => setTimeout(res, 1000))
}
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Select v-model="attrs.color" class="w-44" :items="airColors" placeholder="Color" multiple />
      <B24Select v-model="attrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
      <B24Separator orientation="vertical" class="h-10" />
      <B24Switch v-model="attrs.useDropdown" label="useDropdown" size="xs" />
      <B24Switch v-model="attrs.rounded" label="Rounded" size="xs" />
      <B24Switch v-model="attrs.loading" label="Loading" size="xs" />
    </template>

    <Matrix v-slot="props" :attrs="attrs">
      <PlaygroundCard>
        <template #header>
          <ProseH5 class="mb-0">
            {{ [props?.color, props?.size].join(' | ') }}
          </ProseH5>
        </template>
        <div class="mb-4 flex flex-col items-start justify-center gap-4">
          <B24Button label="Button" v-bind="props" />
          <B24Button label="Link" to="/" v-bind="props" />
          <B24Button label="Disabled" disabled v-bind="props" />
          <B24Button label="Disabled link" to="#" disabled v-bind="props" />
          <B24Button label="Loading wait" use-wait v-bind="props" />
          <B24Button label="Loading clock" use-clock v-bind="props" />
          <B24Button label="Loading auto" loading-auto v-bind="props" @click="onClick" />
          <B24Button label="Icon Dropdown" :icon="RocketIcon" v-bind="props" use-dropdown />
          <B24Button label="Avatar" :avatar="{ src: '/b24ui/demo/avatar/employee.png' }" v-bind="props" />
          <B24Button label="Icon" :icon="RocketIcon" v-bind="props" square />
        </div>
      </PlaygroundCard>
    </Matrix>
  </PlaygroundPage>
</template>
