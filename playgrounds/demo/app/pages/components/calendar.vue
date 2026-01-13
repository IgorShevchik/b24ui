<script setup lang="ts">
import theme from '#build/b24ui/calendar'
import { CalendarDate, DateFormatter, getLocalTimeZone } from '@internationalized/date'
import type { DateValue } from '@internationalized/date'
import ExampleGrid from '../../components/ExampleGrid.vue'
import ExampleCard from '../../components/ExampleCard.vue'
import Calendar1Icon from '@bitrix24/b24icons-vue/main/Calendar1Icon'

const colors = Object.keys(theme.variants.color)
const sizes = Object.keys(theme.variants.size)

const attrs = reactive({
  color: [theme.defaultVariants.color],
  size: [theme.defaultVariants.size],
  multiple: false,
  range: false
})

const value = shallowRef(new CalendarDate(2012, 4, 12))
const defaultValue = shallowRef(new CalendarDate(2012, 4, 12))
const valueMultiple = shallowRef([
  new CalendarDate(2012, 4, 12),
  new CalendarDate(2012, 4, 14),
  new CalendarDate(2012, 4, 24)
])
const valueRange = shallowRef({
  start: new CalendarDate(2012, 4, 11),
  end: new CalendarDate(2012, 4, 21)
})

const withChipEventsValue = shallowRef(new CalendarDate(2012, 4, 12))

// region With min/max dates ////
const withMinMaxValue = shallowRef(new CalendarDate(2012, 4, 12))
const minDate = new CalendarDate(2012, 4, 1)
const maxDate = new CalendarDate(2012, 4, 30)
// endregion ////

// region As a DatePicker ////
const df = new DateFormatter('en-US', {
  dateStyle: 'medium'
})
const datePickerValue = shallowRef(new CalendarDate(2012, 4, 12))
const datePickerRangeValue = shallowRef({
  start: new CalendarDate(2012, 4, 12),
  end: new CalendarDate(2012, 5, 12)
})
// endregion ////

const airColors = computed(() => {
  return colors.filter((color) => {
    return color.includes('air')
  })
})

// region Helpers ////
function getColorByDate(date: Date) {
  const isWeekend = date.getDay() % 6 == 0
  const isDayMeeting = date.getDay() % 3 == 0

  if (isWeekend) {
    return undefined
  }

  if (isDayMeeting) {
    return 'air-primary-alert'
  }

  return 'air-primary-success'
}
const withDisabledDatesValue = shallowRef({
  start: new CalendarDate(2012, 4, 12),
  end: new CalendarDate(2012, 4, 14)
})
const isDateDisabled = (date: DateValue) => {
  return date.day >= 15 && date.day <= 17
}

const withUnavailableDatesValue = shallowRef({
  start: new CalendarDate(2012, 4, 12),
  end: new CalendarDate(2012, 4, 14)
})
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
      <B24Separator orientation="vertical" class="h-10" />
      <B24Switch v-model="attrs.multiple" label="Multiple" size="xs" />
      <B24Switch v-model="attrs.range" label="Range" size="xs" />
    </template>

    <template #default="{ playground }">
      <Matrix v-slot="props" :attrs="attrs">
        <B24Calendar v-bind="props" />
      </Matrix>

      <ExampleGrid v-once>
        <ExampleCard title="v-model" :use-bg="playground.isUseBg.value">
          <B24Separator class="my-3" type="dotted" />
          <div class="mb-4 max-w-[250px] mx-auto">
            <B24Calendar v-model="value" />
          </div>
        </ExampleCard>

        <ExampleCard title="default-value" :use-bg="playground.isUseBg.value">
          <B24Separator class="my-3" type="dotted" />
          <div class="mb-4 max-w-[250px] mx-auto">
            <B24Calendar :default-value="defaultValue" />
          </div>
        </ExampleCard>

        <ExampleCard title="as a date picker" :use-bg="playground.isUseBg.value">
          <B24Separator class="my-3" type="dotted" />
          <div class="mb-4 flex flex-row flex-wrap items-start justify-start gap-4">
            <B24Popover :content="{ align: 'start', side: 'bottom' }">
              <B24Button :icon="Calendar1Icon">
                <div class="truncate">
                  {{ datePickerValue ? df.format(datePickerValue.toDate(getLocalTimeZone())) : 'Select a date' }}
                </div>
              </B24Button>

              <template #content>
                <B24Calendar v-model="datePickerValue" class="p-2" />
              </template>
            </B24Popover>

            <B24Popover :content="{ align: 'start', side: 'bottom' }">
              <B24Button :icon="Calendar1Icon">
                <template v-if="datePickerRangeValue.start">
                  <div v-if="datePickerRangeValue.end" class="truncate">
                    {{ df.format(datePickerRangeValue.start.toDate(getLocalTimeZone())) }} - {{ df.format(datePickerRangeValue.end.toDate(getLocalTimeZone())) }}
                  </div>

                  <div v-else class="truncate">
                    {{ df.format(datePickerRangeValue.start.toDate(getLocalTimeZone())) }}
                  </div>
                </template>
                <template v-else>
                  Pick a date
                </template>
              </B24Button>

              <template #content>
                <B24Calendar
                  v-model="datePickerRangeValue"
                  class="p-2"
                  :number-of-months="2"
                  range
                />
              </template>
            </B24Popover>
          </div>
        </ExampleCard>

        <ExampleCard title="multiple" :use-bg="playground.isUseBg.value">
          <B24Separator class="my-3" type="dotted" />
          <div class="mb-4 max-w-[250px] mx-auto">
            <B24Calendar v-model="valueMultiple" multiple />
          </div>
        </ExampleCard>

        <ExampleCard title="range" :use-bg="playground.isUseBg.value">
          <B24Separator class="my-3" type="dotted" />
          <div class="mb-4 max-w-[250px] mx-auto">
            <B24Calendar v-model="valueRange" range />
          </div>
        </ExampleCard>

        <ExampleCard title="disabled" :use-bg="playground.isUseBg.value">
          <B24Separator class="my-3" type="dotted" />
          <div class="mb-4 max-w-[250px] mx-auto">
            <B24Calendar disabled />
          </div>
        </ExampleCard>

        <ExampleCard title="with chip events" :use-bg="playground.isUseBg.value">
          <B24Separator class="my-3" type="dotted" />
          <div class="mb-4 max-w-[250px] mx-auto">
            <B24Calendar v-model="withChipEventsValue">
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
          </div>
        </ExampleCard>

        <ExampleCard title="with disabled dates" :use-bg="playground.isUseBg.value">
          <B24Separator class="my-3" type="dotted" />
          <div class="mb-4 max-w-[250px] mx-auto">
            <B24Calendar
              v-model="withDisabledDatesValue"
              :is-date-disabled="isDateDisabled"
              range
            />
          </div>
        </ExampleCard>

        <ExampleCard title="with unavailable dates" :use-bg="playground.isUseBg.value">
          <B24Separator class="my-3" type="dotted" />
          <div class="mb-4 max-w-[250px] mx-auto">
            <B24Calendar
              v-model="withUnavailableDatesValue"
              :is-date-unavailable="isDateUnavailable"
              range
            />
          </div>
        </ExampleCard>

        <ExampleCard title="with min/max dates" :use-bg="playground.isUseBg.value">
          <B24Separator class="my-3" type="dotted" />
          <div class="mb-4 max-w-[250px] mx-auto">
            <B24Calendar
              v-model="withMinMaxValue"
              :min-value="minDate"
              :max-value="maxDate"
            />
          </div>
        </ExampleCard>
      </ExampleGrid>

      <B24Separator accent="accent" class="my-4" label="Some months" type="dotted" />
      <ExampleGrid>
        <ExampleCard title="numberOfMonths" :use-bg="playground.isUseBg.value" class="sm:col-span-2">
          <B24Separator class="my-3" type="dotted" />
          <div class="mb-4 max-w-[500px] mx-auto">
            <B24Calendar :number-of-months="2" />
          </div>
        </ExampleCard>
      </ExampleGrid>
    </template>
  </PlaygroundPage>
</template>
