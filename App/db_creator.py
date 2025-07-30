import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("sqlite:///Database.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()
DB_PATH = "Database.db"


#kod ilk çalıştığında Database varlığını arayacak şayet varsa çıkş yapacak yoksa database i oluşturacak bir kod.
def ignition():
    if not os.path.exists(DB_PATH):
        Base.metadata.create_all(engine)
        print("Veritabanı başarıyla oluşturuldu.")
    else:
        print("Veritabanı zaten mevcut.")

# bu tablo sadece giriş ekranında kullanılacak o yüzden simple.
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    #kullanıcı admin mi doktor mu ya da tıbbi gözlemci mi burada karar vereceğiz.
    # 0->hasta 1->doktor 2->admin 
    is_admin = Column(Integer, default=0)
    
    # Relationships
    patient = relationship("Patient", back_populates="user", uselist=False)
    doctor = relationship("Doktor", back_populates="user", uselist=False)
    health_data = relationship("Health_data", back_populates="user")
    user_suggestions = relationship("suggestions", back_populates="user")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="patient")
    doktor_id = Column(Integer, ForeignKey("doktors.id"), nullable=True)
    doctor = relationship("Doktor", back_populates="patients")

class Doktor(Base):
    __tablename__ = "doktors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="doctor")
    patients = relationship("Patient", back_populates="doctor")

class Health_data(Base):
    __tablename__ = "health_data"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="health_data")
    weight =  Column(Integer, nullable=False)
    height =  Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    chest_pain = Column(Integer, nullable=False)
    shortness_of_breath = Column(Integer, nullable=False)
    fatigue = Column(Integer, nullable=False, default=0)
    palpitations = Column(Integer, nullable=False, default=0)
    smoker = Column(Integer, nullable=False, default=0)
    diabetes = Column(Integer, nullable=False, default=0)
    dizziness = Column(Integer, nullable=False, default=0)
    swelling = Column(Integer, nullable=False, default=0)
    radiating_pain = Column(Integer, nullable=False, default=0)
    cold_sweats = Column(Integer, nullable=False, default=0)
    hypertension = Column(Integer, nullable=False, default=0)
    colestrol_high = Column(Integer, nullable=False, default=0)
    # obesity için nullable=True sebebi ise kullanıcıdan alınan bki verilerine göre biz belirleyeceğiz.
    obesity = Column(Integer, nullable=True) 
    family_history = Column(Integer, nullable=False, default=0)
    # buraya kadar alınan verileri database e pushlamadan once risk labelını belirlemeli yada dependency oluşturmalı.
    risk_label = Column(Integer, nullable=False, default=5)
#kullanıcının kayıt olurken bilemeyeceği için bu verilere default olarak 0 yani yok aatandı.

class suggestions(Base):
    __tablename__ = "suggestions"
    id = Column(Integer, primary_key=True)
    # ai tarafından alınan veri string yapılarak buraya aktarılacak.
    suggestion = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user_suggestions")



