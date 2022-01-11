#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import pickle
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler

class CustomScaler(BaseEstimator,TransformerMixin):
    def __init__(self,columns,copy=True,with_mean=True,with_std=True):
        self.scalar= StandardScaler(copy,with_mean,with_std)
        self.columns=columns
        self.mean_=None
        self.var_=None
        
    def fit(self, X, y=None, copy=None):
        self.scalar.fit(X[self.columns],y)
        self.mean_= np.mean(X[self.columns])
        self.var_= np.var(X[self.columns])
        return self
    
    def transform(self, X, y=None, copy=None):
        init_col_order= X.columns
        X_scaled= pd.DataFrame(self.scalar.transform(X[self.columns]), columns= self.columns)
        X_not_scaled = X.loc[:,~X.columns.isin(self.columns)]
        return pd.concat([X_not_scaled,X_scaled], axis=1)[init_col_order]
    
class absenteeism_model():
    def __init__(self,model_file,scaler_file):
        with open('model','rb') as model_file, open('scaler','rb') as scaler_file:
            self.reg= pickle.load(model_file)
            self.scaler=pickle.load(scaler_file)
            self.data=None
            
    def load_and_clean_data(self,data_file):
        df= pd.read_csv(data_file, delimiter=',')
        self.df_with_prdictions = df.copy()
        df = df.drop(['ID'],axis=1)
        df['Absenteeism Time in Hours']='NaN'
        
        reason_columns = pd.get_dummies(df['Reason for Absence'],drop_first=True)
        
        reason_type1= reason_columns.iloc[:,0:14].max(axis=1)
        reason_type2= reason_columns.iloc[:,14:17].max(axis=1)
        reason_type3= reason_columns.iloc[:,17:20].max(axis=1)
        reason_type4= reason_columns.iloc[:,20:].max(axis=1)
        
        df= df.drop(['Reason for Absence'], axis=1)
        
        df= pd.concat([df,reason_type1,reason_type2,reason_type3,reason_type4], axis = 1)
        
        column_names=['Date', 'Transportation Expense', 'Distance to Work','Age',
       'Daily Work Load Average', 'Body Mass Index', 'Education',
       'Children', 'Pets', 'Absenteeism Time in Hours', 'Reason 1', 'Reason 2', 'Reason 3', 'Reason 4']
        
        df.columns=column_names
        
        column_names_reordered= ['Reason 1', 'Reason 2', 'Reason 3', 'Reason 4','Date', 'Transportation Expense', 'Distance to Work','Age','Daily Work Load Average', 'Body Mass Index', 'Education',
       'Children', 'Pets', 'Absenteeism Time in Hours']
        
        df= df[column_names_reordered]
        
        df['Date'] = pd.to_datetime(df['Date'], format = '%d/%m/%Y')
        
        list_months=[]
        for i in range(df.shape[0]):
            list_months.append(df['Date'][i].month)
            
        df['Month Value']=list_months
        
        df['Day of the Week'] = df['Date'].apply(lambda x: x.weekday())
        
        df= df.drop(['Date'], axis=1)

        col_reordered = ['Reason 1', 'Reason 2', 'Reason 3', 'Reason 4','Month Value',
       'Day of the Week',
       'Transportation Expense', 'Distance to Work', 'Age',
       'Daily Work Load Average', 'Body Mass Index', 'Education',
       'Children', 'Pets', 'Absenteeism Time in Hours']
        
        df = df[col_reordered]
        
        df['Education'] = df['Education'].map({1:0,2:1,3:1,4:1})
        
        df=df.fillna(value=0)
        
        df=df.drop(['Absenteeism Time in Hours','Day of the Week','Daily Work Load Average',
                                           'Distance to Work'], axis=1)
        
        self.preprocessed_data = df.copy()
        
        self.data = self.scaler.transform(df)
        
        def predicted_probability(self):
            if (self.data is not None):
                pred = self.reg.predict.proba(self.data)[:,1]
                return pred
            
        def predicted_output_category(self):
            if (self.data is not None):
                pred_outputs = self.reg.predict(self.data)
                return pred_outputs
            
        def predicted_outputs(self):
            if (self.data is not None):
                self.preprocessed_data['Probability'] = self.reg.predict.proba(self.data)[:,1]
                self.preprocessed_data['Prediction'] = self.reg.predict(self.data)
                return self.preprocessed_data
            
            
            


# In[ ]:





# In[ ]:




