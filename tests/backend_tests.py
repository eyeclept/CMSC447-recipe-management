import requests
from getpass import getpass

FLASK = "http://localhost:5000"
GET_RECIPE = "/recipes/single/"
TRENDING_RECIPE = "/recipes/trending"
SEARCH_RECIPE = "/recipes/search"
FAV_RECIPE = "/recipes/favorites/"
OWN_RECIPE = "/recipes/user/"
RATE_RECIPE = "/recipes/rate"
LOGIN = "/login"

RECIPE_ID = "recipe_id"
TITLE = "title"


def get_jwt_token(username="Sam", password=None):
    # it's expected that you know the login creds for this
    if not password:
        password = getpass("Enter password: ")
    creds = {"username": username, "password": password}
    resp = requests.post(FLASK + LOGIN, json=creds)
    assert resp.status_code == 200 and "access_token" in resp.json()
    return resp.json()["access_token"]


JWT_TOKEN = get_jwt_token()  # a little gross but easier
JWT_HEADER = {"Authorization": f"Bearer {JWT_TOKEN}"}


def general_test(test_func,
                 pass_text="TEST PASSED",
                 fail_text="TEST FAILED",
                 quiet=True):
    print(pass_text) if test_func(quiet) else print(fail_text)


def test_trending_recipe(quiet=True):
    resp_1 = requests.get(FLASK + TRENDING_RECIPE)
    resp_2 = requests.get(FLASK + TRENDING_RECIPE)

    if not resp_1.status_code == 200 and resp_2.status_code == 200:
        print("TRENDING TEST FAILED: DID NOT RETURN 200")
        return False
    rec_1 = resp_1.json()
    rec_2 = resp_2.json()

    if not quiet:
        print(rec_1)

    # they should be different (technically, small chance they're the same)
    return rec_1[RECIPE_ID] != rec_2[RECIPE_ID]


def test_get_recipe(quiet=True):
    # get a recipe
    rand_rec = get_rand_recipe()

    rand_id = rand_rec[RECIPE_ID]
    resp = requests.get(FLASK + GET_RECIPE + rand_id)
    if resp.status_code != 200:
        print("FAILED TO GET RECIPE")
        return False
    rec = resp.json()
    if not quiet:
        print("recipe", rec)

    return rec[TITLE] == rand_rec[TITLE]


def test_search(quiet=True):
    search_term = "cheese"
    resp = requests.get(FLASK + SEARCH_RECIPE, params={"query": search_term})

    if resp.status_code != 200:
        print("SEARCH FAILED")
        return False
    results = resp.json()

    return isinstance(results, list) and len(results) > 0


def test_favorite(quiet=True):
    rand_rec = get_rand_recipe()
    rec_id = rand_rec[RECIPE_ID]
    username = "Sam"
    resp = requests.put(FLASK + FAV_RECIPE + username,
                        params={RECIPE_ID: rec_id},
                        headers=JWT_HEADER)

    if resp.status_code != 200:
        print("FAVORITE FAIL INSERT")
        print(resp.text)
        return False

    resp = requests.get(FLASK + FAV_RECIPE + username, headers=JWT_HEADER)
    if resp.status_code != 200:
        print("FAVORITE FAIL GET")

    data: list = resp.json()
    added = False
    for recipe in data:
        if recipe[RECIPE_ID] == rec_id:
            added = True
            break

    if not added:
        print("FAVORITE FAILED TO INSERT")
        return False

    resp = requests.delete(FLASK + FAV_RECIPE + username,
                           params={RECIPE_ID: rec_id},
                           headers=JWT_HEADER)
    if resp.status_code != 200:
        print("FAVORITE FAIL DELETE")
        return False

    resp = requests.get(FLASK + FAV_RECIPE + username, headers=JWT_HEADER)
    if resp.status_code != 200:
        print("FAVORITE FAIL GET")

    data: list = resp.json()
    for recipe in data:
        if recipe[RECIPE_ID] == rec_id:
            print("FAVORITE FAIL DELETE")
            return False

    return True


def test_own(quiet=True):
    DUMMY_RECIPE = {
        "title": "This is my test recipe",
        "ingredients": ["ingred1", "ingred2"],
        "directions": "blah blah directions",
        "description": "blah blah description",
        "keywords": ["some", "keywords", "here"]
    }
    username = "Sam"

    # put a recipe
    resp = requests.put(FLASK + OWN_RECIPE + username,
                        json=DUMMY_RECIPE,
                        headers=JWT_HEADER)
    if resp.status_code != 200:
        print("OWN FAILED TO PUT")
        print(resp.text)
        return False

    resp_data = resp.json()
    id = resp_data[RECIPE_ID]

    # check if it got added to db
    resp = requests.get(FLASK + OWN_RECIPE + username, headers=JWT_HEADER)
    if resp.status_code != 200:
        print("OWN FAILED TO GET RECIPES")
        return False

    added = False
    for recipe in resp.json():
        if recipe[RECIPE_ID] == id:
            added = True
            break
    if not added:
        print("OWN FAILED TO ADD TO DB")
        return False

    # update the title, include the recipe id because it's now known
    DUMMY_RECIPE["title"] = "My Updated Title"
    DUMMY_RECIPE[RECIPE_ID] = id
    resp = requests.put(FLASK + OWN_RECIPE + username,
                        json=DUMMY_RECIPE,
                        headers=JWT_HEADER)
    if resp.status_code != 200:
        print("OWN FAILED TO PUT (UPDATE)")
        return False

    # check that it returned the right status
    update_data = resp.json()
    if update_data["status"] != "updated":
        print("OWN FAILED UPDATE")
        print(update_data["status"])
        return False

    # check if ES has the updated recipe
    updated = get_recipe(id)
    if updated["title"] != DUMMY_RECIPE["title"]:
        print("OWN FAILED UPDATE ES")
        return False

    # recipe should be deleted
    resp = requests.delete(FLASK + OWN_RECIPE + username,
                           params={RECIPE_ID: id},
                           headers=JWT_HEADER)
    if resp.status_code != 200:
        print("OWN FAILED DELETE")
        return False

    resp = requests.get(FLASK + GET_RECIPE + id)
    if resp.status_code != 404:
        print("OWN FAILED DELETE (STILL PRESENT)")
        return False

    return True


def get_rand_recipe():
    resp = requests.get(FLASK + TRENDING_RECIPE)
    return resp.json()


def get_recipe(id):
    resp = requests.get(FLASK + GET_RECIPE + id)
    return resp.json()


def run_tests():

    general_test(test_trending_recipe, "TREND PASS", "TREND FAIL", True)
    general_test(test_get_recipe, "GET PASS", "GET FAIL", True)
    general_test(test_search, "SEARCH PASS", "SEARCH FAIL", True)
    general_test(test_favorite, "ADD FAV PASS", "ADD FAV FAIL", False)
    general_test(test_own, "OWN PASS", "OWN FAIL", False)


if __name__ == '__main__':
    run_tests()
