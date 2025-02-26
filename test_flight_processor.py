import unittest
import os
import pandas as pd
from Flight_Processor import FlightDataProcessor  

class TestFlightDataProcessor(unittest.TestCase):
    def setUp(self):
        #Create a temporary test file and initialize the processor
        self.test_file = "test_airline_dataset.json"
        sample_data = [
            {'Flight Name': 'AA101', 'Status': 'On-Time', 'Departure Time': '2025-02-12T10:00:00',
             'Arrival Time': '2025-02-12T14:00:00', 'Duration (minutes)': 240, 'Departure Airport': 'JFK',
             'Arrival Airport': 'LAX'},
            {'Flight Name': 'BA202', 'Status': 'Delayed', 'Departure Time': '2025-02-12T12:00:00',
             'Arrival Time': '2025-02-12T16:00:00', 'Duration (minutes)': 180, 'Departure Airport': 'LHR',
             'Arrival Airport': 'DXB'}
        ]
        pd.DataFrame(sample_data).to_json(self.test_file, orient='records', indent=4)
        self.processor = FlightDataProcessor(self.test_file)

    def tearDown(self):
        #Remove the test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_flight(self):
        new_flight = {
            'Flight Name': 'DL303', 'Status': 'On-Time', 'Departure Time': '2025-02-13T08:00:00',
            'Arrival Time': '2025-02-13T12:00:00', 'Duration (minutes)': 240, 'Departure Airport': 'ATL',
            'Arrival Airport': 'ORD'
        }
        self.processor.add_flight(new_flight)
        self.assertIn('DL303', self.processor.df['Flight Name'].values)

    def test_remove_flight(self):
        self.processor.remove_flight('AA101')
        self.assertNotIn('AA101', self.processor.df['Flight Name'].values)

    def test_flights_by_status(self):
        flights = self.processor.flights_by_status('On-Time')
        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0]['Flight Name'], 'AA101')

    def test_get_longest_flight(self):
        longest_flight = self.processor.get_longest_flight()
        self.assertEqual(longest_flight['Flight Name'], 'AA101')

    def test_update_flight_status(self):
        self.processor.update_flight_status('BA202', 'Canceled')
        updated_status = self.processor.df.loc[self.processor.df['Flight Name'] == 'BA202', 'Status'].values[0]
        self.assertEqual(updated_status, 'Canceled')

    def test_invalid_flight_removal(self):
        self.processor.remove_flight('FakeFlight123')  # Should not raise an error
        self.assertEqual(len(self.processor.df), 2)  # Ensure no changes were made

    def test_invalid_status_search(self):
        flights = self.processor.flights_by_status('Non-Existent')
        self.assertEqual(flights, [{'Error': "No flights found with status 'Non-Existent'"}])

    def test_update_nonexistent_flight(self):
        self.processor.update_flight_status('FakeFlight123', 'Delayed')
        self.assertNotIn('FakeFlight123', self.processor.df['Flight Name'].values)

if __name__ == '__main__':
    unittest.main()
