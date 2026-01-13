<script setup lang="ts">
import theme from '#build/b24ui/calendar'
import { CalendarDate } from '@internationalized/date'
import type { DateValue } from '@internationalized/date'

const colors = Object.keys(theme.variants.color)
const sizes = Object.keys(theme.variants.size)

const attrs = reactive({
  color: [theme.defaultVariants.color],
  size: [theme.defaultVariants.size],
  disabled: false,
  numberOfMonths: 1
})

const multiple = ref(false)
const range = ref(false)

const value = shallowRef(new CalendarDate(2012, 4, 12))
const valueMultiple = shallowRef([
  new CalendarDate(2012, 4, 12),
  new CalendarDate(2012, 4, 14),
  new CalendarDate(2012, 4, 24)
])
const valueRange = shallowRef({
  start: new CalendarDate(2012, 4, 11),
  end: new CalendarDate(2012, 4, 21)
})

const airColors = computed(() => {
  return colors.filter((color) => {
    return color.includes('air')
  })
})

// region Helpers ////
function getColorByDate(date: Date) {
  const isWeekend = date.getDate() > 5 && date.getDate() < 9
  const isDayMeeting = date.getDate() == 6

  if (isWeekend) {
    return 'air-primary-success'
  }

  if (isDayMeeting) {
    return 'air-primary-alert'
  }

  return
}

const isDateDisabled = (date: DateValue) => {
  return date.day >= 2 && date.day <= 4
}

const isDateUnavailable = (date: DateValue) => {
  return date.day >= 15 && date.day <= 17
}
// endregion ////
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Select v-model="attrs.color" class="w-44" :items="airColors" placeholder="Color" multiple />
      <B24Select v-model="attrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
      <B24InputNumber v-model="attrs.numberOfMonths" class="w-24" placeholder="Number of months" />
      <B24Separator orientation="vertical" class="h-10" />
      <B24Switch v-model="multiple" label="Multiple" size="xs" />
      <B24Switch v-model="range" label="Range" size="xs" />
      <B24Switch v-model="attrs.disabled" label="Disabled" size="xs" />
    </template>

    <Matrix v-slot="props" :attrs="attrs">
      <B24Calendar v-if="range" v-model="valueRange" range :is-date-disabled="isDateDisabled" v-bind="props" />
      <B24Calendar v-else-if="multiple" v-model="valueMultiple" multiple :is-date-unavailable="isDateUnavailable" v-bind="props" />
      <B24Calendar v-else v-model="value" v-bind="props">
        <template #day="{ day }">
          <B24Chip
            :show="!!getColorByDate(day.toDate('UTC'))"
            :color="getColorByDate(day.toDate('UTC'))"
            size="sm"
            :b24ui="{ base: '[--ui-counter-size-sm:6px] px-[2px]' }"
          >
            {{ day.day }}
          </B24Chip>
        </template>
      </B24Calendar>
    </Matrix>
  </PlaygroundPage>
</template>
