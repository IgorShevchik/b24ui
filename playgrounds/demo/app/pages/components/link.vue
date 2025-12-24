<script setup lang="ts">
const attrs = reactive({
  to: '/components/link',
  raw: false,
  isAction: false,
  active: false,
  disabled: false
})
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <div class="flex flex-wrap items-center gap-2">
        <B24Input v-model="attrs.to" class="w-56" type="url" placeholder="to" />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="attrs.raw" label="raw" size="xs" />
        <B24Switch v-model="attrs.isAction" label="isAction" size="xs" />
        <B24Switch v-model="attrs.active" label="active" size="xs" />
        <B24Switch v-model="attrs.disabled" label="disabled" size="xs" />
      </div>
    </template>

    <div class="flex items-stretch flex-wrap justify-start gap-2 min-h-0 mb-4">
      <Matrix v-slot="props" :attrs="attrs">
        <B24Card variant="outline-no-accent" class="w-96">
          <template #header>
            <ProseH5 class="mb-0">
              {{ [props?.raw ? 'raw' : 'default', props?.active ? 'active' : 'inactive', props?.disabled ? 'disabled' : 'enabled'].join(' | ') }}
            </ProseH5>
          </template>

          <div class="flex flex-col items-start gap-3 text-(length:--ui-font-size-sm)">
            <B24Separator :label="props?.to ? 'as link' : 'as button'" />
            <B24Link v-bind="props">
              {{ `${props?.to ? 'Link': 'Button'} preview` }}
            </B24Link>
            <B24Link v-bind="props" active-class="font-(--ui-font-weight-bold) text-(--ui-color-copilot-accent-primary)" inactive-class="text-(--ui-color-accent-main-alert)">
              {{ `${props?.to ? 'Link': 'Button'} preview (with classes)` }}
            </B24Link>
          </div>
        </B24Card>
      </Matrix>
    </div>
  </PlaygroundPage>
</template>
