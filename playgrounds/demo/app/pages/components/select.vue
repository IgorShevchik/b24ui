<script setup lang="ts">
/**
 * @see playground/app/pages/components/select-menu.vue
 */
import type { SelectItem, SelectProps, AvatarProps } from '@bitrix24/b24ui-nuxt'
import theme from '#build/b24ui/select'
import type { IUser } from '~/types'
import Expand1Icon from '@bitrix24/b24icons-vue/actions/Expand1Icon'
import Search2Icon from '@bitrix24/b24icons-vue/main/Search2Icon'
import UserIcon from '@bitrix24/b24icons-vue/common-b24/UserIcon'
import RocketIcon from '@bitrix24/b24icons-vue/main/RocketIcon'
import HelpIcon from '@bitrix24/b24icons-vue/button/HelpIcon'
import PlusInCircleIcon from '@bitrix24/b24icons-vue/actions/PlusInCircleIcon'
import ArrowTopIcon from '@bitrix24/b24icons-vue/actions/ArrowTopIcon'
import CircleCheckIcon from '@bitrix24/b24icons-vue/main/CircleCheckIcon'
import CancelIcon from '@bitrix24/b24icons-vue/button/CancelIcon'

const colors = Object.keys(theme.variants.color)
const sizes = Object.keys(theme.variants.size)

const attrs = reactive({
  color: [theme.defaultVariants.color],
  size: [theme.defaultVariants.size],
  multiple: false,
  disabled: false,
  loading: false
})

const airColors = computed(() => {
  return colors.filter((color) => {
    return color.includes('air')
  })
})

const knowledgeBase = ['Select Knowledge base', 'Create knowledge base'] satisfies SelectItem[]
const smartScripts = ['Scripts', 'Create script', 'Install from Bitrix24.Market'] satisfies SelectItem[]
const smartProcess = ['Smart Process Automation'] satisfies SelectItem[]
const settings = ['CRM settings', 'My company details', 'Access permissions'] satisfies SelectItem[]

const items = [
  [...knowledgeBase],
  [{ label: 'Smart scripts', type: 'label' as const }, ...smartScripts],
  ['Bitrix24.Market'],
  [{ label: 'Smart Process Automation', type: 'label' as const }, ...smartProcess],
  [{ label: 'Settings', type: 'label' as const }, ...settings]
] satisfies SelectItem[][]

const value = ref('CRM settings')

const statuses = [
  {
    label: 'Backlog',
    value: 'backlog',
    description: 'Issues that have been identified but not yet prioritized',
    icon: HelpIcon
  },
  {
    label: 'Todo',
    value: 'todo',
    description: 'Issues that are ready to be worked on',
    icon: PlusInCircleIcon,
    color: 'air-primary-copilot' as SelectProps['color'],
    disabled: true
  },
  {
    label: 'In Progress',
    value: 'in_progress',
    description: 'Issues that are currently being worked on',
    icon: ArrowTopIcon,
    color: 'air-primary' as SelectProps['color']
  },
  {
    label: 'Done',
    value: 'done',
    icon: CircleCheckIcon,
    color: 'air-primary-success' as SelectProps['color']
  },
  { type: 'separator' as const },
  {
    label: 'Canceled',
    value: 'canceled',
    icon: CancelIcon,
    color: 'air-primary-alert' as SelectProps['color']
  }
] satisfies SelectItem[]

const { data: users, status } = await useFetch('https://jsonplaceholder.typicode.com/users', {
  transform: (data: IUser[]) => {
    return data?.map(user => ({
      label: user.name,
      value: String(user.id),
      avatar: { src: `https://i.pravatar.cc/120?img=${user.id}` }
    })) || []
  },
  lazy: true
})

function getStatusIcon(value: string) {
  return statuses.find(status => status.value === value)?.icon || UserIcon
}

function getUserAvatar(value: string) {
  return users.value?.find(user => user.value === value)?.avatar || {}
}
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Select v-model="attrs.color" class="w-44" :items="airColors" placeholder="Color" multiple />
      <B24Select v-model="attrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
      <B24Separator orientation="vertical" class="h-10" />
      <B24Switch v-model="attrs.multiple" label="Multiple" size="xs" />
      <B24Switch v-model="attrs.disabled" label="Disabled" size="xs" />
      <B24Switch v-model="attrs.loading" label="Loading" size="xs" />
    </template>

    <Matrix v-slot="props" :attrs="attrs">
      <PlaygroundCard class="w-[240px]">
        <template #header>
          <ProseH5 class="mb-0">
            {{ [props?.color, props?.size].join(' | ') }}
          </ProseH5>
        </template>

        <div class="flex flex-col gap-4">
          <B24Select
            v-model="value"
            :items="items"
            autofocus
            v-bind="props"
            placeholder="Choose a value…"
            aria-label="Choose a value"
          />
          <B24Select :default-value="value" :items="items" v-bind="props" tag="tag" :tag-color="props?.color" />
          <B24Select placeholder="Highlight" highlight :items="items" v-bind="props" />
          <B24Select placeholder="Search..." :avatar="{ src: '/b24ui/demo/avatar/employee.png' }" :items="items" v-bind="props" />
          <B24Select placeholder="Loading trailing" v-bind="props" trailing :items="items" />
          <B24Select placeholder="Trailing icon" :trailing-icon="RocketIcon" v-bind="props" :items="items" />
          <B24Select placeholder="Underline" underline v-bind="props" :items="items" />
          <B24Select placeholder="Rounded" rounded v-bind="props" :items="items" />
          <B24Select placeholder="No border" no-border v-bind="props" :items="items" />
          <B24Select placeholder="No padding" no-padding v-bind="props" :items="items" />
          <B24Select
            v-if="props?.multiple === false"
            :items="statuses"
            :icon="Search2Icon"
            v-bind="props"
            name="some_value"
            placeholder="Search status&hellip;"
            aria-label="Search status"
            arrow
          >
            <template #leading="{ modelValue, b24ui }">
              <Component
                :is="getStatusIcon(modelValue)"
                v-if="modelValue"
                :class="b24ui.leadingIcon()"
              />
            </template>
          </B24Select>
          <B24Select
            v-if="props?.multiple === false"
            :items="users || []"
            :icon="UserIcon"
            :trailing-icon="Expand1Icon"
            v-bind="props"
            :loading="status === 'pending'"
            name="some_users"
            placeholder="Search users&hellip;"
            aria-label="Search users"
            arrow
          >
            <template #leading="{ modelValue, b24ui }">
              <B24Avatar
                v-if="modelValue"
                v-bind="getUserAvatar(modelValue)"
                :size="b24ui.leadingAvatarSize() as AvatarProps['size']"
                :class="b24ui.leadingAvatar()"
              />
            </template>
          </B24Select>
        </div>
      </PlaygroundCard>
    </Matrix>
  </PlaygroundPage>
</template>
