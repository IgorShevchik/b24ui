<script lang="ts">
export type MatrixValue<V> = V extends readonly (infer U)[] ? U : V

export type MatrixAttrs = Record<string, readonly unknown[]>

export interface MatrixProps<T extends MatrixAttrs> {
  attrs: T
  containerClass?: string
  contentClass?: string
}

export type MatrixSlotProps<T extends MatrixAttrs> = {
  [K in keyof T]?: MatrixValue<T[K]>
}
</script>

<script setup lang="ts" generic="T extends MatrixAttrs">
const props = defineProps<MatrixProps<T>>()

defineSlots<{
  default: (props?: MatrixSlotProps<T>) => any
  clear: (props?: MatrixSlotProps<T>) => any
  header: (props?: MatrixSlotProps<T>) => any
}>()

const attrKeys = computed(() => Object.keys(props.attrs) as Array<keyof T>)

const combinations = computed(() => {
  const keys = attrKeys.value

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
    const variants = props.attrs[key] as Array<MatrixValue<T[typeof key]>>

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

function getDefaultHeader(combination: { [K in keyof T]?: MatrixValue<T[K]> }): string {
  return Object.values(combination).join(' | ')
}
</script>

<template>
  <template v-for="(combination, index) in combinations" :key="index">
    <slot name="clear" v-bind="combination">
      <PlaygroundCard :class="props.containerClass">
        <template #header>
          <slot name="header" v-bind="combination">
            <ProseH5 class="mb-0">
              {{ getDefaultHeader(combination) }}
            </ProseH5>
          </slot>
        </template>

        <div :class="['flex flex-col items-start justify-start gap-4', props.contentClass]">
          <slot v-bind="combination" />
        </div>
      </PlaygroundCard>
    </slot>
  </template>
</template>
