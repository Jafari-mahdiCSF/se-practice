# Acceptance criteria — three selected stories

Assumptions first, then the criteria. The selected stories are US-01, US-02, and US-04.

## Assumptions

- **Overlap:** a booking that ends exactly when another begins is allowed under R3, because the
  occupied intervals share no time.
- **Duration:** a booking of exactly two hours is allowed under R2, because two hours is the stated
  maximum duration.
- A blocked room is unavailable for new bookings until an administrator unblocks it.

## US-01 — View available rooms and time slots

### AC-01
- **Given** a student searches for a future date and time
- **When** the student requests room availability
- **Then** the system lists rooms that have no booking overlapping that requested period and are not blocked

### AC-02
- **Given** a room has a booking that overlaps the requested period
- **When** the student requests room availability
- **Then** that room is shown as unavailable for the period

### AC-03
- **Given** the requested start time is in the past
- **When** the student requests availability for that period
- **Then** the system rejects the request and explains that the booking period must be in the future

## US-02 — Book an available room

### AC-04
- **Given** a student selects an unblocked room and a future slot of exactly two hours with no overlap
- **When** the student submits the booking
- **Then** the system records the booking for that room and slot

### AC-05
- **Given** a selected booking starts in the past or lasts longer than two hours
- **When** the student submits the booking
- **Then** the system rejects it and does not create a reservation

### AC-06
- **Given** another booking for the same room overlaps the selected slot
- **When** the student submits the booking
- **Then** the system rejects it and leaves the existing booking unchanged

## US-04 — Block or unblock a study room

### AC-07
- **Given** an administrator selects an unblocked room
- **When** the administrator blocks the room
- **Then** the room is marked unavailable for new bookings

### AC-08
- **Given** a room is blocked
- **When** a student attempts to book it
- **Then** the system rejects the booking and keeps the room blocked

### AC-09
- **Given** an administrator selects a blocked room
- **When** the administrator unblocks the room
- **Then** the room becomes eligible for future bookings that satisfy the booking rules
