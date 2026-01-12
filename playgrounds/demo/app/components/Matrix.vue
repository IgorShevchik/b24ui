<script lang="ts">
export type MatrixValue<V> = V extends readonly (infer U)[] ? U : V

export type MatrixAttrs = Record<string, unknown | readonly unknown[]>

export interface MatrixProps<T extends MatrixAttrs> {
  attrs: T
}

export type MatrixSlotProps<T extends MatrixAttrs> = {
  [K in keyof T]: T[K] extends readonly (infer U)[] ? U : never
}
</script>

<script setup lang="ts" generic="T extends MatrixAttrs">
const props = defineProps<MatrixProps<T>>()

defineSlots<{
  default: (props?: MatrixSlotProps<T>) => any
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
