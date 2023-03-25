import os
import shutil

try:
  os.system('pip install tensorflow')
  import youtube_dl
except ImportError:
  print("Trying to Install required module: youtube_dl\n")
  os.system('python -m pip install tensorflow')

try:
  os.system('pip install numpy')
  import youtube_dl
except ImportError:
  print("Trying to Install required module: youtube_dl\n")
  os.system('python -m pip install numpy')

try:
  os.system('pip install pandas')
  import youtube_dl
except ImportError:
  print("Trying to Install required module: youtube_dl\n")
  os.system('python -m pip install pandas')

try:
  os.system('pip install scikit-learn')
  import youtube_dl
except ImportError:
  print("Trying to Install required module: youtube_dl\n")
  os.system('python -m pip install scikit-learn')
