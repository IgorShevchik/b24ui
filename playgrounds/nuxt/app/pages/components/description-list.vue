<script setup lang="ts">
import theme from '#build/b24ui/description-list'
import type { ButtonProps } from '@bitrix24/b24ui-nuxt/components/Button.vue'
import type { DescriptionListItem } from '@bitrix24/b24ui-nuxt/components/DescriptionList.vue'
import SignIcon from '@bitrix24/b24icons-vue/main/SignIcon'
import MoreMIcon from '@bitrix24/b24icons-vue/outline/MoreMIcon'
import DownloadDoubleIcon from '@bitrix24/b24icons-vue/actions/DownloadDoubleIcon'
import PersonIcon from '@bitrix24/b24icons-vue/main/PersonIcon'
import Calendar1Icon from '@bitrix24/b24icons-vue/main/Calendar1Icon'
import CreditDebitCardIcon from '@bitrix24/b24icons-vue/main/CreditDebitCardIcon'

const sizes = Object.keys(theme.variants.size)

const multipleAttrs = reactive({
  size: [theme.defaultVariants.size]
})

const variants = ['simple', 'icons', 'actions', 'custom']
const variant = ref<string>(variants[0] ?? '')

const action = (color: string): ButtonProps[] => [
  {
    icon: MoreMIcon,
    color: color as ButtonProps['color'],
    onClick() {
      console.log('Action clicked')
    }
  }
]

const multipleActions = (color: string): ButtonProps[] => [
  {
    label: 'Action',
    color: color as ButtonProps['color'],
    onClick() {
      console.log('Action clicked')
    }
  },
  {
    label: 'Another action',
    color: color as ButtonProps['color'],
    onClick() {
      console.log('Another action clicked')
    }
  },
  {
    label: 'One more action',
    color: color as ButtonProps['color'],
    onClick() {
      console.log('One more action clicked')
    }
  },
  {
    label: 'And one more',
    color: color as ButtonProps['color'],
    icon: SignIcon,
    onClick() {
      console.log('And one more clicked')
    }
  },
  {
    label: 'Last one',
    color: color as ButtonProps['color'],
    icon: MoreMIcon,
    onClick() {
      console.log('Last one clicked')
    }
  }
]

const itemsSimple: DescriptionListItem[] = [
  {
    label: 'Full name',
    description: 'Michael Foster'
  },
  {
    label: 'Event',
    description: 'Payment is made through Atol online'
  },
  {
    label: 'Line 1.3',
    description: 'Description 1.3',
    class: 'text-(--ui-color-design-plain-a-content)'
  },
  {
    label: 'Line 1.4',
    description: 'Description 1.4',
    b24ui: {
      description: 'font-(--ui-font-weight-semi-bold)'
    }
  }
]

const itemsActions: DescriptionListItem[] = [
  {
    label: 'Line 2.1',
    description: 'Description 2.1',
    actions: action('air-tertiary'),
    orientation: 'horizontal' as DescriptionListItem['orientation']
  },
  {
    label: 'Line 2.2',
    description: 'Description 2.2',
    actions: action('air-primary'),
    orientation: 'horizontal' as DescriptionListItem['orientation']
  },
  {
    label: 'Line 2.3',
    description: 'Description 2.3',
    actions: action('air-tertiary'),
    orientation: 'horizontal' as DescriptionListItem['orientation']
  },
  {
    label: 'Line 2.4',
    description: 'Fugiat ipsum ipsum deserunt culpa aute sint do nostrud anim incididunt cillum culpa consequat. Excepteur qui ipsum aliquip consequat sint. Sit id mollit nulla mollit nostrud in ea officia proident. Irure nostrud pariatur mollit ad adipisicing reprehenderit deserunt qui eu.',
    actions: multipleActions('air-secondary')
  }
]

const itemsIcons: DescriptionListItem[] = [
  {
    label: 'Line 1.1',
    description: 'Description 1.1',
    avatar: {
      src: '/avatar/employee.png'
    }
  },
  {
    label: 'Line 1.2',
    description: 'Description 1.2',
    icon: SignIcon
  },
  {
    label: 'Line 1.3',
    description: 'Description 1.3',
    avatar: {
      icon: PersonIcon
    }
  },
  {
    description: 'Description 1.4',
    icon: SignIcon
  }
]

const itemsCustom: (DescriptionListItem & { value?: Date | string })[] = [
  {
    label: 'Amount',
    value: 'Paid',
    description: '$10,560.00',
    b24ui: {
      label: 'font-(--ui-font-weight-semi-bold) text-(length:--ui-font-size-md)/(--ui-font-line-height-md) text-(--b24ui-typography-label-color)',
      description: 'font-(--ui-font-weight-semi-bold) text-(length:--ui-font-size-lg) block w-full'
    }
  },
  {
    label: 'Client',
    avatar: {
      icon: PersonIcon
    },
    description: 'Employee Name',
    b24ui: {
      description: 'font-(--ui-font-weight-semi-bold)'
    }
  },
  {
    label: 'Due date',
    icon: Calendar1Icon,
    value: new Date('2023-01-31T03:24:00')
  },
  {
    label: 'Payment method',
    icon: CreditDebitCardIcon,
    description: 'Paid with MasterCard'
  }
]

const itemsMap: Record<string, DescriptionListItem[]> = {
  simple: itemsSimple,
  icons: itemsIcons,
  actions: itemsActions,
  custom: itemsCustom
}
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Select v-model="multipleAttrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
      <B24Select v-model="variant" class="w-40" :items="variants" placeholder="Demo" />
    </template>

    <Matrix v-slot="props" :attrs="multipleAttrs" :b24ui="{ root: 'max-w-200 w-full' }">
      <template v-if="variant === 'custom'">
        <B24DescriptionList
          legend="Applicant Information"
          text="Personal details and application."
          class="rounded-md backdrop-blur-md bg-(--ui-color-design-outline-na-bg) ring-0 border border-(--ui-color-divider-vibrant-default)"
          :items="itemsCustom"
          v-bind="props"
          :b24ui="{
            legend: 'sr-only',
            text: 'sr-only',
            labelWrapper: 'px-4',
            container: '',
            descriptionWrapper: 'px-4',
            footer: 'mt-4 px-4 py-6 flex flex-row flex-nowrap justify-end items-center'
          }"
        >
          <template #description="{ item }">
            <template v-if="item.label === 'Amount'">
              <div class="flex flex-wrap flex-row items-center justify-between gap-4">
                <div>{{ item.description }}</div>
                <B24Badge
                  :label="item.value?.toString()"
                  color="air-primary-success"
                  inverted
                  size="md"
                />
              </div>
            </template>
            <template v-else-if="item.label === 'Due date'">
              <time :datetime="(item?.value as Date)?.toISOString()">{{ (item?.value as Date)?.toDateString() }}</time>
            </template>
            <template v-else>
              {{ item.description }}
            </template>
          </template>
          <template #footer>
            <B24Button
              color="air-primary"
              label="Download receipt"
              :icon="DownloadDoubleIcon"
            />
          </template>
        </B24DescriptionList>
      </template>
      <template v-else>
        <B24DescriptionList
          legend="Applicant Information"
          text="Personal details and application."
          :items="itemsMap[variant] ?? itemsSimple"
          v-bind="props"
        />
      </template>
    </Matrix>
  </PlaygroundPage>
</template>
