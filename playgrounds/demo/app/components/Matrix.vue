<script lang="ts">
export type MatrixValue<V> = V extends readonly (infer U)[] ? U : V

export type MatrixAttrs = Record<string, unknown | readonly unknown[]>

export interface MatrixProps<T extends MatrixAttrs> {
  attrs: T
  /**
   * - `bare`: only temporarily identifies and sells them into the slot
   * - `card`: wraps each combination in a `PlaygroundCard` with a default header
   */
  layout?: 'bare' | 'card'
  containerClass?: string
  contentClass?: string
}

export type MatrixSlotProps<T extends MatrixAttrs> = {
  [K in keyof T]?: MatrixValue<T[K]>
}
</script>

<script setup lang="ts" generic="T extends MatrixAttrs">
const props = withDefaults(defineProps<MatrixProps<T>>(), {
  layout: 'card'
})

defineSlots<{
  default: (props?: MatrixSlotProps<T>) => any
  header?: (props?: MatrixSlotProps<T>) => any
}>()

const attrKeys = computed(() => Object.keys(props.attrs) as Array<keyof T>)

const multipleKeys = computed(() => {
  return attrKeys.value.filter((key) => {
    return Array.isArray(props.attrs[key])
  })
})

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

function getDefaultHeader(combination: { [K in keyof T]?: MatrixValue<T[K]> }) {
  const parts = multipleKeys.value
    .map(key => combination[key])
    .filter(value => value !== undefined)
    .map(value => String(value))

  return parts.join(' | ')
}
</script>

<template>
  <template v-for="(combination, index) in combinations" :key="index">
    <template v-if="props.layout === 'card'">
      <PlaygroundCard :class="props.containerClass">
        <template v-if="$slots.header || getDefaultHeader(combination)" #header>
          <slot v-if="$slots.header" name="header" v-bind="combination" />
          <ProseH5 v-else class="mb-0">
            {{ getDefaultHeader(combination) }}
          </ProseH5>
        </template>

        <div :class="['flex flex-col items-start justify-start gap-4', props.contentClass]">
          <slot v-bind="combination" />
        </div>
      </PlaygroundCard>
    </template>
    <template v-else>
      <div :class="props.containerClass">
        <slot v-bind="combination" />
      </div>
    </template>
  </template>
</template>
