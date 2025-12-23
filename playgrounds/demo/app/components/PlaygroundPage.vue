<template>
  <div class="w-full flex flex-col gap-lg rounded-(--ui-border-radius-md) mt-lg">
    <Navbar class="rounded-(--ui-border-radius-md)">
      <template #controls>
        <slot name="controls" />
      </template>
    </Navbar>

    <div class="min-w-0 base-mode bg-(--ui-color-bg-content-primary) backdrop-blur-sm backdrop-brightness-110 px-[15px] py-xs2 rounded-(--ui-border-radius-md)">
      <slot />
    </div>
  </div>
</template>
