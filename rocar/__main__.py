import sys
sys.path.append(".")

# cannot use relative import here
from rocar.web import app


app.run(debug=True)
