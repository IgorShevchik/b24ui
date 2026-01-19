<script setup lang="ts">
import { createPlaygroundContext, providePlaygroundContext, usePlaygroundCardStyles } from '../composables/usePlaygroundContext'

const playgroundContext = providePlaygroundContext(createPlaygroundContext())
const { cardVariant, cardClass } = usePlaygroundCardStyles(playgroundContext)
</script>

<template>
  <div class="w-full flex flex-col gap-5">
    <Navbar>
      <template #head-trailing>
        <B24Switch v-model="playgroundContext.isUseBg.value" label="isUseBg" size="xs" />
      </template>
      <template #controls>
        <div class="flex flex-wrap items-center gap-2">
          <slot name="controls" :playground="playgroundContext" />
        </div>
      </template>
    </Navbar>

    <B24Card
      :variant="cardVariant"
      :class="{ 'backdrop-blur-[20px]': playgroundContext.isUseBg.value }"
      class="border-0"
    >
      <div class="flex items-stretch flex-wrap justify-start gap-2 min-h-0">
        <slot v-bind="{ playgroundContext, cardVariant, cardClass }" />
      </div>
    </B24Card>
  </div>
</template>
