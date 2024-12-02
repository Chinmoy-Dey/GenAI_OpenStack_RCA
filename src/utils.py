
def save_predictions(predictions, output_path):
    with open(output_path, "w") as f:
        for pred in predictions:
            f.write(f"{pred}\n")
