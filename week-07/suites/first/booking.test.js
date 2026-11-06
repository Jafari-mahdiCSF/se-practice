import { describe, test, expect } from "vitest";
import { canBook } from "./booking";

function fixture(overrides) {
  return {
    now: 540,
    blocked: false,
    bookings: [{ start: 600, end: 660 }],
    ...overrides
  };
}

describe("canBook", () => {
  test("T01 AC4: touching after the existing booking", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 660, end: 720, now, blocked, bookings })).toBe(true);
  });

  test("T02 AC1: starts now", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 540, end: 570, now, blocked, bookings })).toBe(false);
  });

  test("T03 AC1: zero duration", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 720, end: 720, now, blocked, bookings })).toBe(false);
  });

  test("T04 AC1: reversed times", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 750, end: 720, now, blocked, bookings })).toBe(false);
  });

  test("T05 AC1: past the end of the day", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 1380, end: 1441, now, blocked, bookings })).toBe(false);
  });

  test("T06 AC2: two hours", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 720, end: 840, now, blocked, bookings })).toBe(false);
  });

  test("T07 AC2: over two hours", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 720, end: 841, now, blocked, bookings })).toBe(false);
  });

  test("T08 AC4: touching before the existing booking", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 570, end: 600, now, blocked, bookings })).toBe(true);
  });

  test("T09 AC4: partial overlap", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 630, end: 690, now, blocked, bookings })).toBe(false);
  });

  test("T10 AC4: contains the existing booking", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 570, end: 690, now, blocked, bookings })).toBe(false);
  });

  test("T11 AC4: inside the existing booking", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 615, end: 645, now, blocked, bookings })).toBe(false);
  });

  test("T12 AC4: identical interval", () => {
    const { now, blocked, bookings } = fixture();
    expect(canBook({ start: 600, end: 660, now, blocked, bookings })).toBe(false);
  });

  test("T13 AC3: blocked room", () => {
    const { now, bookings } = fixture();
    expect(canBook({ start: 660, end: 720, now, blocked: true, bookings })).toBe(false);
  });

  test("T14 AC4: overlap shape with no bookings", () => {
    const { now, blocked } = fixture();
    expect(canBook({ start: 630, end: 690, now, blocked, bookings: [] })).toBe(true);
  });
});
