"""Russell Zachary Feeser | z@rzfeeser.com
   Learning about FastAPI and python beyond just the basics"""

# python3 -m pip install "fastapi[standard]"
import fastapi
from pydantic import BaseModel

# create a mock database
forestrydb = [{"tree type": "walnut", "height": 100}]

# create a data model
class Treeinfo(BaseModel):
    tree_type: str
    tree_height: int
    harvestable: bool
    disease: bool

# create an instance of our webapp
app = fastapi.FastAPI()

# When a GET arrives @ http://ip:port/
@app.get("/")     # decorator
async def root(): # define a function (root is not a special name)
    return {"Instructor Zach": "It is breaktime"}  # in an HTTP 200 + this in msg body

@app.get("/survey/{tree_type}/{tree_height}")  # When a GET arrives @ http://ip:port/survey/<tree_type>
async def read_tt(tree_type, tree_height: int):    # this function expects input FROM the uri (tree_type)
    return {"tree type": tree_type, "height": tree_height} # returns tree_type (str) and height (int)

# when a GET arrives @ http://ip:port/survey?tree_type=locust&tree_height=75
@app.get("/survey") # this is JUST the path, not the query parameters
@app.get("/survey/")
async def read_params(tree_type: str = "maple", tree_height: int = 50):  # function calling query parameters
    forestrydb.append({"tree type": tree_type, "height": tree_height})
    return forestrydb


@app.get("/optional")
async def optional(season: str = "Summer", month: str | None = None):  # season is a string and defaults to summer, month is optional
    if month:   # if month was set by the user
        return {"Season": season, "Month": month}
    else:
        return {"Season": season}


@app.post("/v2/survey/")
async def create_tree(tree: Treeinfo):
    tree_dict = tree.dict()  # this creates a dictionary instance of the data we received
    if tree.harvestable == True and tree.disease == False:   # if we can harvest the tree
        tree_dict.update({"estimated price": 10 * tree.tree_height})
    else:
        tree_dict.update({"estimated price": None})
    return tree_dict
