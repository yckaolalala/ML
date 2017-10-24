from pprocess import Load
from model_selection import Cross_val_score 

data = Load("./iris.data")

#score = Cross_val_score(data, model = 'dt', k = 5)
score = Cross_val_score(data, model = 'rf', k = 5)

print ("%f"%(score['accuracy']))
for key in score['recall']:
    print("%f %f"%(score['precision'][key], score['recall'][key]))
