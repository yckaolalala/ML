import pprocess as pp
from model_selection import cross_val_score 

data = pp.Load("./iris.data")

score = cross_val_score(data, model = 'dt', k = 5)

print ("%f"%(score['accuracy']))
for key in score['recall']:
    print("%f %f"%(score['precision'][key], score['recall'][key]))
