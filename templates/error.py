#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify

def login(mysql = None):
    ret = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="icon" type="image/png" href="favicon.png" />
    <link rel="stylesheet" type="text/css" href="style.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes - Error</title>
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
		<a class="collapsible-header">Channels<i class="material-icons">arrow_drop_down</i></a>
		<div class="collapsible-body">
		  <ul>
                    <li><a href="createChan">create</a></li>
                    <li><a href="deleteChan">delete</a></li>
                    <li><a href="joinChan">join</a></li>
<li><a id="leave" name="leave" href="#!">leave</a></li>
    <script>
    $(function() {
    $('#leave').click(function(e) {
    $.ajax({
    url: '/leave',
    type: 'POST',
    success: function(response) {window.location.href = "index";},
    error: function(error) {}
    }); }); });</script>
		    <li class="divider"></li>
		    <li><a class="red-text accent-4" href="player"><i class="material-icons red-text">play_arrow</i>Player</a></li>
		  </ul>
		</div>
	      </li>
 	      <li>
		<a class="collapsible-header">Account<i class="material-icons">arrow_drop_down</i></a>
		<div class="collapsible-body">
		  <ul>
                    <li><a id="login" name="login" href="#!">Log in</a></li>
		  </ul>
		</div>
	      </li>
	      <li><a class="blue-text accent-4" href="help"><i class="material-icons blue-text">help_outline</i>Help</a></li>
            </ul>
	  </li>
	</ul>
	<ul class="right hide-on-med-and-down">
	  <li class="active">
	    <a class="dropdown-button" href="#!" data-hover="true" data-belowOrigin="true" data-activates="dropdown1">Channels<i class="material-icons right">arrow_drop_down</i></a>
	    <ul  id='dropdown1' class='dropdown-content'>
              <li><a href="createChan" class="black-text">create</a></li>
              <li><a href="deleteChan" class="black-text">delete</a></li>
              <li><a href="joinChan" class="black-text">join</a></li>
<li><a id="lve" name="lve" href="#!" class="black-text">leave</a></li>
    <script>
    $(function() {
    $('#lve').click(function(e) {
    $.ajax({
    url: '/leave',
    type: 'POST',
    success: function(response) {window.location.href = "index";},
    error: function(error) {}
    }); }); });</script>
	      <li class="divider"></li>
	      <li><a class="red-text accent-4" href="player"><i class="material-icons red-text">play_arrow</i>Player</a></li>
	    </ul>
	  <li>
	    <a class="dropdown-button" href="#!" data-hover="true" data-belowOrigin="true" data-activates="dropdown2">Account<i class="material-icons right">arrow_drop_down</i></a>
	    <ul  id='dropdown2' class='dropdown-content'>
              <li><a id="login" name="login" href="/" class="black-text">Log in</a></li>
	    </ul>
	  </li>
	  <li><a class="blue-text accent-4" href="help"><i class="material-icons blue-text left">help_outline</i>Help</a></li>
	</ul>
	<a href="#" data-activates="slide-out" class="button-collapse"><i class="material-icons">menu</i></a>
      </div>
    </nav>
  </body>
</html>
    <div class="row collection">
    <p class="center-align"><b><i>Log in</i></b></p>
    </div>
    </body>
    </html>"""
    return ret
