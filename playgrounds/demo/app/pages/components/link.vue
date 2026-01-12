<script setup lang="ts">
const attrs = reactive({
  to: '/components/link',
  raw: false,
  isAction: false,
  active: false,
  disabled: false
})

const classes = reactive({
  activeClass: 'font-(--ui-font-weight-bold) text-(--ui-color-copilot-accent-primary)',
  inactiveClass: 'text-(--ui-color-accent-main-alert)'
})
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Input v-model="attrs.to" class="w-56" type="url" placeholder="to" />
      <B24Input v-model="classes.activeClass" class="w-56" placeholder="activeClass" />
      <B24Input v-model="classes.inactiveClass" class="w-56" placeholder="inactiveClass" />
      <B24Separator orientation="vertical" class="h-10" />
      <B24Switch v-model="attrs.raw" label="raw" size="xs" />
      <B24Switch v-model="attrs.isAction" label="isAction" size="xs" />
      <B24Switch v-model="attrs.active" label="active" size="xs" />
      <B24Switch v-model="attrs.disabled" label="disabled" size="xs" />
    </template>

    <PlaygroundCard class="w-96">
      <template #header>
        <ProseH5 class="mb-0">
          {{ attrs.to ? 'As link (tag <a>)' : 'As tag <button>' }}
        </ProseH5>
      </template>

      <div class="flex flex-col items-start gap-3 text-(length:--ui-font-size-sm)">
        <B24Link v-bind="attrs">
          {{ `${attrs.to ? 'Link' : 'Button'} preview` }}
        </B24Link>
        <B24Link v-bind="{ ...attrs, ...classes }">
          {{ `${attrs.to ? 'Link' : 'Button'} preview (with classes)` }}
        </B24Link>
      </div>
    </PlaygroundCard>
  </PlaygroundPage>
</template>
