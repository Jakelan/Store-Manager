from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_labels(df, filename="labels.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    for index, row in df.iterrows():
        # Gather the information
        asin = row['ASIN']
        condition = row['CONDITION']
        total_retail = row['TOTAL RETAIL']
        sold_price = row['SOLD PRICE'] if row['SOLD PRICE'] else "_________€"

        # Format the label
        label = f"ASIN: {asin}, CONDITION: {condition}, TOTAL RETAIL: {total_retail}, SOLD PRICE: {sold_price}"

        # Draw the label
        c.drawString(80, height-80, label)
        height -= 50  # Spacing between labels

    c.save()

