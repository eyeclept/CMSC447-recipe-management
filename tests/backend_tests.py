import requests
from urllib import parse
from urllib.parse import quote

FLASK = "http://localhost:5000"
GET_RECIPE = "/recipes/single/"
TRENDING_RECIPE = "/recipes/trending"
SEARCH_RECIPE = "/recipes/search"
FAV_RECIPE = "/recipes/favorites/"
OWN_RECIPE = "/recipes/user/"
RATE_RECIPE = "/recipes/rate"

RECIPE_ID = "recipe_id"
TITLE = "title"

def general_test(test_func, pass_text="TEST PASSED", fail_text="TEST FAILED", quiet=True):
    print(pass_text) if test_func(quiet) else print(fail_text)


def test_trending_recipe(quiet=True):
    resp_1 = requests.get(FLASK + TRENDING_RECIPE)
    resp_2 = requests.get(FLASK + TRENDING_RECIPE)
    
    if not resp_1.status_code == 200 and resp_2.status_code == 200:
        print("TRENDING TEST FAILED: DID NOT RETURN 200")
        return False
    print(resp_1.text)
    rec_1 = resp_1.json()
    rec_2 = resp_2.json()

    if not quiet:
        print(rec_1)
    
    # they should be different (technically, small chance they're the same)
    return rec_1[RECIPE_ID] != rec_2[RECIPE_ID]

def test_get_recipe(quiet=True):
    # get a recipe
    resp = requests.get(FLASK + TRENDING_RECIPE)
    rand_rec = resp.json()
    
    rand_id = rand_rec[RECIPE_ID]
    print(rand_id)
    resp = requests.get(FLASK + GET_RECIPE + rand_id)
    if resp.status_code != 200:
        print("FAILED TO GET RECIPE")
        print(resp.text)
        
        return False
    rec = resp.json()
    if not quiet:
        print("recipe", rec)
    
    return rec[TITLE] == rand_rec[TITLE]

def run_tests():
    general_test(test_trending_recipe, "TREND PASS", "TREND FAIL", False)
    general_test(test_get_recipe, "GET PASS", "GET FAIL", True)
    


if __name__ == '__main__':
    run_tests()