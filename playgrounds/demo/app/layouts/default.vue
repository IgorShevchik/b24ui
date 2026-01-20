<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useColorMode } from '#imports'
import { useTextDirection } from '@vueuse/core'
import AlignRightIcon from '@bitrix24/b24icons-vue/outline/AlignRightIcon'
import AlignLeftIcon from '@bitrix24/b24icons-vue/outline/AlignLeftIcon'
import type { NavigationMenuItem } from '@bitrix24/b24ui-nuxt'
import { useNavigation } from '~/composables/useNavigation'

const appConfig = useAppConfig()
const dir = useTextDirection()
const colorMode = useColorMode()

const modeContext = ref<string>((appConfig?.colorModeTypeLight || 'light') as string)

watch(() => colorMode.preference, (newPreference) => {
  const isEdge = modeContext.value.startsWith('edge-')
  if (newPreference === 'dark') {
    modeContext.value = isEdge ? 'edge-dark' : 'dark'
  } else if (newPreference === 'light') {
    modeContext.value = isEdge ? 'edge-light' : 'light'
  }
  nextTick(() => {
    syncHtmlClass()
  })
}, { immediate: true, flush: 'post' })

function syncHtmlClass() {
  if (import.meta.client && typeof document !== 'undefined') {
    const htmlElement = document.documentElement
    const themeClasses = ['dark', 'light', 'edge-dark', 'edge-light']
    themeClasses.forEach(themeClass => htmlElement.classList.remove(themeClass))
    htmlElement.classList.add(modeContext.value)
  }
}

watch(modeContext, syncHtmlClass, { immediate: true, flush: 'post' })

useHead({
  title: 'Bitrix24 UI - Playground',
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { name: 'description', content: 'Explore and test all Bitrix24 UI components in an interactive environment' }
  ],
  htmlAttrs: {
    lang: 'en',
    dir: computed(() => appConfig.dir as 'ltr' | 'rtl'),
    class: computed(() => [modeContext.value])
  }
})

const route = useRoute()
const router = useRouter()

const { groups } = useNavigation()
const searchTerm = ref('')
const input = useTemplateRef('input')

const isDark = computed({
  get() {
    return colorMode.value === 'dark'
  },
  set(_isDark: boolean) {
    colorMode.preference = _isDark ? 'dark' : 'light'
  }
})

function toggleMode() {
  isDark.value = !isDark.value
}

function toggleDir() {
  dir.value = dir.value === 'ltr' ? 'rtl' : 'ltr'
}

function toggleModeContext() {
  if (modeContext.value === 'dark' || modeContext.value === 'edge-dark') {
    colorMode.preference = 'dark'
  } else if (modeContext.value === 'light' || modeContext.value === 'edge-light') {
    colorMode.preference = 'light'
  }
}

const getLightContent = computed(() => {
  const result = {
    root: 'max-lg:h-[100dvh] max-lg:min-h-[100dvh]',
    contentWrapper: 'flex-1 min-h-0',
    pageWrapper: 'px-(--content-area-shift) flex-1 min-h-0 max-lg:overflow-y-auto mt-lg',
    container: 'gap-[22px] h-full min-h-0',
    containerWrapper: `h-full min-h-0 bg-transparent lg:p-0 p-0`,
    containerWrapperInner: 'flex flex-col gap-5'
  }

  return result
})

defineShortcuts({
  'ctrl_arrowleft': () => {
    if (route.path === '/') {
      return
    }
    router.push('/')
  },
  'shift_L': () => {
    toggleDir()
  },
  'shift_D': () => {
    toggleMode()
  },
  '/': {
    usingInput: false,
    handler: () => {
      input?.value?.inputRef?.focus()
    }
  }
})

const contains = (value: string, search: string) => value.toLowerCase().includes(search.toLowerCase())

const filteredGroups = computed(() => {
  if (!searchTerm.value) {
    return groups.value
  }

  return groups.value.map((group) => {
    if (!group.id.includes('component')) {
      return group
    }

    return {
      ...group,
      items: group.items.filter(item => contains(String(item.label), searchTerm.value))
    }
  })
})
</script>

<template>
  <B24DashboardGroup>
    <!-- // @see playgrounds/demo/app/assets/css/main.css -->
    <B24SidebarLayout

      :use-light-content="false"
      :b24ui="getLightContent"
    >
      <template #sidebar>
        <B24SidebarHeader>
          <div class="h-full flex items-center gap-x-sm relative my-0 ps-[25px] pe-xs rtl:pe-[25px]">
            <B24Tooltip :content="{ side: 'bottom' }" :text="`Switch to ${dir === 'ltr' ? 'Right-to-left' : 'Left-to-right'} mode`" :kbds="['shift', 'L']">
              <B24Button
                :icon="dir === 'ltr' ? AlignRightIcon : AlignLeftIcon"
                :aria-label="`Switch to ${dir === 'ltr' ? 'Right-to-left' : 'Left-to-right'} mode`"
                color="air-secondary-accent"
                rounded
                size="xs"
                @click="toggleDir"
              />
            </B24Tooltip>
            <B24Tooltip
              class="flex-0 mt-1"
              :content="{ side: 'bottom', align: 'start' }"
              text="Go home"
              :kbds="['ctrl', 'arrowleft']"
            >
              <NuxtLink to="/" class="mt-0 text-(--ui-color-design-selection-content)" aria-label="Home">
                <ProseH3 class="font-(--ui-font-weight-medium) mb-0">
                  Demo
                </ProseH3>
              </NuxtLink>
            </B24Tooltip>
          </div>
          <div class="mt-4 ps-[25px] pe-xs rtl:pe-[25px] pb-[12px]">
            <B24Input ref="input" v-model="searchTerm" placeholder="Filter..." class="group">
              <template #trailing>
                <B24Kbd value="/" dd-class="ring-(--ui-color-design-plain-na-content-secondary) bg-transparent text-muted" />
              </template>
            </B24Input>
          </div>
        </B24SidebarHeader>
        <B24SidebarBody>
          <template v-for="group in filteredGroups" :key="group.id">
            <B24NavigationMenu
              v-if="group.items.length > 0"
              :items="[
                ...(group.label ? [{ label: group.label, type: 'label' as NavigationMenuItem['type'] }] : []),
                ...group.items
              ]"
              orientation="vertical"
            />
          </template>
        </B24SidebarBody>
        <B24SidebarFooter>
          <B24SidebarSection>
            <MockSidebarLayoutSideFooter framework="nuxt" />
          </B24SidebarSection>
        </B24SidebarFooter>
      </template>

      <template #navbar>
        <B24NavbarSpacer />
        <B24NavbarSection class="flex-row items-center justify-start gap-4">
          <B24DashboardSearchButton size="sm" rounded :collapsed="false" :kbds="[{ value: 'meta', size: 'sm' }, { value: 'K', size: 'sm' }]" />
          <B24Tooltip :content="{ side: 'bottom' }" text="Switch color mode" :kbds="['shift', 'D']">
            <B24ColorModeSwitch size="sm" />
          </B24Tooltip>
          <B24RadioGroup
            v-model="modeContext"
            class="hidden lg:inline-flex"
            :items="['dark', 'light', 'edge-dark', 'edge-light']"
            size="xs"
            orientation="horizontal"
            variant="table"
            indicator="hidden"
            @change="toggleModeContext"
          />
        </B24NavbarSection>
      </template>

      <slot />
    </B24SidebarLayout>

    <B24DashboardSearch :groups="groups" :fuse="{ resultLimit: 100 }" :color-mode="false" />
  </B24DashboardGroup>
</template>
