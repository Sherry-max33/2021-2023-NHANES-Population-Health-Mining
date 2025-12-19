# 📊 Health Insurance Coverage and Hypertension Risk Analysis

This repository presents an **end-to-end data mining** and **predictive modeling** project using `NHANES 2021–2023 data` (*11,933 observations x 21 variables*) to study **health insurance type**, **hypertension risk**, and **vulnerable population segmentation**.

# 🎯 Project Objectives

- **Association rule mining (Apriori)** to uncover interpretable socioeconomic / lifestyle / physiological patterns linked to insurance type and hypertension stage, evaluated with Support, Confidence, Lift, and additional rule-quality metrics (KULC and Imbalance Ratio).
- **Supervised learning** to perform two prediction tasks: (1) **multiclass insurance_type classification** and (2) **hypertension risk/stage prediction**, using **Decision Tree, Random Forest, and XGBoost**; evaluated with Accuracy, Precision, Recall, F1-score, Confusion Matrix, ROC-AUC, and feature importance.
- **Clustering-based segmentation using K-Prototypes to identify distinct subpopulations** (e.g., “Healthy & Insured”, “At-Risk Publicly Insured”, “Uninsured & Unhealthy”), with cluster quality assessed via Silhouette Score, intra-cluster variance, and cluster centroids for interpretability.

The results provide data-driven insights into **insurance disparities, hypertension risk stratification, and vulnerable population identification**, with potential implications for public health policy and targeted intervention strategies.

# 🧪 Dataset Description

**Source: NHANES (CDC)**
**Population:** Adult participants
**Key Variables:**
- Health insurance status:
 `Insurance coverage type` (`Private` / `Public` / `Both` / `Uninsured`), used as a multiclass prediction target.

- Blood pressure and clinical measurements:
  `Systolic and diastolic blood pressure` readings, `BMI`, and relevant laboratory indicators used for hypertension risk prediction.

- Demographic characteristics:
  `Age`, `gender`, and `race/ethnicity`, incorporated as core covariates across classification, clustering, and association rule mining.

- Socioeconomic indicators:
  `Income-to-poverty ratio`, `education level`, `employment status` reflecting healthcare access and structural disparities.

- Health behavior and lifestyle factors:
  `Smoking status`, `physical activity`, and `sleep hours`, capturing modifiable behavioral risk factors associated with hypertension and insurance outcomes.

# 🔍 Methodology Overview

**1. Data Preprocessing**  
- Variable renaming and distinct value decode  
- Missing value and outlier handling  
- Feature selection and transformation  
- Data integration across NHANES modules  

**2. Exploratory Data Analysis (EDA)**  
- Distributional analysis  
- Group comparisons  
- Visualization  

**3. Association Rule Mining**  
- Apriori algorithm  
- Evaluation of rules using support, confidence, lift, KULC, and imbalance ratio (IR)  
- Identification of interpretable rule-based patterns associated with insurance disparities and hypertension risk  

**4. Supervised Learning**  
- Decision Tree, Random Forest, and XGBoost  
- Model evaluation using accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrices  
- Supervised classification for insurance type prediction and hypertension risk/stage prediction  
- Feature importance analysis and model interpretability to support policy-relevant insights  

**5. Unsupervised Learning & Population Segmentation**  
- K-Prototypes to jointly handle mixed numerical and categorical features  
Clustering analysis to identify latent population subgroups  
- Evaluation of clustering quality using silhouette score, intra-cluster variance, and cluster centroids  
- Interpretation of clusters to characterize vulnerable and high-risk population segments  

# 📈 Key Findings (Summary)

✅**Insurance patterns:**  
**Private insurance** is associated with **higher income and college education**; **public insurance** is linked to **lower income** (especially women); **dual coverage** is mostly **older adults on Medicare**; **the uninsured group** is most heterogeneous and **hardest to predict**.  
✅**Hypertension risk:**  
Hypertension progression shows a clear **gradient—BMI dominates early (Stage 1)**, **age dominates severe risk (Stage 2)**, and **younger adults largely remain normotensive** even when overweight.  
✅**Population segments:**  
Clustering reveals **distinct risk profiles**, ranging from **low-income older smokers with moderate hypertension risk** to **high-BMI individuals with unstable insurance and severe hypertension**, alongside young healthy but uninsured and high-SES healthy groups.

Detailed results and visualizations are available in the final report notebooks and PDF.

# 🛠 Tools & Technologies

**Programming:** Python  
**Data Wrangling:** pandas, numpy 
**Pattern Mining:** Apriori 
**Modeling:** scikit-learn (Decision Tree, Random Forest), XGBoost  
**Clustering:** K-Prototypes  
**Visualization:** matplotlib, seaborn  

# 📌 Future Work

**Cost linkage:** Integrate NHANES with **external cost datasets** (e.g., MEPS) via *probabilistic* or *synthetic matching* to **estimate the healthcare cost** of identified risk groups.  
**Diet representation:** Use *representation learning (dietary embeddings)* to summarize **complex nutrition records and improve lifestyle–health modeling**.  
**Risk trajectories:** Apply **longitudinal and causal modeling** to study **how insurance stability and socioeconomic changes influence hypertension progression** over time.  
