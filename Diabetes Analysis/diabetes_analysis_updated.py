import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# 1. Loading the dataset
df = pd.read_csv('diabetes.csv')

# 2. Quick overview of the data
print("Shape:", df.shape)
print(df.head())
print(df.info())

# 3. Quick statistical summary
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)
print(df.describe().T)

# 4. Checking for missing values
print("\nZero values per column:") 
print((df == 0).sum())

# 5. Replace zeros with median for columns where 0 is impossible
cols_with_zero= ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in cols_with_zero:
    median_val =df[col][df[col] != 0].median()
    df.loc[df[col] == 0, col] = median_val

# 6. Verify no remaining NaNs
print(df.isna().sum())

# 7. Splitting and Feature scaling
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler

# 8. Split features and target
X = df.drop('Outcome', axis=1) 
y = df['Outcome'] 

# 9. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
) 

# 10. Feature scaling  
scaler = StandardScaler() 
X_train_scaled = scaler.fit_transform(X_train) 
X_test_scaled = scaler.transform(X_test)

# 11. Show shapes of resulting arrays
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

import seaborn as sns 

# 12. Set style 
sns.set_style('whitegrid') 
plt.rcParams['figure.figsize'] = (12, 8) 

# 13. Outcome distribution 
plt.figure(figsize=(8, 5)) 
df['Outcome'].value_counts().plot(kind='bar', color=['#667eea', '#764ba2']) 
plt.title('Distribution of Diabetes Outcome', fontsize=16) 
plt.xlabel('Outcome (0=No, 1=Yes)') 
plt.ylabel('Count') 
plt.xticks(rotation=0) 
plt.savefig('plot_outcome_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 14. Feature histograms 
df.hist(bins=20, figsize=(15, 10), color='#667eea', edgecolor='black') 
plt.suptitle('Distribution of All Features', fontsize=16) 
plt.tight_layout() 
plt.savefig('plot_feature_histograms.png', dpi=300, bbox_inches='tight')
plt.close() 

# 15. Correlation heatmap 
plt.figure(figsize=(10, 8)) 
correlation = df.corr() 
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, square=True, linewidths=1) 
plt.title('Feature Correlation Heatmap', fontsize=16) 
plt.savefig('plot_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close() 

# 16. Box plots to identify outliers
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.ravel()
for i, col in enumerate(df.columns[:-1]): 
    sns.boxplot(data=df, y=col, ax=axes[i], color='#764ba2')
    axes[i].set_title(f'{col} Distribution')
plt.tight_layout()
plt.savefig('plot_box_plots.png', dpi=300, bbox_inches='tight')
plt.close()

# 17. Pairplot for key features 
key_features = ['Glucose', 'BMI', 'Age', 'Insulin', 'Outcome']
sns.pairplot(df[key_features], hue='Outcome', palette={0:'#667eea', 1: '#764ba2'})
plt.savefig('plot_pairplot.png', dpi=300, bbox_inches='tight')
plt.close()

# 18. Class imbalance check 
print("Class Distribution:") 
print(df['Outcome'].value_counts(normalize=True)) 

# 19. Key statistics by outcome 
print("\nMean values by Outcome:") 
print(df.groupby('Outcome').mean()) 

# 20. Identify potential outliers with Z-score > 4 (less strict for medical data)
from scipy import stats
z_scores = np.abs(stats.zscore(df.select_dtypes(include=[np.number])))
outliers = (z_scores > 4).sum()
print("\nNumber of outliers (Z-score > 4) per column:")
print(outliers)

# 21. See which columns have the most outliers
outliers_per_column = (z_scores > 4).sum(axis=0)
print("Outliers per column (Z > 4):")
print(outliers_per_column)

'''Baseline Model: Logistic Regression'''
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix 
# 22. Train baseline model 
lr_model = LogisticRegression(
    random_state=42, 
    max_iter=1000,
    class_weight='balanced') # Give more weight to diabetic class
lr_model.fit(X_train_scaled, y_train) 
# 23. Predictions 
y_pred_lr = lr_model.predict(X_test_scaled) 
# 24. Evaluate print("Logistic Regression Results:") 
print(f"Accuracy: {accuracy_score(y_test, y_pred_lr):.3f}") 
print("\nClassification Report:") 
print(classification_report(y_test, y_pred_lr))

'''Advanced Model: Random Forest'''
from sklearn.ensemble import RandomForestClassifier 
# 25. Train Random Forest 
rf_model = RandomForestClassifier(random_state=42, n_estimators=100) 
rf_model.fit(X_train_scaled, y_train) 
# 26. Predictions 
y_pred_rf = rf_model.predict(X_test_scaled) 
# 27. Evaluate print("Random Forest Results:") 
print(f"Accuracy: {accuracy_score(y_test, y_pred_rf):.3f}") 
print("\nClassification Report:") 
print(classification_report(y_test, y_pred_rf))

# 28. Feature importance from Random Forest (for report)
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("Top important features:")
print(feature_importance.head())

'''Gradient Boosting'''
from sklearn.ensemble import GradientBoostingClassifier 
# 29. Train Gradient Boosting 
gb_model = GradientBoostingClassifier(random_state=42, n_estimators=100) 
gb_model.fit(X_train_scaled, y_train) 
# 30. Predictions 
y_pred_gb = gb_model.predict(X_test_scaled) 
# 31. Evaluate 
print("Gradient Boosting Results:") 
print(f"Accuracy: {accuracy_score(y_test, y_pred_gb):.3f}") 
print("\nClassification Report:") 
print(classification_report(y_test, y_pred_gb))

# 32. Compare all models
from sklearn.metrics import recall_score

models_comparison = pd.DataFrame({
    'Model': ['Logistic Regression', 'Random Forest', 'Gradient Boosting'],
    'Accuracy': [
        accuracy_score(y_test, y_pred_lr),
        accuracy_score(y_test, y_pred_rf), 
        accuracy_score(y_test, y_pred_gb)
    ],
    'Diabetic_Recall': [
        recall_score(y_test, y_pred_lr, pos_label=1),
        recall_score(y_test, y_pred_rf, pos_label=1),
        recall_score(y_test, y_pred_gb, pos_label=1)
    ]
})
print(models_comparison)

'''Comprehensive Evaluation Metrics'''
from sklearn.metrics import ( 
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, roc_curve, confusion_matrix, classification_report 
)

# Use your existing Random Forest model (not best_rf_model)
y_pred = rf_model.predict(X_test_scaled)  # Use rf_model, not best_rf_model
y_pred_proba = rf_model.predict_proba(X_test_scaled)[:, 1] 

# Calculate metrics 
print("Model Performance Metrics:") 
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}") 
print(f"Precision: {precision_score(y_test, y_pred):.3f}") 
print(f"Recall: {recall_score(y_test, y_pred):.3f}") 
print(f"F1-Score: {f1_score(y_test, y_pred):.3f}") 
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.3f}") 
print("\nDetailed Classification Report:") 
print(classification_report(y_test, y_pred))

'''Confusion Matrix Visualization'''
# Confusion Matrix 
cm = confusion_matrix(y_test, y_pred) 
plt.figure(figsize=(8, 6)) 
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, 
            xticklabels=['No Diabetes', 'Diabetes'], 
            yticklabels=['No Diabetes', 'Diabetes']) 
plt.title('Confusion Matrix', fontsize=16) 
plt.ylabel('True Label') 
plt.xlabel('Predicted Label') 
plt.savefig('plot_confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
 
# Interpretation 
tn, fp, fn, tp = cm.ravel() 
print(f"\nTrue Negatives: {tn}") 
print(f"False Positives: {fp} (Type I Error)") 
print(f"False Negatives: {fn} (Type II Error - Most Critical!)") 
print(f"True Positives: {tp}")

'''ROC Curve'''
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba) 
roc_auc = roc_auc_score(y_test, y_pred_proba) 
plt.figure(figsize=(8, 6)) 
plt.plot(fpr, tpr, color='#667eea', lw=2, label=f'ROC Curve (AUC = {roc_auc:.3f})') 
plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--', label='Random Classifier') 
plt.xlim([0.0, 1.0]) 
plt.ylim([0.0, 1.05]) 
plt.xlabel('False Positive Rate') 
plt.ylabel('True Positive Rate') 
plt.title('Receiver Operating Characteristic (ROC) Curve') 
plt.legend(loc="lower right") 
plt.grid(alpha=0.3) 
plt.savefig('plot_roc_curve.png', dpi=300, bbox_inches='tight')
plt.close()

'''Feature Importance Analysis'''
# Get feature importance
importances = rf_model.feature_importances_ 
feature_names = X.columns

# Create DataFrame for visualization
feature_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
}).sort_values('Importance', ascending=False)

# Plot
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='#764ba2')
plt.xlabel('Importance Score')
plt.title('Feature Importance in Diabetes Prediction')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('plot_feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()

print("\nTop 5 Most Important Features:")
print(feature_importance_df.head())

# Simple prediction function
def predict_diabetes(pregnancies, glucose, bp, skin, insulin, bmi, dpf, age):
    input_data = np.array([[pregnancies, glucose, bp, skin, insulin, bmi, dpf, age]])
    input_scaled = scaler.transform(input_data)
    prediction = rf_model.predict(input_scaled)
    probability = rf_model.predict_proba(input_scaled)[0][1]
    return prediction[0], probability

# Test with sample data
pred, prob = predict_diabetes(1, 150, 70, 30, 100, 30.5, 0.6, 35)
print(f"Prediction: {'Diabetic' if pred == 1 else 'Healthy'}")
print(f"Probability: {prob:.2%}")