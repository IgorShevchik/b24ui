import { splitByCase, upperFirst } from 'scule'

export const normalizePath = (p: string) => (p.endsWith('/') ? p.slice(0, -1) : p)

export function upperName(name: string) {
  return splitByCase(name).map(p => upperFirst(p)).join('')
}
