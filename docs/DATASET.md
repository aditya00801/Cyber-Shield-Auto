# CyberShield-Auto Dataset Documentation

## 1. Purpose

This document describes how CyberShield-Auto will use the CICIDS2017 dataset to develop and evaluate its network threat detection capabilities.

The dataset provides labeled network traffic records that can help evaluate whether the detection engine distinguishes benign traffic from traffic associated with simulated attacks.

The project may also use synthetic events to test application components that CICIDS2017 does not cover, such as Windows process monitoring, file activity, response policies, and API validation.

This document describes the intended dataset workflow. The exact files, columns, preprocessing steps, and evaluation results must be confirmed against the dataset available in the project.

## 2. Dataset overview

**Dataset name:** CICIDS2017

**Primary purpose:** Network intrusion detection and evaluation.

**Data format:** Commonly distributed as CSV files containing network flow records.

**Labels:** The dataset includes benign traffic and records associated with different attack scenarios.

**Planned use in CyberShield-Auto:** Develop and evaluate network traffic detection logic.

Before processing the dataset, inspect its directory structure, file names, column names, label values, and data types. Different files may require preprocessing before they can be combined.

## 3. Project objectives

CICIDS2017 will support the following development tasks:

* Inspect and understand network flow features.
* Identify the target label and available attack categories.
* Clean and validate the data.
* Prepare features for detection and evaluation.
* Evaluate the ability to distinguish benign traffic from labeled attack traffic.
* Measure false positives and false negatives.
* Compare detection results across relevant traffic categories.
* Reproduce test cases when detection behavior changes.

The dataset can help evaluate network intrusion detection. It cannot, by itself, establish the accuracy of every detection capability planned for CyberShield-Auto.

## 4. Dataset organization

The actual dataset files must be inspected before the project defines a fixed directory structure.

A proposed organization is:

```text
data/
├── README.md
├── raw/
│   └── CICIDS2017/
├── processed/
│   └── CICIDS2017/
├── evaluation/
│   └── CICIDS2017/
└── synthetic/
    └── test_events/
```

The directories have the following purposes:

| Directory     | Purpose                                                 |
| ------------- | ------------------------------------------------------- |
| `raw/`        | Original dataset files, preserved without modification  |
| `processed/`  | Cleaned and transformed records                         |
| `evaluation/` | Evaluation outputs and documented results               |
| `synthetic/`  | Controlled events for application and integration tests |

This is a proposed structure. If the repository already stores CICIDS2017 elsewhere, document and retain the existing location rather than creating duplicate copies.

Large dataset files should not be committed to Git without reviewing repository size limits, licensing terms, and data management requirements.

## 5. Dataset inspection

Before preprocessing, record the following information:

* Dataset directory and file names
* File formats and sizes
* Number of records in each file
* Available feature columns
* Label column and unique label values
* Missing values
* Duplicate records
* Invalid or infinite numeric values
* Class distribution
* Data types and parsing issues

Do not assume every CSV file has an identical schema or that every label is spelled consistently.

The inspection results should be documented after the actual files have been examined.

## 6. Data preprocessing

Preprocessing must preserve the meaning of the original records and labels.

The proposed workflow is:

1. Load the source files.
2. Inspect column names and data types.
3. Normalize column names where necessary.
4. Identify the target label.
5. Handle missing and invalid values according to a documented policy.
6. Check for duplicate records.
7. Convert numeric features to suitable types.
8. Separate input features from target labels.
9. Split the data for training, validation, and testing if machine learning is used.
10. Record the transformations so the results can be reproduced.

The original files should remain unchanged. Store transformed data separately.

Avoid silently deleting records simply because they contain unusual values. First determine whether those records are invalid, meaningful attack examples, or artifacts of data collection.

## 7. Labels and detection targets

The dataset's existing labels should be inspected before defining the application's target categories.

For an initial binary classification experiment, labels may be mapped into:

| Application label | Meaning                                                                     |
| ----------------- | --------------------------------------------------------------------------- |
| `benign`          | The source dataset identifies the record as benign                          |
| `attack`          | The source dataset identifies the record as belonging to an attack category |

If the project later needs attack-specific classification, preserve the original labels and define a separate mapping for the categories present in the actual dataset.

Document every label transformation.

Ground-truth labels are used to evaluate predictions. They must not be treated as information available to a live detection engine when it analyzes previously unseen traffic.

## 8. Feature handling

Network flow features may describe properties such as traffic volume, packet counts, flow duration, and timing characteristics. The exact features available to CyberShield-Auto must be confirmed by inspecting the dataset.

Feature processing should follow these rules:

* Separate input features from target labels.
* Exclude identifiers or fields that could leak the expected answer.
* Handle missing and non-finite values consistently.
* Apply scaling only when required by the selected model.
* Fit preprocessing transformations on training data only.
* Apply the fitted transformations to validation and test data.
* Keep a record of the feature columns expected by the trained model.

If a model requires a specific feature order, enforce that order during both training and inference.

## 9. Training and evaluation

If CyberShield-Auto uses machine learning for network traffic classification, divide the dataset into separate subsets.

**Training data:** Used to fit the model.

**Validation data:** Used to select model settings and decision thresholds.

**Test data:** Used to measure final performance on data not used during model selection.

The split strategy must account for the structure of the dataset. Where records from the same capture period or related traffic flows could leak information across subsets, evaluate whether a time-based or grouped split is more appropriate.

Do not select a model based on test-set results and then report those same results as an unbiased final evaluation.

Any preprocessing fitted to the data must follow the same separation rules.

## 10. Evaluation metrics

The project may use the following metrics to assess network detection performance:

| Metric              | Purpose                                                          |
| ------------------- | ---------------------------------------------------------------- |
| Accuracy            | Fraction of predictions that are correct                         |
| Precision           | Fraction of predicted attack records that are labeled as attacks |
| Recall              | Fraction of labeled attack records that are detected             |
| F1 score            | Harmonic mean of precision and recall                            |
| Confusion matrix    | Shows correct and incorrect predictions by class                 |
| False-positive rate | Fraction of benign records incorrectly classified as attacks     |
| Inference latency   | Time required to produce a prediction                            |

Accuracy alone is insufficient when class distributions are imbalanced.

Evaluation reports should include the test-set size, class distribution, preprocessing method, split strategy, model configuration, and results.

Results obtained from CICIDS2017 must be described as performance on that dataset. They do not establish the same performance on live network traffic or other Windows endpoints.

## 11. Data leakage and reproducibility

The evaluation process must reduce the risk of data leakage.

Required practices include:

* Keep target labels out of model input features.
* Fit preprocessing transformations using training data only.
* Avoid using test results to repeatedly tune the model.
* Record the random seed when a randomized split is used.
* Document the source files used for each experiment.
* Record the feature set, label mapping, and model settings.
* Preserve evaluation outputs needed to reproduce reported results.

If duplicate or closely related records appear across dataset files, investigate whether they could make the evaluation results overly optimistic.

## 12. Relationship to the detection engine

CICIDS2017 will support the network detection part of CyberShield-Auto.

Its records can be used to test whether network traffic features match known attack patterns or are classified as suspicious by a trained model.

Other application capabilities require separate test data.

| Capability                  | Suitable initial test data                                     |
| --------------------------- | -------------------------------------------------------------- |
| Network intrusion detection | CICIDS2017                                                     |
| Event validation            | Synthetic valid and invalid records                            |
| Process monitoring          | Synthetic process events or controlled Windows telemetry       |
| File activity detection     | Synthetic file events and isolated test files                  |
| Authentication detection    | Synthetic authentication events or suitable Windows event data |
| Incident correlation        | Controlled sequences of related events                         |
| Response policy             | Synthetic findings and simulated action requests               |
| API validation              | Valid and invalid API requests                                 |

The application should not interpret a network flow classification as proof that a particular Windows process or file is malicious. Such conclusions require supporting evidence from appropriate sources.

## 13. Privacy and licensing

Before redistributing or publishing dataset files, review the applicable license and usage terms.

The project should document the dataset's source and any transformations applied to it.

Do not mix personal endpoint logs or credentials into the evaluation dataset without an approved need and suitable protections.

## 14. Dataset testing

Tests should verify that:

* The expected files can be loaded.
* Required columns are present.
* Labels are recognized and mapped correctly.
* Missing and invalid values are handled according to policy.
* Numeric features are converted safely.
* Unexpected columns do not silently alter model inputs.
* Preprocessing produces consistent output.
* Training and test data remain separated.
* Evaluation metrics are calculated correctly.

Small fixtures should be used for routine unit tests. Loading the complete dataset should be reserved for tests where the full data volume is necessary.

## 15. Acceptance criteria

The dataset workflow is ready for model development when:

* The available CICIDS2017 files have been inventoried.
* The target label and feature columns are documented.
* Preprocessing rules are explicit and reproducible.
* Invalid values and duplicate records have been assessed.
* The train, validation, and test split strategy is documented.
* Evaluation metrics are calculated correctly.
* Data leakage checks have been performed.
* The results and limitations are recorded.

## 16. Open decisions

The following items require confirmation during implementation:

* The exact CICIDS2017 files available in the repository
* The feature columns and label values in those files
* Whether the first model will use binary or multiclass classification
* The preprocessing and data-splitting strategy
* The initial model selection criteria
* Whether additional datasets will be needed for endpoint-specific detection
* How large raw and processed files will be stored and versioned

## 17. Status

CICIDS2017 is the dataset identified for network intrusion detection work in CyberShield-Auto.

The actual file inventory, preprocessing pipeline, model, and evaluation results must be verified separately. This document does not claim that those components have already been implemented or tested.
