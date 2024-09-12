# Stock Price Predictor

## Description

The **Stock Price Predictor** is an App designed to predict future stock prices based on historical data. It processes CSV files containing stock information, generates random samples, and applies a prediction algorithm to estimate the next three stock prices. The results of the predictions are saved in new files at the specified output path.

The input data should be organized as follows:
- The input directory must contain stock exchanges folders.
- Each of these exchange folders should contain CSV files with historical stock price data.

## Dependencies

- **Python 3.6+**: Ensure you have Python 3.6 or newer installed.
- **Libraries**: 
  - `os`
  - `csv`
  - `argparse`
  - `random`
  - `datetime`

## Installing

**Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/stock-price-predictor.git
   ```

## How to run the program
**Run the command**
   ```bash
   python stock_price_predictor.py --n <number_of_files> --input <path_to_input_directory> --output <path_to_output_directory>
   ```
- --n:      The number of files to process from each exchange folder [1 or 2].
- --input:  The input path to the directory containing exchange folders and CSV files.
- --output: The output path to the directory where the result files will be saved.

## Authors
  **Alisa CHICIUC**
