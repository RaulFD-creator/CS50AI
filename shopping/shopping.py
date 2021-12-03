import csv
import sys

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test set
    print("Loading data...")
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    print("Calculating ...")
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Initialise empty lists for evidence and labels
    evidence = []
    labels = []

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            evidence.append([
                int(row["Administrative"]),
                float(row["Administrative_Duration"]),
                int(row["Informational"]),
                float(row["Informational_Duration"]),
                int(row["ProductRelated"]),
                float(row["ProductRelated_Duration"]),                    
                float(row["BounceRates"]),
                float(row["ExitRates"]),
                float(row["PageValues"]),
                float(row["SpecialDay"]),
                month_to_num(row["Month"]),
                int(row["OperatingSystems"]),                    
                int(row["Browser"]),
                int(row["Region"]),
                int(row["TrafficType"]),
                1 if row["VisitorType"] == "Returning_Visitor" else 0,
                1 if row["Weekend"] == "TRUE" else 0
            ])
            labels.append(1 if row["Revenue"] == "TRUE" else 0)
        
    return (evidence, labels)

def month_to_num(Month):

    for _ in Month:

        if Month == "Jan":
            Month = 0
        elif Month == "Feb":
            Month = 1
        elif Month == "Mar":
            Month = 2
        elif Month == "Apr":
            Month = 3
        elif Month == "May":
            Month = 4
        elif Month == "June":
            Month = 5
        elif Month == "Jul":
            Month = 6
        elif Month == "Aug":
            Month = 7
        elif Month == "Sep":
            Month = 8
        elif Month == "Oct":
            Month = 9
        elif Month == "Nov":
            Month = 10
        elif Month == "Dec":
            Month = 11

    return Month

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    K = 1
    K = int(K)
    return KNeighborsClassifier(n_neighbors = K).fit(evidence, labels)

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty)

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    sensitivity = float(0)
    specificity = float(0)

    positive_accurate = float(0)
    negative_accurate = float(0)

    positive_total = float(0)
    negative_total = float(0)

    for label, prediction in zip(labels, predictions):
        if label == 1:
            positive_total += 1 
            if label == prediction:
                positive_accurate += 1

        if label == 0:
            negative_total += 1 
            if label == prediction:
                negative_accurate += 1 
    
    sensitivity = positive_accurate / positive_total
    specificity = negative_accurate / negative_total

    return (sensitivity, specificity)



if __name__ == "__main__":
    main()
