import { subtotal } from './pricing.js'
import { calculateTax } from './tax.js'

export function checkoutTotal(lines) {
  const beforeTax = subtotal(lines)
  return beforeTax + calculateTax(beforeTax)
}
