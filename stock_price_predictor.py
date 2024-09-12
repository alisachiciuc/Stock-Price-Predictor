import os
import csv
import argparse
import random
from datetime import datetime, timedelta

# Create the argument parser
parser = argparse.ArgumentParser(description='Predict values of stock price.')

# Add the required arguments
parser.add_argument('--n', type=int, required=True, help='Number of files to process')
parser.add_argument('--input', type=str, required=True, help='Path to the input files')
parser.add_argument('--output', type=str, required=True, help='Path to the output files')

# Parse the arguments
args = parser.parse_args()


def generate_random_start_row(total_row_count):
    """
    Generates a random starting row.

    Args:
        total_row_count (int): The total number of rows in the file.

    Returns:
        int: A random starting row.
    """
    # Ensure the start row is non-negative
    if total_row_count < 10:
        return 0

    # Seed with the current timestamp
    current_timestamp = datetime.now().timestamp()
    random.seed(current_timestamp)

    # Ensure the start row is valid
    return random.randint(0, total_row_count-10)


def get_random_rows(file_path):
    """
    Retrieves 10 random rows from a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        list of dict: A list with the 10 random rows.
    """
    try:
        # Get the total number of rows in the file
        with open(file_path, mode='r', encoding='utf-8') as file:
            total_row_count = sum(1 for _ in file)

            # Generate a random starting row
            start_row = generate_random_start_row(total_row_count)

            random_rows = []
            current_row = 0

            # Read the file and extract the random rows
            file.seek(0)

            for row in file:
                if current_row >= start_row + 10:
                    break

                if current_row >= start_row:
                    splitted_row = row.strip().split(',')
                    random_rows.append({
                        'Stock-ID': splitted_row[0],
                        'Timestamp': datetime.strptime(splitted_row[1], "%d-%m-%Y").date(),
                        'Stock Price Value': float(splitted_row[2])
                    })
                current_row += 1

        return random_rows

    except FileNotFoundError:
        print(f'ERROR: The file {file_path} does not exist.')
    except PermissionError:
        print(f'ERROR: Permission denied for accessing {file_path}.')
    except Exception as e:
        print(f'ERROR: An unexpected error occurred: {e}')


def predict_next_values(random_rows):
    """
    Predicts the next 3 stock price values.

    Args:
        random_rows (list of dict): List containing stock rows.

    Returns:
        list of dict: Updated list of random rows and the new predicted values.
    """
    # Generate a set of sorted unique Stock Price Values
    unique_stock_price_values = set([row['Stock Price Value'] for row in random_rows])
    sorted_stock_price_values = sorted(unique_stock_price_values, reverse=True)

    # Get the last value and create the predicted values list
    n = random_rows[-1]['Stock Price Value']
    predicted_values = []

    # Calculate the next 3 predicted values
    predicted_values.append(sorted_stock_price_values[1])
    predicted_values.append(round(predicted_values[0] + (n - predicted_values[0])/2, 2))
    predicted_values.append(round(predicted_values[1] + (predicted_values[0] - predicted_values[1])/4, 2))

    # Update existing rows with new values
    for stock_price_values in predicted_values:
        random_rows.append({
            'Stock-ID': random_rows[-1]['Stock-ID'],
            'Timestamp': random_rows[-1]['Timestamp'] + timedelta(days=1),
            'Stock Price Value': stock_price_values
        })

    return random_rows


def format_rows(rows):
    """
    Formats the Timestamp and Stock Price Value for each row

    Args:
        rows (list of dict): List containing stock rows.

    Returns:
        list of dict: Updated list of formated rows.
    """
    for row in rows:
        row['Timestamp'] = row['Timestamp'].strftime('%d-%m-%Y')
        row['Stock Price Value'] = f"{float(row['Stock Price Value']):.2f}"

    return rows


def save_predicted_stock_rows(output_path, exchange_name, file_name, predicted_rows):
    """
    Saves the random rows and predicted values in a new CSV file.

    Args:
        output_path (str): The output path where the results will be saved.
        exchange_name (str): The name of the exchange containing CSV files.
        file_name (str): The name of the file containing predicted result.
        predicted_rows (list of dict): The list with random rows and new predicted values
    """
    try:
        # Generates the output path and creates exchanges if they don't exist
        exchange_path = os.path.join(output_path, exchange_name)

        if not os.path.exists(exchange_path):
            os.makedirs(exchange_path)

        # Generates the file path and formats the rows to be written
        formated_rows = format_rows(predicted_rows)
        file_path = os.path.join(exchange_path, file_name)

        # Writes the random and predicted rows to the file
        with open(file_path, 'w') as file:
            writer = csv.writer(file)
            for row in formated_rows:
                writer.writerow(row.values())

    except FileNotFoundError:
        print(f'ERROR: The directory {output_path} does not exist.')
    except PermissionError:
        print(f'ERROR: Permission denied for accessing {output_path}.')
    except Exception as e:
        print(f'ERROR: An unexpected error occurred: {e}')


def process_files_from_exchange(n, input_path, output_path, exchange_name):
    """
    Processes up to n CSV files from the specified exchange.

    Args:
        n (int): The maximum number of CSV files to process per exchange.
        input_path (str): The input path where exchanges are located.
        output_path (str): The output path where the results will be saved.
        exchange_name (str): The name of the exchange containing files.
    """
    try:
        processed_files_count = 0
        exchange_path = os.path.join(input_path, exchange_name)

        # Search for all files with the CSV extension
        for file_name in os.listdir(exchange_path):
            file_path = os.path.join(exchange_path, file_name)

            if os.path.isfile(file_path) and file_name.lower().endswith('.csv'):
                random_rows = get_random_rows(file_path)
                predicted_rows = predict_next_values(random_rows)
                save_predicted_stock_rows(output_path, exchange_name, file_name, predicted_rows)
                processed_files_count += 1

            # If the number of files is reached, stop
            if processed_files_count == n:
                return

    except FileNotFoundError:
        print(f'ERROR: The directory {exchange_path} does not exist.')
    except PermissionError:
        print(f'ERROR: Permission denied for accessing {exchange_path}.')
    except Exception as e:
        print(f'ERROR: An unexpected error occurred: {e}')


def process_exchanges(n, input_path, output_path):
    """
    Iterates through all exchanges in the specified input path.

    Args:
        n (int): The maximum number of CSV files to process per exchange.
        input_path (str): The input path where exchanges are located.
        output_path (str): The output path where the results will be saved.
    """
    try:
        # Search for all exchanges in the path
        for exchange_name in os.listdir(input_path):
            exchange_path = os.path.join(input_path, exchange_name)

            if os.path.isdir(exchange_path):
                process_files_from_exchange(n, input_path, output_path, exchange_name)

    except FileNotFoundError:
        print(f'ERROR: The directory {input_path} does not exist.')
    except PermissionError:
        print(f'ERROR: Permission denied for accessing {input_path}.')
    except Exception as e:
        print(f'ERROR: An unexpected error occurred: {e}')


def main():
    process_exchanges(args.n, args.input, args.output)


if __name__ == "__main__":
    main()
