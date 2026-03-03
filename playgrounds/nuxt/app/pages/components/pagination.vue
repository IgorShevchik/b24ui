<script setup lang="ts">
const attrs = reactive({
  siblingCount: 1,
  showEdges: true,
  showControls: true
})

const page = ref(5)
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24FormField label="Siblings" orientation="horizontal">
        <B24InputNumber v-model="attrs.siblingCount" class="w-20" :min="0" :max="3" />
      </B24FormField>
      <B24Switch v-model="attrs.showControls" label="Show controls" />
      <B24Switch v-model="attrs.showEdges" label="Show edges" />
    </template>

    <template #default="{ cardVariant, cardBorderClass }">
      <B24Card :variant="cardVariant" :class="[cardBorderClass]" :b24ui="{ body: 'overflow-x-auto' }">
        <template #header>
          <ProseH5 class="mb-0">
            With buttons
          </ProseH5>
        </template>
        <B24Pagination
          v-model:page="page"
          :total="100"
          v-bind="attrs"
        />
      </B24Card>
      <B24Card :variant="cardVariant" :class="[cardBorderClass]" :b24ui="{ body: 'overflow-x-auto' }">
        <template #header>
          <ProseH5 class="mb-0">
            With links
          </ProseH5>
        </template>
        <B24Pagination
          v-model:page="page"
          :total="100"
          :to="page => ({ query: { page } })"
          v-bind="attrs"
        />
      </B24Card>
    </template>
  </PlaygroundPage>
</template>
