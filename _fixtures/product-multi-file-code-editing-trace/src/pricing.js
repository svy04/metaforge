export function subtotal(lines) {
  return lines.reduce((sum, line) => sum + (line.price * line.quantity), 0)
}
