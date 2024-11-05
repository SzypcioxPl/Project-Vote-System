import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def create_histogram(dataset, start, end, bin_split_in_percent, title, width_px, height_px):
    dpi = 100
    
    # Calculating number of time spaces
    number_of_bins = 100/bin_split_in_percent

    # Creating equal time spaces
    bins = pd.date_range(start=start, end=end, periods=number_of_bins+1)

    # Creating histogram
    plt.figure(figsize=(width_px/dpi, height_px/dpi), dpi=dpi)
    plt.hist(x=dataset, bins=bins, edgecolor='black')
    plt.xlabel("Time slots")
    plt.ylabel("Number of voters")
    plt.title(f"{title} ({bin_split_in_percent}%)")

    # X axis formating
    plt.xticks(ticks=bins, labels=bins, rotation=80, ha='right')
    plt.tight_layout()

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()  # Zamknięcie figury, aby zwolnić pamięć
    img_buffer.seek(0)

    return img_buffer