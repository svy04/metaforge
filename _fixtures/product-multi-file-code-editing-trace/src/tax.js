export const TAX_RATE = 0.1

export function calculateTax(subtotal) {
  return subtotal * TAX_RATE
}
