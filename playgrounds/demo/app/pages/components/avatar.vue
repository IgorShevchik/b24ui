<script setup lang="ts">
import theme from '#build/b24ui/avatar'
import IncertImageIcon from '@bitrix24/b24icons-vue/editor/IncertImageIcon'
import PersonIcon from '@bitrix24/b24icons-vue/main/PersonIcon'

const sizes = Object.keys(theme.variants.size) as Array<keyof typeof theme.variants.size>

type AvatarMode = 'text' | 'src' | 'icon'

const isUseBg = ref(true)
const mode = ref<AvatarMode>('src')
const showGroup = ref(false)

const defaultSize = (theme.defaultVariants?.size ?? sizes[0]) as (typeof sizes)[number]
const attrs = reactive({
  size: [defaultSize]
})
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <div class="flex flex-wrap items-center gap-2">
        <B24Select v-model="attrs.size" class="w-44" :items="sizes" placeholder="Size" multiple />
        <B24Select v-model="mode" class="w-32" :items="['text', 'src', 'icon']" placeholder="Mode" />
        <B24Separator orientation="vertical" class="h-10" />
        <B24Switch v-model="showGroup" label="Group" size="xs" />
        <B24Switch v-model="isUseBg" label="isUseBg" size="xs" />
      </div>
    </template>

    <div class="flex items-stretch flex-wrap justify-start gap-2 min-h-0">
      <Matrix v-slot="props" :attrs="attrs">
        <B24Card :variant="isUseBg ? 'outline-no-accent' : 'plain-no-accent'">
          <template #header>
            <ProseH5 class="mb-0">
              {{ [props?.size, mode, showGroup ? 'group' : 'single'].join(' | ') }}
            </ProseH5>
          </template>

          <div class="flex flex-col items-start justify-start gap-4">
            <template v-if="showGroup">
              <B24AvatarGroup :max="3" v-bind="props">
                <B24Avatar src="/b24ui/demo/avatar/employee.png" alt="Employee Name" />
                <B24Avatar src="/b24ui/demo/avatar/assistant.png" alt="Assistant Name" />
                <B24Avatar src="/b24ui/demo/avatar/employee.png" alt="Employee Name" class="grayscale" />
                <B24Avatar src="/b24ui/demo/avatar/employee.png" alt="Employee Name" />
                <B24Avatar src="/b24ui/demo/avatar/assistant.png" alt="Assistant Name" />
              </B24AvatarGroup>
            </template>
            <template v-else>
              <B24Avatar
                v-if="mode === 'src'"
                src="/b24ui/demo/avatar/employee.png"
                text="Employee Name"
                v-bind="props"
              />
              <B24Avatar
                v-else-if="mode === 'icon'"
                :icon="IncertImageIcon"
                alt="Icon"
                v-bind="props"
              />
              <B24Avatar
                v-else
                :icon="PersonIcon"
                text="B24"
                alt="B24"
                v-bind="props"
              />
            </template>
          </div>
        </B24Card>
      </Matrix>
    </div>
  </PlaygroundPage>
</template>
