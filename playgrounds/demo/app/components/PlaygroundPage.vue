<script setup lang="ts">
const isUseBg = ref(true)
</script>

<template>
  <div class="w-full flex flex-col gap-lg rounded-(--ui-border-radius-md)">
    <Navbar>
      <template #controls>
        <slot name="controls" />
      </template>
      <template #head-trailing>
        <B24Switch v-model="isUseBg" label="isUseBg" size="xs" />
      </template>
    </Navbar>

    <B24Card
      :variant="isUseBg ? 'outline-alt' : 'plain-no-accent'"
      :class="{ 'backdrop-blur-[20px]': isUseBg }"
      class="border-0"
    >
      <slot :is-use-bg="isUseBg" />
    </B24Card>
  </div>
</template>
