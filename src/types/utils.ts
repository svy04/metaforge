type Primitive = string | number | boolean | bigint | symbol | null | undefined

export type DeepImmutable<T> = T extends Primitive
  ? T
  : T extends (...args: never[]) => unknown
    ? T
    : T extends ReadonlyMap<infer K, infer V>
      ? ReadonlyMap<DeepImmutable<K>, DeepImmutable<V>>
      : T extends ReadonlySet<infer V>
        ? ReadonlySet<DeepImmutable<V>>
        : T extends readonly (infer V)[]
          ? readonly DeepImmutable<V>[]
          : T extends object
            ? { readonly [K in keyof T]: DeepImmutable<T[K]> }
            : T

export type Permutations<T, U = T> = [T] extends [never]
  ? []
  : T extends U
    ? [T, ...Permutations<Exclude<U, T>>]
    : never
