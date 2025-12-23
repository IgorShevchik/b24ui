<script setup lang="ts" generic="T extends Record<string, unknown | readonly unknown[]>">
type MatrixValue<V> = V extends readonly (infer U)[] ? U : V

const props = defineProps<{
  attrs: T
  containerClass?: string
  containerProps?: Record<string, unknown>
}>()

defineSlots<{
  default: (props?: { [K in keyof T]: T[K] extends (infer U)[] ? U : never }) => any
}>()

const combinations = computed(() => {
  const keys = Object.keys(props.attrs) as Array<keyof T>

  if (keys.length === 0) {
    return [{}] as Array<{ [K in keyof T]?: MatrixValue<T[K]> }>
  }

  const result: Array<{ [K in keyof T]?: MatrixValue<T[K]> }> = []

  function generateCombinations(index: number, current: { [K in keyof T]?: MatrixValue<T[K]> }) {
    if (index === keys.length) {
      result.push({ ...current })
      return
    }

    const key = keys[index]!
    const raw = props.attrs[key]
    const variants = (Array.isArray(raw) ? raw : [raw]) as Array<MatrixValue<T[typeof key]>>

    if (variants.length === 0) {
      return
    }

    for (const value of variants) {
      generateCombinations(index + 1, { ...current, [key]: value } as any)
    }
  }

  generateCombinations(0, {})
  return result
})
</script>

<template>
  <template v-for="(combination, index) in combinations" :key="index">
    <slot v-bind="combination" />
  </template>
</template>
