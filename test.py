from app import app
from unittest import TestCase
from models import db

coming_down_lyrics = """Look into the stars
Find every moment, moment on mars
Fly above the earth
Find every moment under the nine
Hey you found your way
You're coming down from outer space
Hey you found your way
You're coming down from outer space
Ride the dark lit skies
Find every moment as you fall to the light
Rise above the world
Find every moment you've left behind
Hey you found your way
You're coming down from outer space
Hey you found your way
You're coming down from outer space
Look into the stars
Find every moment, moment on mars
Fly above the earth
Find every moment under the nine
Hey you found your way
You're coming down from outer space
Hey you found your way
You're coming down from outer space"""

class RouteTestCase(TestCase):
  """Tests"""

  def setUp(self) -> None:
    print("setting up")
    return super().setUp()


  def tearDown(self) -> None:
    print("tearing down")
    db.session.rollback()
    return super().tearDown()

  
  def test_home(self):
    with app.test_client() as client:
      resp = client.get("/")

      self.assertEqual(resp.status_code, 302)


  def test_get_users(self):
    with app.test_client() as client:
      resp = client.get("/users")

      self.assertEqual(resp.status_code, 200)
      self.assertIn('<a href="/users/new"><button class="btn btn-primary">Create new user</button></a>', resp.get_data(as_text=True))


  def test_new_user(self):
    with app.test_client() as client:
      resp = client.get("/users/new")

      self.assertEqual(resp.status_code, 200)
      self.assertIn('<label>First Name</label><input type="text" name="first-name">', resp.get_data(as_text=True))


  def test_post_new_user(self):
    with app.test_client() as client:
      resp = client.post("/users/new", data={"first-name": "Mr.", "last-name": "Magoo", "image-url": ""})

      self.assertEqual(resp.status_code, 302)
      self.assertEqual(resp.location, "/users")

      resp = client.get("/users")

      CLIENT_ID = 6 # assuming after seed data in seed.py

      self.assertEqual(resp.status_code, 200)
      self.assertIn("Mr. Magoo", resp.get_data(as_text=True))

      # get user page
      resp = client.get(f"/users/{CLIENT_ID}")

      self.assertEqual(resp.status_code, 200)
      self.assertIn("Mr. Magoo", resp.get_data(as_text=True))

      # get edit user page
      resp = client.get(f"/users/{CLIENT_ID}/edit")
      self.assertEqual(resp.status_code, 200)
      self.assertIn('<label>First Name</label><input type="text" name="first-name" value="Mr.">', resp.get_data(as_text=True))
      self.assertIn('<label>Last Name</label><input type="text" name="last-name" value="Magoo">', resp.get_data(as_text=True))

      # edit user
      resp = client.post(f"/users/{CLIENT_ID}/edit", data={"first-name": "Bullwinkle", "last-name": "Moose", "image-url": ""})

      self.assertEqual(resp.status_code, 302)
      self.assertEqual(resp.location, "/users")

      # confirm edited user in users
      resp = client.get("/users")

      self.assertEqual(resp.status_code, 200)
      self.assertIn("Bullwinkle Moose", resp.get_data(as_text=True))

      # delete
      resp = client.post(f"/users/{CLIENT_ID}/delete")

      self.assertEqual(resp.status_code, 302)
      self.assertEqual(resp.location, "/users")


      resp = client.get("/users")

      self.assertEqual(resp.status_code, 200)
      # from home, make sure list is empty
      response_text = resp.get_data(as_text=True)
      response_text = response_text.replace("\n", "").replace(" ", "")

      self.assertNotIn("Mr. Magoo", response_text)

  def test_blog_cycle(self):
    """Go through cycle of creating a post, editing it, deleting it"""
    with app.test_client() as client:

      # create user for making posts
      resp = client.post("/users/new", data={"first-name": "Mr.", "last-name": "Magoo", "image-url": ""})

      self.assertEqual(resp.status_code, 302)
      self.assertEqual(resp.location, "/users")

      resp = client.get("/users")

      self.assertEqual(resp.status_code, 200)
      self.assertIn("Mr. Magoo", resp.get_data(as_text=True))

      CLIENT_ID = 6 ## assuming after running seed

      # get post page
      resp = client.get(f'/users/{CLIENT_ID}')

      self.assertEqual(resp.status_code, 200)
      self.assertIn('<h1>Mr. Magoo</h1>', resp.get_data(as_text=True))

      # get post form
      resp = client.get(f"/users/{CLIENT_ID}/posts/new")

      match_string = f"""<form id="new-post-form" action="/users/{CLIENT_ID}/posts/new" method="post">"""

      self.assertEqual(resp.status_code, 200)
      self.assertIn(match_string, resp.get_data(as_text=True))

      # create new post
      resp = client.post(f"/users/{CLIENT_ID}/posts/new", data={"title":"Magoo Post", "content":"Hello my name is Mr. Magoo, no, no relation.", "author_id":CLIENT_ID})

      self.assertEqual(resp.status_code, 302)
      self.assertEqual(resp.location, f"/users/{CLIENT_ID}")
      
      POST_ID = 9 # assuming after seed


      # get new post
      resp = client.get(f"/posts/{POST_ID}")

      self.assertEqual(resp.status_code, 200)
      self.assertIn("Hello my name is Mr. Magoo, no, no relation.", resp.get_data(as_text=True))

      # get edit post form
      resp = client.get(f"/posts/{POST_ID}/edit")

      self.assertEqual(resp.status_code, 200)
      self.assertIn("Hello my name is Mr. Magoo, no, no relation.", resp.get_data(as_text=True))

      # edit post
      resp = client.post(f"/posts/{POST_ID}/edit", data={"title":"Coming Down From Outer Space", "content":coming_down_lyrics})

      self.assertEqual(resp.status_code, 302)
      self.assertEqual(resp.location, f"/users/{CLIENT_ID}")

      # get edited post
      resp = client.get(f"/posts/{POST_ID}")

      self.assertEqual(resp.status_code, 200)

      self.assertIn("<h1>Coming Down From Outer Space</h1>", resp.get_data(as_text=True))
      self.assertIn("Rise above the world", resp.get_data(as_text=True))

      # delete post
      resp = client.post(f"/posts/{POST_ID}/delete")

      self.assertEqual(resp.status_code, 302)
      self.assertEqual(resp.location, f"/users/{CLIENT_ID}")

      # ensure post is gone
      resp = client.get(f"/users/{CLIENT_ID}")

      self.assertEqual(resp.status_code, 200)
      self.assertNotIn("Coming Down From Outer Space", resp.get_data(as_text=True))


  def test_tag_cycle(self):
    with app.test_client() as client:
      # get new tag form
      resp = client.get("/tags/new")

      self.assertEqual(resp.status_code, 200)
      self.assertIn('<h1>New Tag', resp.get_data(as_text=True))

      # post new tag
      resp = client.post("/tags/new", data={"tag-name":"taggy mctagface"})

      TAG_ID = 4 # assuming after seed

      self.assertEqual(resp.status_code, 302)
      self.assertEqual(resp.location, "/tags")

      # get all tags, see that new tag is there
      resp = client.get("/tags")

      self.assertEqual(resp.status_code, 200)
      self.assertIn('taggy mctagface', resp.get_data(as_text=True))

      # get tag edit form
      resp = client.get(f"/tags/{TAG_ID}/edit")

      self.assertEqual(resp.status_code, 200)
      self.assertIn('<button type="submit" class="btn btn-success">Save Tag Changes</button>', resp.get_data(as_text=True))

      # post edited tag
      resp = client.post(f"/tags/{TAG_ID}/edit", data={"tag-name":"junior mctagface"})

      self.assertEqual(resp.status_code, 302)
      self.assertEqual(resp.location, f"/tags/{TAG_ID}")

      # get all tags, see that edited tag is there
      resp = client.get("/tags")

      self.assertEqual(resp.status_code, 200)
      self.assertIn('junior mctagface', resp.get_data(as_text=True))

      # delete tag
      resp = client.post(f"/tags/{TAG_ID}/delete")

      self.assertEqual(resp.status_code, 302)
      self.assertEqual(resp.location, "/tags")

      # get all tags, see that deleted tag is not there
      resp = client.get("/tags")

      self.assertEqual(resp.status_code, 200)
      self.assertNotIn('tagface', resp.get_data(as_text=True))