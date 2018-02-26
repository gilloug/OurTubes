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
    <link rel="stylesheet" type="text/css" href="style.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes - Sign In</title>
  </head>
  <body>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <script>
      $( document ).ready(function() {
      $(".button-collapse").sideNav();
      });
    </script>
    <nav>
      <div class="nav-wrapper red accent-4">
	<a href="/" class="brand-logo">OurTubes</a>
	<ul id="slide-out" class="side-nav">
	  <li class="no-padding">
            <ul class="collapsible collapsible-accordion">
 	      <li>
		<a class="collapsible-header green accent-3">Account<i class="material-icons">arrow_drop_down</i></a>
		<div class="collapsible-body">
		  <ul>
                    <li class="green"><a href="register">Sign in</a></li>
                    <li><a href="index">Log in</a></li>
		  </ul>
		</div>
	      </li>
	      <li><a class="blue-text accent-4" href="help"><i class="material-icons blue-text">help_outline</i>Help</a></li>
            </ul>
	  </li>
	</ul>
	<ul class="right hide-on-med-and-down">
	    <li class="active"><a class="dropdown-button" href="#!" data-hover="true" data-belowOrigin="true" data-activates="dropdown2">Account<i class="material-icons right">arrow_drop_down</i></a>
	    <ul id='dropdown2' class='dropdown-content'>
               <li class="active"><a href="register">Sign in</a></li>
               <li><a href="index">Log in</a></li>
	    </ul>
	  <li><a class="blue-text accent-4" href="help"><i class="material-icons blue-text left">help_outline</i>Help</a></li>
	</ul>
</li>
	<a href="#" data-activates="slide-out" class="button-collapse"><i class="material-icons">menu</i></a>
      </div>
    </nav>
    <div class="container">
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
    </body>
    </html>"""
    return ret
