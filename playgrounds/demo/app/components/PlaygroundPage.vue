<script setup lang="ts">
import { createPlaygroundContext, providePlaygroundContext } from '../composables/usePlaygroundContext'

const playground = providePlaygroundContext(createPlaygroundContext({ isUseBg: true }))
</script>

<template>
  <div class="w-full flex flex-col gap-lg rounded-(--ui-border-radius-md)">
    <Navbar>
      <template #controls>
        <slot name="controls" :playground="playground" />
      </template>
      <template #head-trailing>
        <B24Switch v-model="playground.isUseBg.value" label="isUseBg" size="xs" />
      </template>
    </Navbar>

    <B24Card
      :variant="playground.isUseBg.value ? 'outline-alt' : 'plain-no-accent'"
      :class="{ 'backdrop-blur-[20px]': playground.isUseBg.value }"
      class="border-0"
    >
      <div class="flex items-stretch flex-wrap justify-start gap-2 min-h-0">
        <slot :playground="playground" />
      </div>
    </B24Card>
  </div>
</template>
