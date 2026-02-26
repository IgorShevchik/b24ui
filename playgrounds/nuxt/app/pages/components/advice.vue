<script setup lang="ts">
import theme from '#build/b24ui/advice'
import InfoIcon from '@bitrix24/b24icons-vue/button/InfoIcon'
import MoreMIcon from '@bitrix24/b24icons-vue/outline/MoreMIcon'

const angles = Object.keys(theme.variants.angle)

const multipleAttrs = reactive({
  angle: [theme.defaultVariants.angle]
})

const singleAttrs = reactive({
  useIcon: false,
  useAvatar: false
})

const description = ref('Let\'s signal the manager that the deal is not moving, the manager does not call the client back and does not respond to his messages. Let\'s assign a task to the manager on behalf of the manager')
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Select
        v-model="multipleAttrs.angle"
        class="w-44"
        :items="angles"
        placeholder="Angle"
        multiple
      />
      <B24Switch v-model="singleAttrs.useIcon" label="Icon" />
      <B24Switch v-model="singleAttrs.useAvatar" label="Avatar" />
    </template>

    <Matrix
      v-slot="props"
      :attrs="multipleAttrs"
      :b24ui="{ root: 'max-w-180' }"
    >
      <B24Advice
        :description="description"
        :icon="singleAttrs.useIcon ? InfoIcon : undefined"
        :avatar="
          singleAttrs.useAvatar
            ? { src: '/avatar/assistant.png' }
            : undefined
        "
        v-bind="props"
      />

      <B24Advice
        :avatar="
          singleAttrs.useAvatar
            ? { src: '/avatar/employee.png' }
            : undefined
        "
        :icon="singleAttrs.useIcon ? InfoIcon : undefined"
        v-bind="props"
      >
        <div class="flex flex-col items-start justify-between gap-1.5">
          <div class="font-(--ui-font-weight-bold)">Reference information</div>
          <div>
            Typically, instructions on how to add a SAML application and add the
            ACS URL and SP Entity ID can be found in the Microsoft Azure
            technical documentation.
          </div>
          <B24Link to="/components/advice"> Read more </B24Link>
          <div
            class="mt-2 flex flex-row flex-wrap items-start justify-between gap-2"
          >
            <B24Button size="sm" color="primary" label="some action 1" />
            <B24Button size="sm" color="link" label="some action 2" />
            <B24Button size="sm" color="link" :icon="MoreMIcon" />
          </div>
        </div>
      </B24Advice>
    </Matrix>
  </PlaygroundPage>
</template>
