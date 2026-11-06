/*
 * The one place where availability is decided (AC1-AC5).
 * decideAvailability() takes the request, walks the rules in a fixed order and returns
 * { available, headline, detail }. It never touches the page and never writes anything.
 */

const MAX_BOOKING_MINUTES = 120;
const END_OF_DAY = 1440;

function parseClock(text) {
  const match = /^(\d{1,2}):(\d{2})$/.exec(String(text || "").trim());
  if (!match) {
    return null;
  }
  const hours = Number(match[1]);
  const minutes = Number(match[2]);
  if (minutes > 59) {
    return null;
  }
  if (hours === 24) {
    return minutes === 0 ? END_OF_DAY : null;
  }
  if (hours > 23) {
    return null;
  }
  return hours * 60 + minutes;
}

function clockText(minutes) {
  if (minutes === END_OF_DAY) {
    return "24:00";
  }
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return String(hours).padStart(2, "0") + ":" + String(mins).padStart(2, "0");
}

function unavailable(detail) {
  return { available: false, headline: "Unavailable", detail: detail };
}

function decideAvailability(request) {
  const room = request.room;
  const start = parseClock(request.startText);
  const end = parseClock(request.endText);
  const now = parseClock(request.nowText);

  if (start === null) {
    return unavailable("The start must be a time like 11:00 (00:00 to 23:59).");
  }
  if (end === null) {
    return unavailable("The end must be a time like 12:00, or 24:00 for the end of the day.");
  }
  if (now === null) {
    return unavailable("Enter the current time as HH:MM so the check can compare with it.");
  }
  if (now === END_OF_DAY) {
    return unavailable("The current time cannot be 24:00.");
  }
  if (start === END_OF_DAY) {
    return unavailable("24:00 can only be the end of a slot, never the start.");
  }
  if (room.blocked) {
    return unavailable(room.name + " is blocked" + (room.note ? " (" + room.note + ")" : "") +
      ", so no window can be booked in it.");
  }
  if (start >= end) {
    return unavailable("Start " + clockText(start) + " is not before end " + clockText(end) +
      " - that window is reversed.");
  }
  if (end - start > MAX_BOOKING_MINUTES) {
    return unavailable("That window is " + (end - start) + " minutes long; the limit is " +
      MAX_BOOKING_MINUTES + " minutes.");
  }
  if (start <= now) {
    return unavailable("Start " + clockText(start) + " is not after the current time " +
      clockText(now) + ".");
  }

  const clash = request.bookings.find(function (booking) {
    return booking.roomId === room.id && start < booking.end && end > booking.start;
  });

  if (clash) {
    return unavailable("It overlaps the existing booking " + clockText(clash.start) + "-" +
      clockText(clash.end) + " in this room.");
  }

  return {
    available: true,
    headline: "Available",
    detail: clockText(start) + "-" + clockText(end) + " (" + (end - start) + " min) in " +
      room.name + ": it starts after " + clockText(now) +
      " and no existing booking overlaps it."
  };
}
