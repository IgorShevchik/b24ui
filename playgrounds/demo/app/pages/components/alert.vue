<script setup lang="ts">
import type { ButtonProps } from '@bitrix24/b24ui-nuxt'
import theme from '#build/b24ui/alert'
import SignIcon from '@bitrix24/b24icons-vue/main/SignIcon'
import MoreMIcon from '@bitrix24/b24icons-vue/outline/MoreMIcon'

const colors = Object.keys(theme.variants.color)
const sizes = Object.keys(theme.variants.size)

const attrs = reactive({
  color: [theme.defaultVariants.color],
  size: [theme.defaultVariants.size],
  inverted: false
})

const airColors = computed(() => {
  return colors.filter((color) => {
    return color.includes('air')
  })
})

const data = {
  title: 'Heads up!',
  description: 'Let\'s signal the manager that the deal is not moving, the manager does not call the client back and does not respond to his messages. Let\'s assign a task to the manager on behalf of the manager.',
  icon: SignIcon,
  close: true
}

const action = () => [
  {
    icon: MoreMIcon,
    color: 'air-secondary-no-accent' as ButtonProps['color'],
    onClick() {
      console.log('Action 3 clicked')
    }
  }
]

const multipleActions = () => [
  {
    label: 'Action',
    color: 'air-primary' as ButtonProps['color'],
    onClick() {
      console.log('Action clicked')
    }
  },
  {
    label: 'Another action',
    color: 'air-primary-success' as ButtonProps['color'],
    onClick() {
      console.log('Another action clicked')
    }
  },
  {
    label: 'One more action',
    color: 'air-secondary-accent-1' as ButtonProps['color'],
    onClick() {
      console.log('One more action clicked')
    }
  },
  {
    label: 'And one more',
    color: 'air-secondary' as ButtonProps['color'],
    icon: SignIcon,
    onClick() {
      console.log('And one more clicked')
    }
  },
  {
    label: 'Last one',
    color: 'air-secondary-no-accent' as ButtonProps['color'],
    icon: MoreMIcon,
    onClick() {
      console.log('Last one clicked')
    }
  }
]
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Select v-model="attrs.color" class="w-44" :items="airColors" placeholder="Color" multiple />
      <B24Select v-model="attrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
      <B24Separator orientation="vertical" class="h-10" />
      <B24Switch v-model="attrs.inverted" class="w-24" placeholder="Inverted" />
    </template>
    <Matrix v-slot="props" :attrs="attrs" container-class="max-w-80">
      <B24Alert :title="data.title" v-bind="props" />
      <B24Alert :title="data.title" :icon="data.icon" v-bind="props" />
      <B24Alert :title="data.title" :icon="data.icon" :close="data.close" v-bind="props" />
      <B24Alert
        :title="data.title"
        :icon="data.icon"
        :close="data.close"
        :actions="action()"
        orientation="horizontal"
        v-bind="props"
      />
      <B24Alert
        :title="data.title"
        :icon="data.icon"
        :close="data.close"
        :description="data.description"
        v-bind="props"
      />
      <B24Alert
        :title="data.title"
        :avatar="{ src: '/b24ui/demo/avatar/employee.png' }"
        :close="data.close"
        :description="data.description"
        v-bind="props"
      />
      <B24Alert
        :title="data.title"
        :icon="data.icon"
        description="Example with multiple actions."
        :actions="multipleActions()"
        v-bind="props"
      />
    </Matrix>
  </PlaygroundPage>
</template>
