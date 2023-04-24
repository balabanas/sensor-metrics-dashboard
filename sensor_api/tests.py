import unittest
import pandas as pd

from sensor_api.helpers import clean_string_values, get_sensors_df, get_metrics_df, get_types_df


class CleanStringTest(unittest.TestCase):
    def test_clean_string(self):
        data = {
            'col1': ['  string with leading space', 'string without space', '  ',
                     'another string with trailing space '],
            'col2': ['empty string', '', '  string with leading trailing space ', 'string without space'],
            'col3': ['some string', 'another string', '', '  ']
        }

        df = pd.DataFrame(data)
        df_new = clean_string_values(df)
        self.assertEqual('string with leading space', df_new.iloc[0]['col1'])
        self.assertEqual('string with leading trailing space', df_new.iloc[2]['col2'])
        self.assertIsNotNone(df_new.iloc[1]['col3'])
        self.assertIsNone(df_new.iloc[2]['col3'])
        self.assertIsNone(df_new.iloc[3]['col3'])


class ParseDataTest(unittest.TestCase):
    def test_read_parse_sensors(self):
        sensors_df = get_sensors_df('test_files/test_sensors.json')
        self.assertIsInstance(sensors_df, pd.DataFrame)
        substituted_sensor_name = sensors_df.loc[sensors_df['sensor_id'] == '6291474', 'sensor_name'].iloc[0]
        self.assertEqual('id6291474', substituted_sensor_name)
        self.assertEqual((9, 6), sensors_df.shape)

    def test_read_parse_metrics(self):
        metrics_df = get_metrics_df('test_files/test_metrics.json')
        self.assertIsInstance(metrics_df, pd.DataFrame)
        self.assertEqual((5, 5), metrics_df.shape)

    def test_read_parse_types(self):
        sensor_types_df = get_types_df('test_files/test_sensorTypes.json')
        self.assertIsInstance(sensor_types_df, pd.DataFrame)
        self.assertEqual((4, 3), sensor_types_df.shape)


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(CleanStringTest))
suite.addTest(unittest.makeSuite(ParseDataTest))


class NewResult(unittest.TextTestResult):
    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        return doc_first_line or ""


class NewRunner(unittest.TextTestRunner):
    resultclass = NewResult


if __name__ == "__main__":
    runner = NewRunner(verbosity=2)
    runner.run(suite)
