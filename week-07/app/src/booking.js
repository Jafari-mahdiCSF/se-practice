export function canBook({ start, end, now, blocked, bookings }) {
  if (blocked) {
    return false;
  }
  if (!(start >= 0 && start < end && end <= 1440)) {
    return false;
  }
  if (start <= now) {
    return false;
  }
  if (end - start > 120) {
    return false;
  }
  for (let i = 0; i < bookings.length; i++) {
    const booking = bookings[i];
    if (start < booking.end && end > booking.start) {
      return false;
    }
  }
  return true;
}
