from etl.extract import load_csv_data
from etl.transform import clean_and_transform
from etl.load import load_to_sqlite

def run_etl_pipeline():
    path = "data/breast_cancer_risk_data.csv"  # make sure this exists
    df = load_csv_data(path)
    cleaned = clean_and_transform(df)
    load_to_sqlite(cleaned)
    print("ETL complete: data loaded into cohort_data table.")

if __name__ == "__main__":
    run_etl_pipeline()

