import unittest
import Rbx1cnc

class FakeAxisTest(unittest.TestCase):

    def new_fake_is_not_busy(self):
        fake = Rbx1cnc.FakeAxis(False)
        self.assertFalse(fake.isBusy())

    def new_fake_have_pos_0(self):
        fake = Rbx1cnc.FakeAxis(False)
        self.assertEqual(fake.getPosition(), 0)

    def test_move(self):
        fake = Rbx1cnc.FakeAxis(False)
        fake.goTo(10)
        self.assertTrue(fake.isBusy())
        fake._update();
        self.assertFalse(fake.isBusy())
        self.assertEqual(fake.getPosition(), 10)

    def test_move_negative(self):
        fake = Rbx1cnc.FakeAxis(False)
        fake.goTo(-10)
        fake._update();
        self.assertEqual(fake.getPosition(), -10)

    def test_longmove(self):
        fake = Rbx1cnc.FakeAxis(False)
        fake.goTo(20)
        fake._update();
        self.assertEqual(fake.getPosition(), 15)
        fake._update();
        self.assertEqual(fake.getPosition(), 20)

    def test_longmove_negative(self):
        fake = Rbx1cnc.FakeAxis(False)
        fake.goTo(-20)
        fake._update();
        self.assertEqual(fake.getPosition(), -15)
        fake._update();
        self.assertEqual(fake.getPosition(), -20)
