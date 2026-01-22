<script setup lang="ts">
import theme from '#build/b24ui/field-group'

const sizes = Object.keys(theme.variants.size)
const orientations = Object.keys(theme.variants.orientation)

const knowledgeBase = ['Select', 'Create']
const smartScripts = ['Scripts', 'Create script', 'Install from Bitrix24.Market']

const items = [
  [{ label: 'Knowledge base', type: 'label' }, ...knowledgeBase],
  [{ label: 'Smart scripts', type: 'label' }, ...smartScripts]
]

function onClick() {
  return new Promise<void>(res => setTimeout(res, 3000))
}

const attrs = reactive({
  size: ['md' as keyof typeof theme.variants.size]
})

const singleAttrs = reactive({
  orientation: 'horizontal' as keyof typeof theme.variants.orientation,
  noSplit: false
})
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Select v-model="attrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
      <B24Select v-model="singleAttrs.orientation" class="w-44" :items="orientations" placeholder="Orientation" />
      <B24Separator orientation="vertical" class="h-10" />
      <B24Switch v-model="singleAttrs.noSplit" label="No split" size="xs" />
    </template>

    <Matrix v-slot="props" :attrs="attrs">
      <B24FieldGroup v-bind="{ ...props, ...singleAttrs }">
        <B24Button
          loading-auto
          use-clock
          @click="onClick"
        >
          Button
        </B24Button>
        <B24Button use-dropdown />
      </B24FieldGroup>

      <B24FieldGroup v-bind="{ ...props, ...singleAttrs }">
        <B24Button loading-auto use-clock @click="onClick">
          Button
        </B24Button>
        <B24Button loading-auto use-clock @click="onClick">
          Button
        </B24Button>
        <B24Button loading-auto use-clock @click="onClick">
          Button
        </B24Button>
      </B24FieldGroup>

      <B24FieldGroup v-bind="{ ...props, ...singleAttrs }">
        <B24Input name="search" placeholder="Search&hellip;" aria-label="Search" type="search" />
        <B24Button
          loading-auto
          use-clock
          @click="onClick"
        >
          Button
        </B24Button>
      </B24FieldGroup>

      <B24FieldGroup v-bind="{ ...props, ...singleAttrs }">
        <B24Select class="w-32" :items="items" name="some_value" placeholder="Choose a value&hellip;" aria-label="Choose a value" />
        <B24Button
          loading-auto
          use-clock
          @click="onClick"
        >
          Button
        </B24Button>
      </B24FieldGroup>

      <B24FieldGroup v-bind="{ ...props, ...singleAttrs }">
        <B24Badge color="air-tertiary" label="https://" />
        <B24Input class="max-w-40" type="url" placeholder="www.example.com" />
      </B24FieldGroup>

      <B24FieldGroup v-bind="{ ...props, ...singleAttrs }">
        <B24InputNumber class="max-w-40" placeholder="Some number" />
        <B24Button
          loading-auto
          use-clock
          @click="onClick"
        >
          Button
        </B24Button>
      </B24FieldGroup>
    </Matrix>
  </PlaygroundPage>
</template>
