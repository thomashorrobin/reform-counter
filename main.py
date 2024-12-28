import requests
import time
import logging
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reform.log'),
        logging.StreamHandler()
    ]
)

def check_api() -> Dict[Any, Any]:
    """
    Makes a request to the API and returns the response
    """
    try:
        # Replace with your API endpoint
        response = requests.get('https://pro-worker.reformparty.uk/ticker/count')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        return {}

def append_to_file(timestamp: str, data: Dict[Any, Any]) -> None:
    """
    Append the API response data to a local file
    """
    try:
        # Create file if it doesn't exist
        file_path = Path("count_timeseries.txt")
        if not file_path.exists():
            logging.info("Creating new timeseries file")
            file_path.touch()
        
        # Append the data
        with open(file_path, "a") as f:
            f.write(f"{timestamp},{data}\n")
    except IOError as e:
        logging.error(f"Failed to write to file: {e}")

def process_response(data: Dict[Any, Any]) -> None:
    """
    Process the API response data
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_total = data.get('current_total', 'error')
    logging.info(f"Processing data: {current_total}")
    append_to_file(current_time, current_total)

def main() -> None:
    """
    Main function that runs the API check loop
    """
    interval = 60  # Time in seconds between checks

    logging.info("Starting API monitoring...")
    
    while True:
        try:
            # Get current timestamp
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.info(f"Checking API at {current_time}")

            # Check API and process response
            response_data = check_api()
            process_response(response_data)

            # Wait for the next interval
            time.sleep(interval)

        except KeyboardInterrupt:
            logging.info("Stopping API monitoring...")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    main()
