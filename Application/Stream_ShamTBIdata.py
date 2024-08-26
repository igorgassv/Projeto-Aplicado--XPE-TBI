import streamlit as st
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages
from statsmodels.formula.api import mixedlm

# Function to load the uploaded file
def load_file(file, file_type):
    try:
        if file_type == "csv":
            df = pd.read_csv(file)
        elif file_type in ["xls", "xlsx"]:
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type!")
            return None
        return df
    except ValueError as e:
        st.error(f"Error reading the file: {e}")
        return None

# Trimming function
def trim_data(data, tbi_date=None, days_before=6, days_after=6, temp_min=34, temp_max=39):
    if tbi_date is None or pd.isnull(tbi_date):
        st.error("TBI date is missing or invalid for this animal.")
        return pd.DataFrame()  # Return an empty DataFrame to indicate no data for this window

    try:
        tbi_date = pd.to_datetime(tbi_date)  # Ensure tbi_date is a datetime object
    except Exception as e:
        st.error(f"Error converting TBI date to datetime: {e}")
        return pd.DataFrame()

    start_date = tbi_date - pd.Timedelta(days=days_before)
    end_date = tbi_date + pd.Timedelta(days=days_after)

    trimmed_data = data[(data['date_time'] >= start_date) & (data['date_time'] <= end_date)]
    return trimmed_data

# Cosinor model function
def cosinor_model(time, mesor, amplitude, acrophase):
    return mesor + amplitude * np.cos((2 * np.pi * time / 24) - acrophase)

# Perform Cosinor Analysis and Save Results
def perform_cosinor_analysis(group_data, tbi_dates, analysis_window='both'):
    results = {'animal': [], 'group': [], 'experiment': [], 'window': [], 'Mesor': [], 'Amplitude': [], 'Acrophase': []}
    
    for animal, experiments in group_data.items():
        group = 'TBI' if animal in [2, 3, 6, 7, 8] else 'Sham'
        for exp, data in experiments.items():
            tbi_date = tbi_dates.get(animal)
            
            if analysis_window in ['both', 'before']:
                before_data = trim_data(data, tbi_date, days_before=6, days_after=0)
                if not before_data.empty:
                    perform_fit_and_store_results(before_data, animal, group, exp, 'before', results)
            
            if analysis_window in ['both', 'after']:
                after_data = trim_data(data, tbi_date, days_before=0, days_after=6)
                if not after_data.empty:
                    perform_fit_and_store_results(after_data, animal, group, exp, 'after', results)

    return pd.DataFrame(results)

def perform_fit_and_store_results(data, animal, group, exp, window, results):
    data['time'] = pd.to_datetime(data['date_time'])
    time_in_minutes = (data['time'] - data['time'].min()).dt.total_seconds() / 60
    time_in_hours = time_in_minutes / 60
    temperature = data['temp'].values

    if len(temperature) == 0:
        return

    guess = [temperature.mean(), (temperature.max() - temperature.min()) / 2, 0]

    try:
        params, _ = curve_fit(cosinor_model, time_in_hours, temperature, p0=guess)
        mesor, amplitude, acrophase = params

        results['animal'].append(animal)
        results['group'].append(group)
        results['experiment'].append(exp)
        results['window'].append(window)
        results['Mesor'].append(mesor)
        results['Amplitude'].append(amplitude)
        results['Acrophase'].append(acrophase)

    except RuntimeError as e:
        st.write(f"Curve fitting failed for animal {animal} experiment {exp} ({window} window): {e}")

# Streamlit page
st.title("Cosinor Analysis Dashboard")

# Section for uploading files
st.header("Upload Files")
metadata_file = st.file_uploader("Upload Metadata File", type=['csv', 'xlsx'])
temperature_files = st.file_uploader("Upload Temperature Data Files", type=['csv', 'xlsx'], accept_multiple_files=True)

# Load metadata and temperature data
metadata_df = None
temperature_data = {}

if metadata_file is not None:
    file_type = metadata_file.name.split('.')[-1]
    metadata_df = load_file(metadata_file, file_type)
    if metadata_df is not None:
        st.write("Metadata loaded successfully.")

if temperature_files:
    for file in temperature_files:
        file_name = file.name
        try:
            # Assuming the format is still 'brunaX_Y.xlsx' where X is animal and Y is experiment
            parts = file_name.split('_')
            if len(parts) >= 2:
                animal = int(parts[0].replace('bruna', ''))  # Extract animal number
                exp = int(parts[1].split('.')[0])  # Extract experiment number (before file extension)
            else:
                st.error(f"File name {file_name} is not in the expected format.")
                continue
            
            file_type = file_name.split('.')[-1]
            temp_df = load_file(file, file_type)
            if temp_df is not None:
                if animal not in temperature_data:
                    temperature_data[animal] = {}
                temperature_data[animal][exp] = temp_df
        except ValueError as e:
            st.error(f"Error parsing file name {file_name}: {e}")

if metadata_df is not None and temperature_data:
    tbi_dates = metadata_df.set_index('animal')['tbi_date'].to_dict()

    # Separate the data into TBI and Sham groups
    tbi_group_data = {animal: temperature_data[animal] for animal in [2, 3, 6, 7, 8] if animal in temperature_data}
    sham_group_data = {animal: temperature_data[animal] for animal in [1, 4, 5, 9, 10] if animal in temperature_data}

    st.header("Perform Cosinor Analysis")
    analysis_window = st.selectbox("Select Analysis Window", ['both', 'before', 'after'])

    if st.button("Run Analysis"):
        tbi_results = perform_cosinor_analysis(tbi_group_data, tbi_dates, analysis_window)
        sham_results = perform_cosinor_analysis(sham_group_data, tbi_dates, analysis_window)

        all_results = pd.concat([tbi_results, sham_results])

        # Save results to a CSV file
        csv_filename = 'cosinor_group_comparison_results.csv'
        all_results.to_csv(csv_filename, index=False)
        st.write(f"Results saved to {csv_filename}")

        # Visualization
        st.header("Visualize Results")

        # Combine 'group' and 'window' into a new column
        all_results['group_window'] = all_results['group'] + '_' + all_results['window']

        # Define a palette that matches the combined 'group_window' variable
        palette = {
            'Sham_before': 'black',
            'Sham_after': 'gray',
            'TBI_before': 'orange',
            'TBI_after': 'yellow'
        }

        # Create the plots
        plt.figure(figsize=(6, 12))  # Adjusted to be narrower and taller

        # MESOR plot
        plt.subplot(3, 1, 1)  # 3 rows, 1 column, first plot
        sns.boxplot(x='group', y='Mesor', hue='group_window', data=all_results, palette=palette)
        plt.title('MESOR')
        plt.xlabel('Group')
        plt.ylabel('MESOR')
        plt.ylim(all_results['Mesor'].min() - 0.5, all_results['Mesor'].max() + 0.5)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

        # Amplitude plot
        plt.subplot(3, 1, 2)  # 3 rows, 1 column, second plot
        sns.boxplot(x='group', y='Amplitude', hue='group_window', data=all_results, palette=palette)
        plt.title('Amplitude')
        plt.xlabel('Group')
        plt.ylabel('Amplitude')
        plt.ylim(all_results['Amplitude'].min() - 0.5, all_results['Amplitude'].max() + 0.5)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

        # Acrophase plot
        plt.subplot(3, 1, 3)  # 3 rows, 1 column, third plot
        sns.boxplot(x='group', y='Acrophase', hue='group_window', data=all_results, palette=palette)
        plt.title('Acrophase')
        plt.xlabel('Group')
        plt.ylabel('Acrophase')
        plt.ylim(all_results['Acrophase'].min() - 0.5, all_results['Acrophase'].max() + 0.5)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(plt)

        # Save the plot as TIFF and SVG
        tiff_filename = 'cosinor_group_comparison_plot.tiff'
        svg_filename = 'cosinor_group_comparison_plot.svg'
        plt.savefig(tiff_filename, format='tiff', dpi=300)
        plt.savefig(svg_filename, format='svg')
        st.write(f"Plots saved as {tiff_filename} and {svg_filename}")

        # Save the results to a PDF
        pdf_filename = 'cosinor_group_comparison_before_after.pdf'
        with PdfPages(pdf_filename) as pdf:
            plt.figure(figsize=(6, 12))

            plt.subplot(3, 1, 1)
            sns.boxplot(x='group', y='Mesor', hue='group_window', data=all_results, palette=palette)
            plt.title('MESOR')
            plt.xlabel('Group')
            plt.ylabel('MESOR')
            plt.ylim(all_results['Mesor'].min() - 0.5, all_results['Mesor'].max() + 0.5)
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

            plt.subplot(3, 1, 2)
            sns.boxplot(x='group', y='Amplitude', hue='group_window', data=all_results, palette=palette)
            plt.title('Amplitude')
            plt.xlabel('Group')
            plt.ylabel('Amplitude')
            plt.ylim(all_results['Amplitude'].min() - 0.5, all_results['Amplitude'].max() + 0.5)
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

            plt.subplot(3, 1, 3)
            sns.boxplot(x='group', y='Acrophase', hue='group_window', data=all_results, palette=palette)
            plt.title('Acrophase')
            plt.xlabel('Group')
            plt.ylabel('Acrophase')
            plt.ylim(all_results['Acrophase'].min() - 0.5, all_results['Acrophase'].max() + 0.5)
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

            plt.tight_layout()
            pdf.savefig()
            plt.close()

        st.write(f"PDF saved as {pdf_filename}")
