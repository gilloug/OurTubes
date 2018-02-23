#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify

def main(mysql=None):
    ret = """ """
    ret += """
<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="icon" type="image/png" href="favicon.png" />
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes - Sign In</title>
  </head>
  <body>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <nav class="red accent-4">
    <ul class="nav nav-pills pull-right">
    <li><a class="blue-text accent-4" href="help"><i class="material-icons blue-text">help_outline</i></a></li>
    <li role="presentation" class="active"><a href="#!">OurTubes</a>
    </li>
    <li class="right"><a class="dropdown-button" href="#!" data-hover="true" data-belowOrigin="true" data-activates="dropdown0">Account<i class="material-icons right">arrow_drop_down</i></a></li>
    <ul id='dropdown0' class='dropdown-content'>
    <li class="active"><a href="register">Sign in</a></li>
    <li><a href="index">Log in</a></li>
    </ul>
    </ul>
    </nav>
    <div class="container jumbotron">
      <form class="form-signin">
        <label for="inputEmail" class="sr-only">Email</label>
        <input type="email" name="inputEmail" id="inputEmail" class="form-control" placeholder="email" required autofocus>
        <label for="inputPassword" class="sr-only">password</label>
        <input type="password" name="inputPassword" id="inputPassword" class="form-control" placeholder="Password" required>
	<label for="inputPasswordd" class="sr-only">Password</label>
        <input type="password" name="inputPasswordd" id="inputPasswordd" class="form-control" placeholder="Password" required>
	<button id="btnRegister" class="btn btn-lg btn-primary btn-block" type="button">Sign in</button>
	<script>
	  $(function() {
	  $('#btnRegister').click(function() {
          $.ajax({
          url: '/addUser',
          data: $('form').serialize(),
          type: 'POST',
          success: function(response) {
          Materialize.toast('You can now login', 3000, 'green')
          function show_popup(){
          location.reload();
          };
          window.setTimeout( show_popup, 3000 );
          },
          error: function(error) {
	  Materialize.toast('User cannot be created', 4000, 'red')
          }
          });
	  });
	  });
	</script>
      </form>
    </div>
    </div>
    <footer class="page-footer red accent-5>
    <div class="footer-copyright">
    <p class="center">&copy; BunnyCompany 2018</p>
    </div>
    </footer>
    </body>
    </html>"""
    return ret

