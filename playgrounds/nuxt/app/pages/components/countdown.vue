<script setup lang="ts">
import theme from '#build/b24ui/countdown'
import B24Countdown from '@bitrix24/b24ui-nuxt/components/Countdown.vue'
import PlayIcon from '@bitrix24/b24icons-vue/button/PlayIcon'
import StopIcon from '@bitrix24/b24icons-vue/button/StopIcon'
import StopHandIcon from '@bitrix24/b24icons-vue/main/StopHandIcon'
import Refresh5Icon from '@bitrix24/b24icons-vue/actions/Refresh5Icon'
import Clock2Icon from '@bitrix24/b24icons-vue/main/Clock2Icon'
import Cross30Icon from '@bitrix24/b24icons-vue/actions/Cross30Icon'

const sizes = Object.keys(theme.variants.size)

const multipleAttrs = reactive({
  size: [theme.defaultVariants.size]
})

const singleAttrs = reactive({
  seconds: 60,
  interval: 1000,
  showMinutes: true,
  useCircle: false,
  emitEvents: true
})

// region Control ////
const countdownControlRef = ref<typeof B24Countdown | null>(null)
const countingControl = ref(false)

function onControlStart() {
  countingControl.value = true
  countdownControlRef.value?.start()
}

function onControlStop() {
  countingControl.value = false
  countdownControlRef.value?.stop()
}

function onControlAbort() {
  countingControl.value = false
  countdownControlRef.value?.abort()
}

function onControlRestart() {
  countingControl.value = true
  countdownControlRef.value?.restart()
}

function onControlCountdownAbort() {
  console.log('event:abort')
}

function onControlCountdownStart() {
  console.log('event:start')
}

function onControlCountdownEnd() {
  countingControl.value = false
  console.log('event:end')
}

function onControlCountdownProgress(params: any) {
  console.log('event:progress', params.totalSeconds, params)
}
// endregion ////
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24FormField label="Seconds" orientation="horizontal">
        <B24InputNumber v-model="singleAttrs.seconds" class="w-28" />
      </B24FormField>
      <B24FormField label="Interval" orientation="horizontal">
        <B24InputNumber v-model="singleAttrs.interval" class="w-32" />
      </B24FormField>
      <B24Select v-model="multipleAttrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />

      <B24Switch v-model="singleAttrs.showMinutes" label="ShowMinutes" />
      <B24Switch v-model="singleAttrs.useCircle" label="UseCircle" />
      <B24Switch v-model="singleAttrs.emitEvents" label="EmitEvents" />
    </template>

    <template #default="{ cardVariant, cardBorderClass }">
      <Matrix v-slot="props" :attrs="multipleAttrs" :b24ui="{ root: 'max-w-120' }">
        <div class="flex flex-wrap items-center justify-between gap-4 w-full min-h-8">
          <B24Countdown
            v-bind="{ ...props, ...singleAttrs }"
          />
          <B24Countdown
            :icon="Clock2Icon"
            v-bind="{ ...props, ...singleAttrs }"
            :use-circle="false"
          />
          <B24Countdown
            :avatar="{ src: '/avatar/employee.png', text: 'Employee Name' }"
            v-bind="{ ...props, ...singleAttrs }"
            :use-circle="false"
          />
        </div>
        <B24Countdown
          v-slot="{ days, hours, minutes, seconds, milliseconds }"
          :seconds="singleAttrs.seconds"
          :interval="singleAttrs.interval"
          v-bind="{ ...props }"
        >
          <span>Time Remaining: {{ days }} days, {{ hours }} hours, {{ minutes }} minutes, {{ seconds }}.<small>{{ Math.floor(milliseconds / 100) }}</small> seconds.</span>
        </B24Countdown>
      </Matrix>

      <B24Card
        :variant="cardVariant"
        :class="[cardBorderClass, 'max-w-120 w-full']"
      >
        <template #header>
          <ProseH5 class="mb-0">
            Control
          </ProseH5>
        </template>
        <div class="flex flex-wrap items-center justify-around gap-3">
          <B24Button
            color="air-tertiary-no-accent"
            size="sm"
            class="p-0 rounded-full"
            :b24ui="{ baseLine: 'ps-0 pe-0' }"
            @click="onControlStop"
          >
            <div class="shrink-0 relative h-8 group">
              <B24Countdown
                ref="countdownControlRef"
                as="div"
                class="size-full group-hover:z-10 group-hover:opacity-40"
                :need-start-immediately="false"
                size="lg"
                v-bind="{ ...singleAttrs }"
                @start="onControlCountdownStart"
                @abort="onControlCountdownAbort"
                @end="onControlCountdownEnd"
                @progress="onControlCountdownProgress"
                @click="onControlCountdownEnd"
              />
              <Cross30Icon
                v-if="countingControl"
                class="cursor-pointer size-full opacity-0 group-hover:opacity-100 text-legend group-hover:text-legend absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-20"
                @click="onControlCountdownEnd"
              />
            </div>
          </B24Button>

          <div class="flex items-center justify-between gap-2">
            <B24Tooltip text="Start counting">
              <B24Button
                :disabled="countingControl"
                size="sm"
                :icon="PlayIcon"
                color="air-primary-success"
                @click="onControlStart"
              />
            </B24Tooltip>
            <B24Separator decorative orientation="vertical" type="dashed" />
            <B24Tooltip text="Stop counting">
              <B24Button
                :disabled="!countingControl"
                size="sm"
                :icon="StopIcon"
                color="air-primary"
                @click="onControlStop"
              />
            </B24Tooltip>
            <B24Tooltip text="Abort counting">
              <B24Button
                :disabled="!countingControl"
                size="sm"
                :icon="StopHandIcon"
                color="air-tertiary"
                @click="onControlAbort"
              />
            </B24Tooltip>
            <B24Tooltip text="Restart counting">
              <B24Button
                :disabled="!countingControl"
                size="sm"
                :icon="Refresh5Icon"
                color="air-tertiary"
                @click="onControlRestart"
              />
            </B24Tooltip>
          </div>
        </div>
      </B24Card>
    </template>
  </PlaygroundPage>
</template>
