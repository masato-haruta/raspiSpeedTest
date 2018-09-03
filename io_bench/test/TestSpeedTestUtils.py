# coding:utf-8
import unittest
from io_bench.src.model.ValidationConst import ValidateConst
from io_bench.src.util.Utility import SpeedTestUtil


class TestSpeedTestUtils(unittest.TestCase):
    def test_get_trial_count_within_range(self):
        expected = 8
        actual = SpeedTestUtil.get_trial_count(8)
        self.assertEquals(expected, actual)

    def test_get_trial_count_out_of_range_over(self):
        expected = ValidateConst.DEFAULT_TRIAL_COUNT.value
        actual = SpeedTestUtil.get_trial_count(10000)
        self.assertEquals(expected, actual)

    def test_get_trial_count_out_of_range_minus(self):
        expected = ValidateConst.DEFAULT_TRIAL_COUNT.value
        actual = SpeedTestUtil.get_trial_count(-10000)
        self.assertEquals(expected, actual)

    def test_get_read_test_cmd_debug_on(self):
        expected = SpeedTestUtil.read_command_debug
        actual = SpeedTestUtil.get_read_test_cmd(True, '/dev/disk1')
        self.assertEquals(expected, actual)

    def test_get_read_test_cmd_debug_off(self):
        expected = SpeedTestUtil.read_command.format('/dev/disk1', '\'{print $11, $12}\'')
        actual = SpeedTestUtil.get_read_test_cmd(False, '/dev/disk1')
        self.assertEquals(expected, actual)

    def test_get_write_test_cmd_debug_on(self):
        expected = SpeedTestUtil.write_command_debug
        actual = SpeedTestUtil.get_write_test_cmd(True)
        self.assertEquals(expected, actual)

    def test_get_write_test_cmd_debug_off(self):
        expected = SpeedTestUtil.write_command
        actual = SpeedTestUtil.get_write_test_cmd(False)
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()
