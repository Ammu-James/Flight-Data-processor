#imports
import pandas as pd
from typing import List, Dict

class FlightDataProcessor:
    def __init__(self, file_path: str):
        """Initialize the class"""
        self.df = pd.read_json(file_path)

    def add_flight(self,New_data: dict) -> None: #add new rown to the data
        assert isinstance(New_data, dict), "New_data must be a dictionary"
        try:
            self.df = pd.concat([self.df, pd.DataFrame([New_data])], ignore_index=True)
            print("Successfully added the flight details")
        except Exception as ex:
            print(f"Error while adding the flight details: {ex}")

    def remove_flight(self,flight_name: str) -> None: #remove the row that contains the flight number
        assert isinstance(flight_name, str), "flight_name must be a string"
        if flight_name not in self.df['Flight Name'].values:
            print(f"Flight '{flight_name}' not found!")
            return
        try:
            self.df = self.df[self.df['Flight Name'] != flight_name]
            print("Successfully removed the flight details")
        except Exception as ex:
            print(f"Error while removing the flight details: {ex}")

    def flights_by_status(self,status: str) -> List[dict]:  #extract the data with the given status
        assert isinstance(status, str), "Status must be a string"
        List1 = self.df[self.df['Status']==status]
        if List1.empty:
            return [{"Error": f"No flights found with status '{status}'"}]
        return List1.to_dict(orient='records')

    def get_longest_flight(self) -> dict:  #get the longest duration flight in te given data set
        if self.df.empty:
            return {"Error": "No flights available"}
        self.df['Duration (minutes)'] = pd.to_numeric(self.df['Duration (minutes)'], errors='coerce')
        max_index = self.df['Duration (minutes)'].idxmax()
        list1 = self.df.loc[max_index].to_dict()
        return list1

    def update_flight_status(self,flight_name: str, new_status: str) -> None: #filter the flight with flight name and update the status
        assert isinstance(flight_name, str), "Flight Name must be a string"
        assert isinstance(new_status, str), "New Status must be a string"
        if flight_name not in self.df['Flight Name'].values:
            print(f"Flight '{flight_name}' not found!")
            return
        try:
            self.df.loc[self.df['Flight Name'] == flight_name,'Status'] = new_status
            print("Successfully updated the status details")
        except Exception as ex:
            print(f"Error while updated the status details: {ex}")

#inputs
file_path =r"C:\Users\sunil\Downloads\airline_dataset.json"
processor = FlightDataProcessor(file_path)
New_data = {'Flight Name':'Frontier 4533', 'Status':'On-Time', 'Departure Time':'2025-02-12T14:56:13.793', 
            'Arrival Time':'2025-02-24T20:56:13.684', 'Duration (minutes)' : 220,'Departure Airport':'BOS','Arrival Airport':'MIA'}


processor.add_flight(New_data)
processor.remove_flight("Frontier 4533")
flight_list = processor.flights_by_status("On-Time")
print(f"No of flights with the given status: {len(flight_list)}")
longest_flight = processor.get_longest_flight()
print(f"The longest flight is: {longest_flight['Flight Name']}")
processor.update_flight_status("American Airlines 353",'Canceled')
# processor.df.tail()

print("Processing Completed")
