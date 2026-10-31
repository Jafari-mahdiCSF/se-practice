/* Wiring only: read the fields, ask availability.js for the decision, render the answer. */

const roomSelect = document.getElementById("room");
const scenarioSelect = document.getElementById("scenario");
const nowInput = document.getElementById("now");
const startInput = document.getElementById("start");
const endInput = document.getElementById("end");
const endOfDayInput = document.getElementById("end-of-day");
const checkButton = document.getElementById("check");
const resultBox = document.getElementById("result");
const roomStatus = document.getElementById("room-status");
const bookingsList = document.getElementById("bookings");
const roomLabel = document.getElementById("room-label");
const dataStatus = document.getElementById("data-status");

let checksThisSession = 0;

function currentRoom() {
  return ROOMS.find(function (room) {
    return room.id === roomSelect.value;
  });
}

function bookingsFor(roomId) {
  return SAMPLE_BOOKINGS.filter(function (booking) {
    return booking.roomId === roomId;
  }).sort(function (a, b) {
    return a.start - b.start;
  });
}

function clockNow() {
  const today = new Date();
  return String(today.getHours()).padStart(2, "0") + ":" +
    String(today.getMinutes()).padStart(2, "0");
}

function readRequest() {
  return {
    room: currentRoom(),
    startText: startInput.value,
    endText: endOfDayInput.checked ? "24:00" : endInput.value,
    nowText: nowInput.value,
    bookings: SAMPLE_BOOKINGS
  };
}

function renderRooms() {
  roomSelect.innerHTML = "";
  ROOMS.forEach(function (room) {
    const option = document.createElement("option");
    option.value = room.id;
    option.textContent = room.name + (room.blocked ? " (blocked)" : "");
    roomSelect.appendChild(option);
  });
}

function updateRoomStatus() {
  const room = currentRoom();
  if (room.blocked) {
    roomStatus.textContent = "This room is blocked" + (room.note ? " (" + room.note + ")" : "") +
      ", so every check on it answers Unavailable.";
    roomStatus.className = "hint blocked";
    return;
  }
  const count = bookingsFor(room.id).length;
  roomStatus.textContent = "Not blocked. " + count +
    (count === 1 ? " existing booking" : " existing bookings") + " in the sample data.";
  roomStatus.className = "hint";
}

function renderBookings() {
  const room = currentRoom();
  roomLabel.textContent = room.name;
  bookingsList.innerHTML = "";
  const list = bookingsFor(room.id);
  if (list.length === 0) {
    const empty = document.createElement("li");
    empty.textContent = "No bookings in the sample data.";
    bookingsList.appendChild(empty);
    return;
  }
  list.forEach(function (booking) {
    const item = document.createElement("li");
    item.textContent = clockText(booking.start) + " - " + clockText(booking.end);
    bookingsList.appendChild(item);
  });
}

function showDecision(decision) {
  resultBox.dataset.state = decision.available ? "available" : "unavailable";
  resultBox.className = "result " + (decision.available ? "ok" : "no");

  const head = document.createElement("p");
  head.className = "result-head";
  head.textContent = decision.headline;

  const detail = document.createElement("p");
  detail.className = "result-detail";
  detail.textContent = decision.detail;

  resultBox.innerHTML = "";
  resultBox.appendChild(head);
  resultBox.appendChild(detail);
}

function updateDataStatus() {
  const room = currentRoom();
  const count = bookingsFor(room.id).length;
  dataStatus.textContent = "Booking data: " + count + (count === 1 ? " booking" : " bookings") +
    " for this room, unchanged by the check. Checks on this page load: " + checksThisSession + ".";
}

checkButton.addEventListener("click", function () {
  checksThisSession += 1;
  showDecision(decideAvailability(readRequest()));
  updateDataStatus();
});

function applyScenario() {
  const key = scenarioSelect.value;
  const source = SAMPLE_SETS[key] || SAMPLE_STANDARD;
  SAMPLE_BOOKINGS = source.map(function (booking) {
    return { roomId: booking.roomId, start: booking.start, end: booking.end };
  });
  renderBookings();
  updateRoomStatus();
  updateDataStatus();
}

roomSelect.addEventListener("change", function () {
  renderBookings();
  updateRoomStatus();
  updateDataStatus();
});

scenarioSelect.addEventListener("change", applyScenario);

endOfDayInput.addEventListener("change", function () {
  endInput.disabled = endOfDayInput.checked;
});

nowInput.value = clockNow();
renderRooms();
renderBookings();
updateRoomStatus();
updateDataStatus();
