<script setup lang="ts">
import type { CardProps } from '@bitrix24/b24ui-nuxt'
import { createPlaygroundContext, providePlaygroundContext, usePlaygroundCardStyles } from '../composables/usePlaygroundContext'

const props = defineProps<{
  b24ui?: CardProps['b24ui']
}>()

const slots = defineSlots<{
  controls?: () => any
  trailing?: () => any
  default?: (props: { playgroundContext: PlaygroundContext, cardVariant: CardProps['variant'], cardClass: string }) => any
}>()

const playgroundContext = providePlaygroundContext(createPlaygroundContext())
const { cardVariant, cardClass } = usePlaygroundCardStyles(playgroundContext)
</script>

<template>
  <Navbar>
    <template #trailing>
      <B24Switch v-model="playgroundContext.isUseBg.value" label="isUseBg" size="xs" />
    </template>
    <template v-if="slots.controls" #controls>
      <div class="flex items-center gap-2 overflow-x-auto py-2">
        <slot name="controls" :playground="playgroundContext" />
      </div>
    </template>
  </Navbar>

  <B24Card
    :variant="cardVariant"
    :b24ui="{
      root: [playgroundContext.isUseBg.value ? 'backdrop-blur-xl' : '', 'border-0 border-t-2 rounded-none lg:rounded-(--ui-border-radius-md)'],
      body: 'flex items-stretch flex-wrap justify-center md:justify-start gap-4 min-h-0 p-4',
      ...props.b24ui
    }"
  >
    <slot v-bind="{ playgroundContext, cardVariant, cardClass }" />
  </B24Card>
</template>
