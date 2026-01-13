<script setup lang="ts">
import theme from '#build/b24ui/checkbox'

const checked = ref(true)

const sizes = Object.keys(theme.variants.size)
const colors = Object.keys(theme.variants.color)
const variants = Object.keys(theme.variants.variant)
const indicators = Object.keys(theme.variants.indicator)

const attrs = reactive({
  color: [theme.defaultVariants.color],
  size: [theme.defaultVariants.size],
  variant: [theme.defaultVariants.variant],
  indicator: [theme.defaultVariants.indicator],
  disabled: false,
  required: false
})

const airColors = computed(() => {
  return colors.filter((color) => {
    return color.includes('air')
  })
})
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Select v-model="attrs.color" class="w-44" :items="airColors" placeholder="Color" multiple />
      <B24Select v-model="attrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
      <B24Select v-model="attrs.variant" class="w-40" :items="variants" placeholder="Variant" multiple />
      <B24Select v-model="attrs.indicator" class="w-44" :items="indicators" placeholder="Indicator" multiple />
      <B24Separator orientation="vertical" class="h-10" />
      <B24Switch v-model="attrs.disabled" label="Disabled" size="xs" />
      <B24Switch v-model="attrs.required" label="Required" size="xs" />
      <B24Switch v-model="checked" label="Checked" size="xs" />
    </template>

    <Matrix v-slot="props" :attrs="attrs">
      <B24Checkbox
        v-model="checked"
        label="Check me"
        name="matrix"
        v-bind="props"
      />
      <B24Checkbox
        v-model="checked"
        label="With description"
        description="This is a description"
        name="matrix_desc"
        v-bind="props"
      />
    </Matrix>
  </PlaygroundPage>
</template>
