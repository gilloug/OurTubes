#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify


def main(login, connected_to, connected_as):
    ret = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="icon" type="image/png" href="favicon.png" />
    <link rel="stylesheet" type="text/css" href="style.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes - Help</title>
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
    }); }); });</script>"""
    if connected_as and connected_as == "Administrator":
        ret += """<li class="divider"></li>
	<li><a class="red-text accent-4" href="player"><i class="material-icons red-text">play_arrow</i>Player</a></li>"""
    ret += """</ul>
    </div>
	      </li>
 	      <li>
		<a class="collapsible-header">Account<i class="material-icons">arrow_drop_down</i></a>
		<div class="collapsible-body">
		  <ul>"""
    if login != "" and login != None:
        ret += """<li><a id="logout" name="logout" href="#!">Log out</a></li>
		    <script>
		      $(function() {
		      $('#logout').click(function(e) {
		      $.ajax({
		      url: '/logout',
		      type: 'POST',
		      success: function(response) {
		      window.location.href = "index";},
		      error: function(error) {}
		      }); }); });
		    </script>"""
    else:
        ret +="""<li><a id="login" name="login" href="/">Log in</a></li>"""
    ret += """</ul>
    </div>
    </li>
    <li><a class="blue-text accent-4 green accent-3" href="help"><i class="material-icons blue-text">help_outline</i>Help</a></li>
    </ul>
    </li>
    </ul>
	<ul class="right hide-on-med-and-down">
	  <li>
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
    }); }); });</script>"""
    if connected_as and connected_as == "Administrator":
        ret += """<li class="divider"></li>
        <li><a class="red-text accent-4" href="player"><i class="material-icons red-text">play_arrow</i>Player</a></li>"""
    ret += """</ul>
    <li>
	    <a class="dropdown-button" href="#!" data-hover="true" data-belowOrigin="true" data-activates="dropdown2">Account<i class="material-icons right">arrow_drop_down</i></a>
	    <ul  id='dropdown2' class='dropdown-content'>"""
    if login != "" and login != None:
        ret += """<li><a id="lgt" name="lgt" href="#!" class="black-text">Log out</a></li>
	      <script>
	  	$(function() {
	  	$('#lgt').click(function(e) {
	  	$.ajax({
	  	url: '/logout',
	  	type: 'POST',
	  	success: function(response) {
	  	window.location.href = "index";},
	  	error: function(error) {}
	  	}); }); });
	      </script>"""
    else:
        ret += """<li><a id="login" name="login" href="/" class="black-text">Log in</a></li>"""
    ret += """</ul>
    </li>
    <li class="active"><a class="blue-text accent-4" href="help"><i class="material-icons blue-text left">help_outline</i>Help</a></li>
    </ul>
    <a href="#" data-activates="slide-out" class="button-collapse"><i class="material-icons">menu</i></a>
    </div>
    </nav>
    </div>
    <div class="row collection">"""
    ret += """<p class="center-align"><b>Welcome to OurTube's help page!</b></p>"""
    ret += """<p class="center-align">This web application has been created to let you and your friend manage your playlist during parties.</p>"""
    ret += """<p class="center-align">When you arrive on the app you have to create a free account with a valid email and a password. To do so you can go to the "<b>Sign In</b>" tab.</p>"""
    ret += """<p class="center-align">Now that you have an account, you just have to to go to the "<b>Log In</b>" tab, to fill your email and password.</p>"""
    ret += """<br/><p class="center-align"><b>After login you can access the whole application:</b></p>"""
    ret += """<p class="center-align">Create a Channel to create a playlist with your friends on the "<b>Channel - Create</b>" tab,</p>"""
    ret += """<p class="center-align">Join a Channel by going on the "<b>Channel - Join</b>" tab,</p>"""
    ret += """<p class="center-align">Leave a Channel when you want to manage another playlist by going on the "<b>Channel - Leave</b>" tab,</p>"""
    ret += """<p class="center-align">Delete your Channel after your parrty by going to the "<b>Channel - Delete</b>" tab,</p>"""
    ret += """<p class="center-align">To see the current channel's playlist and act on it you just have to go to the "<b>OurTube</b>" tab, our main page,</p>"""
    ret += """<p class="center-align">If you are the administrator of the channel, you can arbitrarily delete musics on the main page,</p>"""
    ret += """<p class="center-align">If you are the administrator of the channel, you can launch the playlist by going to the "<b>Channel - Play</b>" tab,</p>"""
    ret += """<p class="center-align">Log out by clicking on the "<b>Account - Log Out</b>" tab.</p>"""
    ret += """<br/><p class="center-align">Have fun and do not hesitate to contact our team by email: <i>ourtubesteam@gmail.com</i></p>"""
    ret += """</div>
    </body>
    </html>"""
    return ret
