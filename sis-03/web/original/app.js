/* Smart Campus room availability checker - first version. */

const ROOMS = [
  { id: "a101", name: "A-101 \u00b7 Lecture Hall", blocked: false },
  { id: "b214", name: "B-214 \u00b7 Study Room", blocked: true },
  { id: "c305", name: "C-305 \u00b7 Computer Lab", blocked: false }
];

const STORAGE_KEY = "smart-campus-bookings";

const SAMPLE_BOOKINGS = [
  { roomId: "a101", start: 600, end: 660 },
  { roomId: "c305", start: 780, end: 840 }
];

const roomSelect = document.getElementById("room");
const startInput = document.getElementById("start");
const endInput = document.getElementById("end");
const resultBox = document.getElementById("result");
const bookingsList = document.getElementById("bookings");
const roomLabel = document.getElementById("room-label");

let bookings = readBookings();

function readBookings() {
  try {
    const saved = window.localStorage.getItem(STORAGE_KEY);
    if (saved) {
      return JSON.parse(saved);
    }
  } catch (error) {
    /* fall back to the sample data */
  }
  return SAMPLE_BOOKINGS.map(function (booking) {
    return { roomId: booking.roomId, start: booking.start, end: booking.end };
  });
}

function writeBookings() {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(bookings));
}

function toMinutes(text) {
  if (!text) {
    return null;
  }
  const parts = text.split(":");
  return Number(parts[0]) * 60 + Number(parts[1]);
}

function toClock(minutes) {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return String(hours).padStart(2, "0") + ":" + String(mins).padStart(2, "0");
}

function currentRoom() {
  return ROOMS.find(function (room) {
    return room.id === roomSelect.value;
  });
}

function bookingsFor(roomId) {
  return bookings
    .filter(function (booking) {
      return booking.roomId === roomId;
    })
    .sort(function (a, b) {
      return a.start - b.start;
    });
}

function renderRooms() {
  roomSelect.innerHTML = "";
  ROOMS.forEach(function (room) {
    const option = document.createElement("option");
    option.value = room.id;
    option.textContent = room.name;
    roomSelect.appendChild(option);
  });
}

function renderBookings() {
  const room = currentRoom();
  roomLabel.textContent = room.name;
  bookingsList.innerHTML = "";
  const list = bookingsFor(room.id);
  if (list.length === 0) {
    const empty = document.createElement("li");
    empty.textContent = "No bookings yet.";
    bookingsList.appendChild(empty);
    return;
  }
  list.forEach(function (booking) {
    const item = document.createElement("li");
    item.textContent = toClock(booking.start) + " - " + toClock(booking.end);
    bookingsList.appendChild(item);
  });
}

function showResult(text, available) {
  resultBox.textContent = text;
  resultBox.className = "result " + (available ? "ok" : "no");
}

function checkAvailability() {
  const room = currentRoom();
  const start = toMinutes(startInput.value);
  const end = toMinutes(endInput.value);

  if (start === null || end === null) {
    showResult("Choose a start time and an end time.", false);
    return;
  }

  if (end - start > 120) {
    showResult("Not available for this slot.", false);
    return;
  }

  const clash = bookingsFor(room.id).some(function (booking) {
    return start < booking.end && end > booking.start;
  });

  if (clash) {
    showResult("Not available for this slot.", false);
    return;
  }

  showResult("Available - " + toClock(start) + " to " + toClock(end), true);

  /* Keep the slot reserved while the student confirms the booking. */
  bookings.push({ roomId: room.id, start: start, end: end });
  writeBookings();
  renderBookings();
}

function bookSlot() {
  const room = currentRoom();
  const start = toMinutes(startInput.value);
  const end = toMinutes(endInput.value);

  if (start === null || end === null) {
    showResult("Choose a start time and an end time.", false);
    return;
  }

  bookings.push({ roomId: room.id, start: start, end: end });
  writeBookings();
  renderBookings();
  showResult("Booked " + toClock(start) + " to " + toClock(end) + " (prototype only).", true);
}

document.getElementById("check").addEventListener("click", checkAvailability);
document.getElementById("book").addEventListener("click", bookSlot);
roomSelect.addEventListener("change", renderBookings);

renderRooms();
renderBookings();
