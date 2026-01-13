<script setup lang="ts">
import theme from '#build/b24ui/switch'
import CheckIcon from '@bitrix24/b24icons-vue/main/CheckIcon'
import Cross30Icon from '@bitrix24/b24icons-vue/actions/Cross30Icon'

const sizes = Object.keys(theme.variants.size)
const colors = Object.keys(theme.variants.color)

const attrs = reactive({
  color: [theme.defaultVariants.color],
  size: [theme.defaultVariants.size],
  loading: false,
  disabled: false,
  required: false
})

const showIcons = ref(false)
const checked = ref(true)

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
      <B24Separator orientation="vertical" class="h-10" />
      <B24Switch v-model="showIcons" label="Icons" size="xs" />
      <B24Switch v-model="attrs.loading" label="Loading" size="xs" />
      <B24Switch v-model="attrs.disabled" label="Disabled" size="xs" />
      <B24Switch v-model="attrs.required" label="Required" size="xs" />
    </template>

    <Matrix v-slot="props" :attrs="attrs">
      <B24Switch
        v-model="checked"
        label="Preview"
        :unchecked-icon="showIcons ? Cross30Icon : undefined"
        :checked-icon="showIcons ? CheckIcon : undefined"
        v-bind="props"
      />
      <B24Switch
        v-model="checked"
        label="With description"
        description="This is a description"
        :unchecked-icon="showIcons ? Cross30Icon : undefined"
        :checked-icon="showIcons ? CheckIcon : undefined"
        v-bind="props"
      />
    </Matrix>
  </PlaygroundPage>
</template>
