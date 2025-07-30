# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 16:27:02 2025

@author: rabia
"""

# Gerekli kütüphaneleri içe aktarma
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib # Model kaydetmek/yüklemek için

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler # OneHotEncoder artık kullanılmıyor, çünkü binary zaten kodlu
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report

# Veri Yükleme
# CSV dosyanızın yolunu kendi sisteminize göre ayarlayın.
df = pd.read_csv(r'C:\Users\rabia\Desktop\bootcamp\heart.csv') #

# İlk Keşifsel Veri Analizi (EDA)
print("\n--- Veri Setinin İlk 5 Satırı ---")
print(df.head()) #

print("\n--- Veri Seti Bilgisi ---")
print(df.info()) #

print("\n--- İstatistiksel Özet ---")
print(df.describe()) #

print("\n--- Eksik Değer Kontrolü ---")
print(df.isnull().sum()) #

print("\n--- 'Heart_Risk' Değişkeninin Dağılımı ---")
print(df['Heart_Risk'].value_counts())
print(df['Heart_Risk'].value_counts(normalize=True) * 100) 

# Kalp Hastalığı Risk Durumu Görselleştirmesi
plt.figure(figsize=(7, 5))
sns.countplot(x='Heart_Risk', data=df, palette='viridis')
plt.title('Kalp Hastalığı Risk Durumu (0: Düşük, 1: Yüksek)')
plt.xlabel('Risk Seviyesi')
plt.ylabel('Sayı')
plt.xticks(ticks=[0, 1], labels=['Düşük Risk (0)', 'Yüksek Risk (1)'])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show() #


# Özellik Tanımlama
# Sayısal Özellikler (sadece Age)
numerical_features = ['Age']

binary_categorical_features = [col for col in df.columns if col not in numerical_features and col != 'Heart_Risk']

print(f"\nSayısal Özellikler: {numerical_features}")
print(f"Binary/Kategorik Özellikler: {binary_categorical_features}")

# Detaylı EDA ve Görselleştirmeler
print("\n--- Binary/Kategorik Özelliklerin 'Heart_Risk' ile İlişkisi ---")
plt.figure(figsize=(20, 20)) 
num_cols = 4 
num_rows = (len(binary_categorical_features) + num_cols - 1) // num_cols 

for i, feature in enumerate(binary_categorical_features):
    plt.subplot(num_rows, num_cols, i + 1)
    sns.countplot(x=feature, hue='Heart_Risk', data=df, palette='coolwarm')
    plt.title(f'{feature} vs Heart Risk')
    plt.xlabel(feature)
    plt.ylabel('Sayı')
    plt.xticks(ticks=[0, 1], labels=['Yok (0)', 'Var (1)'], rotation=45, ha='right')
plt.tight_layout()
plt.show() #

print("\n--- Sayısal Özelliğin ('Age') 'Heart_Risk' ile İlişkisi (Dağılım) ---")
plt.figure(figsize=(8, 6))
sns.histplot(data=df, x='Age', hue='Heart_Risk', kde=True, palette='viridis')
plt.title('Yaş Dağılımı (Kalp Riski Durumuna Göre)')
plt.xlabel('Yaş')
plt.ylabel('Sıklık')
plt.show() #

# Tüm özelliklerin hedef değişken ile korelasyonu 
correlation_with_target = df.corr()['Heart_Risk'].sort_values(ascending=False)
print("\n'Heart_Risk' ile Özellik Korelasyonları (Sıralı):")
print(correlation_with_target) #

# En yüksek korelasyonlu özellikleri görselleştirme
plt.figure(figsize=(10, 8))
correlation_with_target.drop('Heart_Risk').plot(kind='barh', cmap='coolwarm')
plt.title('Özelliklerin Kalp Riski ile Korelasyonu')
plt.xlabel('Korelasyon Katsayısı')
plt.ylabel('Özellik')
plt.tight_layout()
plt.show() #

# Bağımsız ve Bağımlı Değişkenleri Ayırma 
X = df.drop('Heart_Risk', axis=1)
y = df['Heart_Risk'] 

# Eğitim ve Test Setlerine Ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nEğitim seti boyutu: {X_train.shape}")
print(f"Test seti boyutu: {X_test.shape}")

# Özellik Dönüşümleri için Pipeline Oluşturma
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features), # Sadece 'Age' sütununu ölçeklendir
    ],
    remainder='passthrough' 
)

# Modelleri Tanımlama ve Karşılaştırma
models = {
    'Lojistik Regresyon': LogisticRegression(random_state=42, solver='liblinear'),
    'Karar Ağacı': DecisionTreeClassifier(random_state=42),
    'Rastgele Orman': RandomForestClassifier(random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42),
    'Destek Vektör Makineleri': SVC(random_state=42, probability=True), 
    'K-En Yakın Komşu': KNeighborsClassifier()
}

results = {}
best_roc_auc = -1 # En iyi ROC AUC değerini takip etmek için
best_pipeline = None # En iyi modeli tutmak için
best_model_name = "" 

for name, model in models.items():
    
    current_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                       ('classifier', model)])

# Modeli eğitme
    print(f"\n--- {name} Modeli Eğitiliyor ---")
    current_pipeline.fit(X_train, y_train)

# Tahminler yapma
    y_pred = current_pipeline.predict(X_test)
    y_pred_proba = current_pipeline.predict_proba(X_test)[:, 1] 
    
# Performans metriklerini hesaplama
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report_str = classification_report(y_test, y_pred)

    results[name] = {
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'ROC AUC': roc_auc,
        'Confusion Matrix': conf_matrix,
        'Classification Report': class_report_str
    }

    print(f"{name} Performansı:")
    print(f"  Doğruluk (Accuracy): {accuracy:.4f}")
    print(f"  Kesinlik (Precision): {precision:.4f}")
    print(f"  Hassasiyet (Recall): {recall:.4f}")
    print(f"  F1-Score: {f1:.4f}")
    print(f"  ROC AUC: {roc_auc:.4f}")
    print("\n  Karmaşıklık Matrisi:")
    print(conf_matrix)
    print("\n  Sınıflandırma Raporu:")
    print(class_report_str)

# En iyi pipeline'ı takip etme
    if roc_auc > best_roc_auc:
        best_roc_auc = roc_auc
        best_pipeline = current_pipeline 
        best_model_name = name

print(f"\n--- En İyi Performans Gösteren Model (ROC AUC'ye Göre): {best_model_name} ---")
print("Tüm Modellerin Özeti:")
for name, metrics in results.items():
    print(f"  {name}:")
    print(f"    Accuracy: {metrics['Accuracy']:.4f}, Precision: {metrics['Precision']:.4f}, Recall: {metrics['Recall']:.4f}, F1-Score: {metrics['F1-Score']:.4f}, ROC AUC: {metrics['ROC AUC']:.4f}")

#En İyi Modeli Kaydetme 
if best_pipeline:
    joblib.dump(best_pipeline, 'heart_disease_risk_prediction_model.pkl')
    print(f"\n'{best_model_name}' modeli 'heart_disease_risk_prediction_model.pkl' olarak kaydedildi.")
else:
    print("\nUyarı: Hiçbir model eğitilmedi veya best_pipeline belirlenemedi. Model kaydedilemedi.")

# Yeni Bir Kullanıcıdan Tahmin Alma ve Olasılık Hesabı
print("\n--- Yeni Kullanıcıdan Tahmin Alma Örneği ---")

# Yeni kullanıcı verisi (ÖNEMLİ: Tüm sütunları, orijinal df sırasına ve tiplerine göre ekleyin)
# Değerlerin float olmasına dikkat edin. Bu örnek verileri kendi senaryonuza göre değiştirin.
new_user_data = pd.DataFrame({
    'Chest_Pain': [1.0],
    'Shortness_of_Breath': [0.0],
    'Fatigue': [1.0],
    'Palpitations': [0.0],
    'Dizziness': [0.0],
    'Swelling': [0.0],
    'Pain_Arms_Jaw_Back': [1.0],
    'Cold_Sweats_Nausea': [0.0],
    'High_BP': [1.0],
    'High_Cholesterol': [1.0],
    'Diabetes': [0.0],
    'Smoking': [1.0],
    'Obesity': [1.0],
    'Sedentary_Lifestyle': [1.0],
    'Family_History': [1.0],
    'Chronic_Stress': [1.0],
    'Gender': [1.0], # 1.0 için erkek, 0.0 için kadın
    'Age': [58.0]
})

# Yüklenen modeli kullanarak tahmin yapma
try:
    loaded_model = joblib.load('heart_disease_risk_prediction_model.pkl')
except FileNotFoundError:
    print("Hata: Kaydedilmiş model dosyası bulunamadı. Lütfen önce bir model eğittiğinizden ve kaydettiğinizden emin olun.")
    loaded_model = None

if loaded_model:
# Olasılık Tahmini (Yüksek Risk - Sınıf 1 için)
    new_user_proba = loaded_model.predict_proba(new_user_data)[0]
    risk_percentage = new_user_proba[1] * 100

    print(f"\nKalp Krizi Riski Olasılığı: %{risk_percentage:.2f}")

# Sınıflandırma Etiketi (0 veya 1)
    new_user_prediction_label = loaded_model.predict(new_user_data)[0]
    print(f"Kalp Krizi Riski Sınıflandırması (0:Düşük, 1:Yüksek): {new_user_prediction_label}")

