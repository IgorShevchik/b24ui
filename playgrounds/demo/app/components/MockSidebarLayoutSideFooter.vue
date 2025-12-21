<script setup lang="ts">
import RocketIcon from '@bitrix24/b24icons-vue/outline/RocketIcon'
import GoToLIcon from '@bitrix24/b24icons-vue/outline/GoToLIcon'
import { useNavigation } from '~/composables/useNavigation'

const props = withDefaults(defineProps<{
  framework?: 'nuxt' | 'vue'
}>(), {
  framework: 'nuxt'
})

const { externalLinks } = useNavigation()
</script>

<template>
  <template
    v-for="(item, indexItem) in externalLinks"
    :key="indexItem"
  >
    <B24Link
      class="text-(length:--ui-font-size-sm) mb-2 flex flex-row items-center justify-between"
      :to="item.to"
      :target="item.target"
    >
      <div>{{ item.label }}</div>
      <GoToLIcon class="size-4" />
    </B24Link>
  </template>

  <B24Button
    v-if="props.framework === 'nuxt'"
    block
    label="Use our Nuxt starter"
    color="air-boost"
    size="sm"
    :icon="RocketIcon"
    to="https://bitrix24.github.io/b24ui/docs/getting-started/installation/nuxt/#use-our-nuxt-starter"
    target="_blank"
  />
  <B24Button
    v-else-if="props.framework === 'vue'"
    block
    label="Use our Vue starter"
    color="air-boost"
    size="sm"
    :icon="RocketIcon"
    to="https://bitrix24.github.io/b24ui/docs/getting-started/installation/vue/#use-our-vue-starter"
    target="_blank"
  />
</template>
