from rest_framework.decorators import api_view
from rest_framework.response import Response





names= {0: 'airport', 1: 'bindabasini', 2: 'hemja', 3: 'museum', 4: 'pumdikot', 5: 'ramghat_gumba', 6: 'ric', 7: 'stupa'}

landmark_id = {0:"PEMA TS'AL Monastery (Hemja Gumba)", 1:"RIC Building, Pashchimanchal Campus", 2:'Pokhara International Airport', 3:"Ramghat Monastery", 4:"Peace Pagoda Stupa", 5:"Pumdikot Shiva Temple", 6:"Gorkha Museum", 7:"Bindabasini Temple" }

#map names to landmark_id
mapping = {0:3, 1:8, 2:1, 3:7, 4:6, 5:4, 6:2, 7:5}


