#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import cgi
import urllib
import datetime
import wsgiref.handlers

from django.utils import simplejson
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Todo(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  tags = db.StringListProperty()
  date_done = db.DateTimeProperty()
  date_added = db.DateTimeProperty(auto_now_add=True)

  def toJson(self):
    if self.date_done:
      date_done = self.date_done.isoformat()
    else:
      date_done = '-'
    
    return simplejson.dumps({'author': self.author.nickname(), 'content': self.content, 'date_added': self.date_added.isoformat(), 'date_done': date_done, 'tags': ",".join(self.tags), 'key': self.key().__str__() })

  def mark_done(self):
    if not self.date_done:
      self.date_done = datetime.datetime.now()

  def reopen(self):
    if self.date_done:
      self.date_done = None

  def done(self):
    return self.date_done != None

  def human_tags(self):
    return ','.join([self.link_to_tag(tag) for tag in self.tags])

  def link_to_tag(self, tag):
    return "<a href=\"/tags/" + tag +"\">" + tag + "</a>"


class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    
    todos = db.Query(Todo).filter('author =', user).filter('date_done = ', None).order('date_added')
    done_todos = db.Query(Todo).filter('date_done != ', None).order('-date_done').fetch(5)
    path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    self.response.out.write(template.render(path, { 'login_link': users.create_login_url('/'), 'user': user, 'todos': todos, 'done_todos': done_todos}))

class NewTodo(webapp.RequestHandler):
  def post(self):
    todo = Todo()

    if users.get_current_user():
      todo.author = users.get_current_user()

    todo.content = self.request.get('content')
    todo.tags = self._get_tags(self.request.get('tags'))
    todo.put()
    self.redirect('/')

  def _get_tags(self, tag_string):
    tags = []
    for tag in tag_string.split(','):
      tag = tag.strip()
      if not tag in tags:
        tags.append(tag)
    return tags

class GetTodo(webapp.RequestHandler):
  def get(self, id):
    todo = Todo.get(id)
    self.response.out.write(todo.toJson())


class DoneTodo(webapp.RequestHandler):
  def put(self, id):
    todo = Todo.get(id)
    todo.mark_done()
    todo.put()

    self.response.out.write(todo.toJson())

class ReopenTodo(webapp.RequestHandler):
  def put(self, id):
    todo = Todo.get(id)
    todo.reopen()
    todo.put()

    self.response.out.write(todo.toJson())

class TodosByTag(webapp.RequestHandler):
  def get(self, tag):
    user = users.get_current_user()
    path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    unescaped_tag = urllib.unquote(tag)

    todos = db.Query(Todo).filter('author =', user).filter('tags = ',unescaped_tag).order('date_done').order('date_added')
    self.response.out.write(template.render(path, { 'login_link': users.create_login_url('/'), 'user': user, 'todos': todos }))
    

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/todos', NewTodo),
  ('/todos/([^/]*)', GetTodo),
  ('/todos/([^/]*)/done', DoneTodo),
  ('/todos/([^/]*)/reopen', ReopenTodo),
  ('/tags/([^/]*)', TodosByTag)
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
