<script setup lang="ts">
import MagicWandIcon from '@bitrix24/b24icons-vue/outline/MagicWandIcon'

const myCanvas = ref<HTMLCanvasElement | undefined>()
const confetti = useConfetti()

const particleCount = ref(100)
const spread = ref(70)
const originY = ref(0.6)
const originX = ref(0.5)

function fireConfetti(): void {
  confetti.fire()
}

function fireConfettiWithOptions(): void {
  confetti.create()
  confetti.fire({
    particleCount: particleCount.value,
    spread: spread.value,
    origin: { y: originY.value, x: originX.value }
  })
}

function fireAtPlace(): void {
  const confettiInstance = confetti.create(myCanvas.value, { resize: true })
  confettiInstance({
    particleCount: particleCount.value,
    spread: spread.value
  })
}
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24FormField label="particleCount" orientation="horizontal">
        <B24Input v-model.number="particleCount" type="number" class="w-24" />
      </B24FormField>
      <B24FormField label="spread" orientation="horizontal">
        <B24Input v-model.number="spread" type="number" class="w-24" />
      </B24FormField>
      <B24FormField label="originY" orientation="horizontal">
        <B24Input v-model.number="originY" type="number" step="0.1" class="w-24" />
      </B24FormField>
      <B24FormField label="originX" orientation="horizontal">
        <B24Input v-model.number="originX" type="number" step="0.1" class="w-24" />
      </B24FormField>
    </template>

    <template #default="{ cardVariant, cardBorderClass }">
      <canvas ref="myCanvas" class="z-0 absolute size-full" />
      <B24Card
        :variant="cardVariant"
        :class="[cardBorderClass, 'max-w-[550px] w-full mx-auto']"
        :b24ui="{
          body: 'flex flex-col items-center justify-center gap-2.5 px-15 py-10 text-center'
        }"
      >
        <B24Avatar
          :icon="MagicWandIcon"
          alt="useConfetti"
          size="3xl"
          :b24ui="{
            root: 'bg-transparent ring-2 ring-(--ui-color-design-outline-na-content-icon)',
            icon: 'size-[74px] text-(--ui-color-design-outline-na-content-icon)'
          }"
        />
        <ProseH2 class="leading-[29px] mb-0">
          useConfetti
        </ProseH2>
        <ProseP accent="less">
          Performant confetti animation in the browser
        </ProseP>
        <div class="flex flex-col sm:flex-row items-center justify-center gap-3.75">
          <B24Button label="Simple" color="air-primary" @click.stop="fireConfetti" />
          <B24Button label="With options" color="air-secondary-accent-2" @click.stop="fireConfettiWithOptions" />
          <B24Button label="Custom canvas" color="air-secondary-accent-2" @click.stop="fireAtPlace" />
        </div>
      </B24Card>
    </template>
  </PlaygroundPage>
</template>
