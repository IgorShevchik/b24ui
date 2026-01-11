import { inject, provide, ref, type InjectionKey, type Ref } from 'vue'

export type PlaygroundContext = {
  isUseBg: Ref<boolean>
}

const PlaygroundContextKey: InjectionKey<PlaygroundContext> = Symbol('PlaygroundContext')

export function createPlaygroundContext(
  initial?: Partial<{
    isUseBg: boolean
  }>
): PlaygroundContext {
  return {
    isUseBg: ref(initial?.isUseBg ?? true)
  }
}

export function providePlaygroundContext(ctx: PlaygroundContext): PlaygroundContext {
  provide(PlaygroundContextKey, ctx)
  return ctx
}

export function usePlaygroundContext(): PlaygroundContext {
  const ctx = inject(PlaygroundContextKey)
  if (!ctx) {
    throw new Error('usePlaygroundContext() must be used inside provider')
  }
  return ctx
}
