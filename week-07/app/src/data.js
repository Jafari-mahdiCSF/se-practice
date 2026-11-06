/* Fictional sample data. Nothing here comes from a server, and nothing here is written by the page. */

const ROOMS = [
  { id: "a101", name: "A-101 \u00b7 Lecture Hall", blocked: false, note: "" },
  { id: "b214", name: "B-214 \u00b7 Study Room", blocked: true, note: "maintenance until 20 October" },
  { id: "c305", name: "C-305 \u00b7 Computer Lab", blocked: false, note: "" }
];

const SAMPLE_BOOKINGS = [
  { roomId: "a101", start: 600, end: 660 },
  { roomId: "c305", start: 780, end: 840 }
];
