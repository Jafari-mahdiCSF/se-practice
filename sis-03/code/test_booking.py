import unittest
from booking import can_book


NOW = 540
EXISTING = [(600, 660)]


class BookingTests(unittest.TestCase):
    def test_touching_end_is_allowed(self):
        self.assertIs(can_book(660, 720, NOW, False, EXISTING), True)

    def test_touching_start_is_allowed(self):
        self.assertIs(can_book(570, 600, NOW, False, EXISTING), True)

    def test_partial_overlap_over_end_is_rejected(self):
        self.assertIs(can_book(630, 690, NOW, False, EXISTING), False)

    def test_partial_overlap_over_start_is_rejected(self):
        self.assertIs(can_book(570, 630, NOW, False, EXISTING), False)

    def test_inside_existing_booking_is_rejected(self):
        self.assertIs(can_book(615, 645, NOW, False, EXISTING), False)

    def test_containing_existing_booking_is_rejected(self):
        self.assertIs(can_book(570, 690, NOW, False, EXISTING), False)

    def test_identical_to_existing_booking_is_rejected(self):
        self.assertIs(can_book(600, 660, NOW, False, EXISTING), False)

    def test_blocked_room_is_rejected(self):
        self.assertIs(can_book(660, 720, NOW, True, EXISTING), False)

    def test_blocked_room_with_no_bookings_is_rejected(self):
        self.assertIs(can_book(660, 720, NOW, True, []), False)

    def test_exactly_two_hours_is_allowed(self):
        self.assertIs(can_book(720, 840, NOW, False, EXISTING), True)

    def test_over_two_hours_is_rejected(self):
        self.assertIs(can_book(720, 841, NOW, False, EXISTING), False)

    def test_one_minute_duration_is_allowed(self):
        self.assertIs(can_book(720, 721, NOW, False, EXISTING), True)

    def test_starts_now_is_rejected(self):
        self.assertIs(can_book(540, 570, NOW, False, EXISTING), False)

    def test_starts_one_minute_after_now_is_allowed(self):
        self.assertIs(can_book(541, 571, NOW, False, []), True)

    def test_starts_in_the_past_is_rejected(self):
        self.assertIs(can_book(500, 530, NOW, False, EXISTING), False)

    def test_now_zero_start_zero_is_rejected(self):
        self.assertIs(can_book(0, 60, 0, False, []), False)

    def test_now_zero_start_one_is_allowed(self):
        self.assertIs(can_book(1, 61, 0, False, []), True)

    def test_zero_length_is_rejected(self):
        self.assertIs(can_book(700, 700, NOW, False, []), False)

    def test_reversed_interval_is_rejected(self):
        self.assertIs(can_book(720, 660, NOW, False, EXISTING), False)

    def test_negative_start_is_rejected(self):
        self.assertIs(can_book(-30, 30, NOW, False, []), False)

    def test_day_end_is_allowed(self):
        self.assertIs(can_book(1380, 1440, NOW, False, EXISTING), True)

    def test_after_day_end_is_rejected(self):
        self.assertIs(can_book(1380, 1441, NOW, False, EXISTING), False)

    def test_empty_existing_allows_valid_request(self):
        self.assertIs(can_book(600, 660, NOW, False, []), True)

    def test_second_booking_is_checked(self):
        self.assertIs(
            can_book(720, 780, NOW, False, [(600, 660), (700, 760)]),
            False,
        )

    def test_unsorted_existing_is_checked(self):
        self.assertIs(
            can_book(610, 650, NOW, False, [(900, 960), (600, 660)]),
            False,
        )

    def test_fits_exactly_between_two_bookings(self):
        self.assertIs(
            can_book(660, 720, NOW, False, [(600, 660), (720, 780)]),
            True,
        )

    def test_free_slot_among_three_is_allowed(self):
        self.assertIs(
            can_book(760, 800, NOW, False, [(600, 660), (700, 760), (800, 860)]),
            True,
        )

    def test_same_check_twice_stays_allowed(self):
        existing = [(600, 660)]
        first = can_book(660, 720, NOW, False, existing)
        second = can_book(660, 720, NOW, False, existing)
        self.assertIs(first, True)
        self.assertIs(second, True)
        self.assertEqual(existing, [(600, 660)])

    def test_existing_input_is_unchanged(self):
        existing = [(900, 960), (600, 660), (700, 760)]
        original = list(existing)
        self.assertIs(can_book(780, 840, NOW, False, existing), True)
        self.assertEqual(existing, original)

    def test_rejected_request_leaves_existing_unchanged(self):
        existing = [(900, 960), (600, 660), (700, 760)]
        original = list(existing)
        self.assertIs(can_book(610, 650, NOW, False, existing), False)
        self.assertEqual(existing, original)

    def test_result_is_real_boolean_true(self):
        result = can_book(660, 720, NOW, False, EXISTING)
        self.assertIs(result, True)
        self.assertEqual(type(result).__name__, "bool")

    def test_result_is_real_boolean_false(self):
        result = can_book(630, 690, NOW, False, EXISTING)
        self.assertIs(result, False)
        self.assertEqual(type(result).__name__, "bool")


if __name__ == "__main__":
    unittest.main()
