<script setup lang="ts">
import theme from '#build/b24ui/color-picker'

const sizes = Object.keys(theme.variants.size)

const attrs = reactive({
  size: [theme.defaultVariants.size],
  disabled: false
})

const colorHex = ref('#00C16A')

function handleColorChange(event: Event) {
  colorHex.value = (event.target as HTMLInputElement).value
}
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Select v-model="attrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />

      <B24FieldGroup>
        <B24Button>
          <span :style="{ backgroundColor: colorHex }" class="inline-flex size-5 rounded-sm" />
        </B24Button>
        <B24Input :model-value="colorHex" @change="handleColorChange" />
      </B24FieldGroup>
    </template>

    <Matrix v-slot="props" :attrs="attrs">
      <B24ColorPicker v-model="colorHex" v-bind="props" />
    </Matrix>
  </PlaygroundPage>
</template>
