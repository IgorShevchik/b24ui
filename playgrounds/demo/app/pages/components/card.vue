<script setup lang="ts">
import theme from '#build/b24ui/card'

const variants = Object.keys(theme.variants.variant) as Array<keyof typeof theme.variants.variant>

const isUseBg = ref(true)
const withHeader = ref(true)
const withFooter = ref(true)

const defaultVariant = (theme.defaultVariants?.variant ?? variants[0]) as (typeof variants)[number]
const attrs = reactive({
  variant: [defaultVariant]
})
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <div class="flex flex-wrap items-center gap-2">
        <B24Select v-model="attrs.variant" class="w-56" :items="variants" placeholder="Variant" multiple />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="withHeader" label="Header" size="xs" />
        <B24Switch v-model="withFooter" label="Footer" size="xs" />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="isUseBg" label="isUseBg" size="xs" />
      </div>
    </template>

    <div class="flex items-stretch flex-wrap justify-start gap-2 min-h-0">
      <Matrix v-slot="props" :attrs="attrs">
        <B24Card :variant="isUseBg ? (props?.variant) : 'plain-no-accent'" class="w-60">
          <template v-if="withHeader" #header>
            <ProseH5 class="mb-0">
              {{ props?.variant }}
            </ProseH5>
          </template>

          <Placeholder class="h-32" />

          <template v-if="withFooter" #footer>
            <Placeholder class="h-8" />
          </template>
        </B24Card>
      </Matrix>
    </div>
  </PlaygroundPage>
</template>
