import pandas as pd
import numpy as np
import re
import os

def build_nhanes_2021_2023(path, save_csv_path="/Users/sherrywang/Desktop/Data_Mining/Project/data-mining-project-starter/data/processed/nhanes.csv"):
    """
    Load and merge NHANES 2021–2023 (Cycle L) modules, decode categorical variables,
    and construct insurance type flags.
    The final dataset will be automatically saved as CSV.
    """

    # 1) Read all module files
    demo = pd.read_sas(path + "/DEMO_L.XPT")
    bmx  = pd.read_sas(path + "/BMX_L.XPT")
    bpx  = pd.read_sas(path + "/BPXO_L.XPT")
    lab  = pd.read_sas(path + "/GHB_L.XPT")
    glu  = pd.read_sas(path + "/GLU_L.XPT")
    smq  = pd.read_sas(path + "/SMQ_L.XPT")
    paq  = pd.read_sas(path + "/PAQ_L.XPT")
    slq  = pd.read_sas(path + "/SLQ_L.XPT")
    diq  = pd.read_sas(path + "/DIQ_L.XPT")
    inq  = pd.read_sas(path + "/INQ_L.XPT")
    dbq  = pd.read_sas(path + "/DBQ_L.XPT")
    hiq  = pd.read_sas(path + "/HIQ_L.XPT")
    hsq  = pd.read_sas(path + "/HSQ_L.XPT")
    huq  = pd.read_sas(path + "/HUQ_L.XPT")
    ocq  = pd.read_sas(path + "/OCQ_L.XPT")
    alq  = pd.read_sas(path + "/ALQ_L.XPT")
    agp  = pd.read_sas(path + "/AGP_L.XPT")

    dfs = [demo, bmx, bpx, lab, glu, smq, paq, slq, diq, inq, dbq, hiq, hsq, huq, ocq, alq, agp]

    # 2) Merge all datasets by respondent ID (SEQN)
    nhanes = dfs[0]
    for t in dfs[1:]:
        nhanes = nhanes.merge(t, on="SEQN", how="left")

    # 3) Select and rename columns of interest
    cols_map = {
        "SEQN": "id",
        "RIDAGEYR": "age",
        "RIAGENDR": "gender",
        "RIDRETH3": "race",
        "DMDEDUC2": "education",
        "INDFMPIR": "income_poverty_ratio",

        "BMXWT": "weight_kg",
        "BMXHT": "height_cm",
        "BMXBMI": "bmi",

        "BPXOSY1": "sbp",
        "BPXODI1": "dbp",

        "LBXGH": "a1c",
        "LBXGLU": "glucose",

        "SMQ020": "smoking_current",
        "SMQ040": "smoking_ever",

        "PAD820": "physical_activity_freq",
        "SLD012": "sleep_hours",

        "DIQ010": "diabetes_self_report",
        "HIQ011": "has_health_insurance",
        "HUQ010": "doctor_visit_12m",
    }
    nhanes = nhanes[list(cols_map.keys())].rename(columns=cols_map)

    # 4) Decode categorical variables using official codebooks
    gender_map = {1: "Male", 2: "Female"}
    race_map = {
        1: "Mexican American", 2: "Other Hispanic", 3: "Non-Hispanic White",
        4: "Non-Hispanic Black", 6: "Non-Hispanic Asian", 7: "Other Race / Multi"
    }
    education_map = {
        1: "<9th grade", 2: "9-11th grade", 3: "High school/GED",
        4: "Some college/AA", 5: "College graduate or above"
    }
    yesno_map = {1: "Yes", 2: "No", 7: "Refused", 9: "Don't know"}
    diabetes_map = {1: "Yes", 2: "No", 3: "Borderline", 7: "Refused", 9: "Don't know"}
    insurance_map = {1: "Insured", 2: "Not insured", 7: "Refused", 9: "Don't know"}
    visit_map = {1: "Yes", 2: "No", 7: "Refused", 9: "Don't know"}

    nhanes['gender'] = nhanes['gender'].map(gender_map)
    nhanes['race'] = nhanes['race'].map(race_map)
    nhanes['education'] = nhanes['education'].map(education_map)
    nhanes['smoking_current'] = nhanes['smoking_current'].map(yesno_map)
    nhanes['smoking_ever'] = nhanes['smoking_ever'].map(yesno_map)
    nhanes['diabetes_self_report'] = nhanes['diabetes_self_report'].map(diabetes_map)
    nhanes['has_health_insurance'] = nhanes['has_health_insurance'].map(insurance_map)
    nhanes['doctor_visit_12m'] = nhanes['doctor_visit_12m'].map(visit_map)

    # 5) Derive insurance type from HIQ032 multiple-mention variables
    hiq_cols = ['SEQN'] + [c for c in hiq.columns if str(c).upper().startswith('HIQ032')]
    hiq_32 = hiq[hiq_cols].copy()

    nhanes = nhanes.merge(
        hiq_32, left_on='id', right_on='SEQN', how='left', suffixes=('', '_hiq')
    )
    nhanes.drop(columns=['SEQN'], inplace=True)

    hiq32_cols_in_df = [c for c in nhanes.columns if str(c).upper().startswith('HIQ032')]
    bases = {}
    pat = re.compile(r'^(HIQ032[ABCDEFGHI])(?:_.+)?$', re.I)
    for c in hiq32_cols_in_df:
        m = pat.match(c)
        if m:
            base = m.group(1).upper()
            s = pd.to_numeric(nhanes[c], errors='coerce')
            if base not in bases or s.notna().sum() > bases[base].notna().sum():
                bases[base] = s

    hiq32 = pd.DataFrame(bases) if bases else pd.DataFrame(index=nhanes.index)

    has_any = (nhanes['has_health_insurance'] == 'Insured')
    private_flag = hiq32.eq(1).any(axis=1).fillna(False).to_numpy() if not hiq32.empty else np.zeros(len(nhanes), bool)
    public_codes = {2,3,4,5,6,8,9}
    public_flag  = hiq32.isin(public_codes).any(axis=1).fillna(False).to_numpy() if not hiq32.empty else np.zeros(len(nhanes), bool)

    private_only = has_any & private_flag & np.logical_not(public_flag)
    public_only  = has_any & np.logical_not(private_flag) & public_flag
    both         = has_any & private_flag & public_flag
    uninsured    = (nhanes['has_health_insurance'] == 'Not insured')

    nhanes['insurance_type'] = np.select(
        [private_only, public_only, both, uninsured],
        ['Private only', 'Public only', 'Both', 'Uninsured'],
        default='Unknown'
    )

    hiq_drop_cols = [c for c in nhanes.columns if str(c).upper().startswith("HIQ032")]
    nhanes.drop(columns=hiq_drop_cols, inplace=True, errors='ignore')

    # --- Save CSV automatically ---
    if os.path.isdir(save_csv_path): save_csv_path = os.path.join(save_csv_path, "nhanes.csv")
    nhanes.to_csv(save_csv_path, index=False)
    print(f"✅ NHANES dataset saved to: {save_csv_path}")


    return nhanes