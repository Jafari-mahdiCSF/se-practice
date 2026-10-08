import unittest
from booking import can_book


class BookingTests(unittest.TestCase):
    def test_touching_end_is_allowed(self):
        result = can_book(660, 720, 540, False, [(600, 660)])
        self.assertIs(result, True)

    def test_partial_overlap_over_end_is_rejected(self):
        self.assertIs(can_book(630, 690, 540, False, [(600, 660)]), False)

    def test_partial_overlap_over_start_is_rejected(self):
        self.assertIs(can_book(570, 630, 540, False, [(600, 660)]), False)

    def test_inside_existing_booking_is_rejected(self):
        self.assertIs(can_book(615, 645, 540, False, [(600, 660)]), False)

    def test_containing_existing_booking_is_rejected(self):
        self.assertIs(can_book(570, 690, 540, False, [(600, 660)]), False)

    def test_blocked_room_is_rejected(self):
        self.assertIs(can_book(660, 720, 540, True, [(600, 660)]), False)

    def test_exactly_two_hours_is_allowed(self):
        self.assertIs(can_book(720, 840, 540, False, [(600, 660)]), True)

    def test_over_two_hours_is_rejected(self):
        self.assertIs(can_book(720, 841, 540, False, [(600, 660)]), False)

    def test_starts_now_is_rejected(self):
        self.assertIs(can_book(540, 570, 540, False, [(600, 660)]), False)

    def test_zero_length_is_rejected(self):
        self.assertIs(can_book(700, 700, 540, False, []), False)

    def test_reversed_interval_is_rejected(self):
        self.assertIs(can_book(720, 700, 540, False, []), False)

    def test_day_end_is_allowed(self):
        self.assertIs(can_book(1320, 1440, 540, False, []), True)

    def test_after_day_end_is_rejected(self):
        self.assertIs(can_book(1320, 1441, 540, False, []), False)

    def test_empty_existing_allows_valid_request(self):
        self.assertIs(can_book(600, 660, 540, False, []), True)

    def test_second_booking_is_checked(self):
        self.assertIs(
            can_book(720, 780, 540, False, [(600, 660), (700, 760)]),
            False,
        )

    def test_existing_input_is_unchanged(self):
        existing = [(900, 960), (600, 660), (700, 760)]
        original = list(existing)
        self.assertIs(can_book(780, 840, 540, False, existing), True)
        self.assertEqual(existing, original)
